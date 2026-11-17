import { lookup } from "node:dns/promises";
import { realpath } from "node:fs/promises";
import { isIP } from "node:net";
import { dirname, isAbsolute, relative } from "node:path";
import { fileURLToPath } from "node:url";

const DNS_TIMEOUT_MS = 2_000;
const MAX_REDIRECT_HOPS = 5;
const INLINE_SCHEMES = new Set(["data:", "blob:", "about:"]);

function parseIpv4(address) {
  if (isIP(address) !== 4) return null;
  const octets = address.split(".").map(Number);
  return octets.length === 4 ? octets : null;
}

export function isPublicNetworkAddress(rawAddress) {
  const address = rawAddress.trim().replace(/^\[|\]$/g, "").toLowerCase();
  const ipv4 = parseIpv4(address);
  if (ipv4) {
    const [a = 0, b = 0, c = 0] = ipv4;
    if (a === 0 || a === 10 || a === 127 || a >= 224) return false;
    if (a === 100 && b >= 64 && b <= 127) return false;
    if (a === 169 && b === 254) return false;
    if (a === 172 && b >= 16 && b <= 31) return false;
    if (a === 192 && (b === 168 || (b === 0 && (c === 0 || c === 2)))) return false;
    if (a === 192 && b === 88 && c === 99) return false;
    if (a === 198 && (b === 18 || b === 19 || (b === 51 && c === 100))) return false;
    if (a === 203 && b === 0 && c === 113) return false;
    return true;
  }
  if (isIP(address) !== 6) return false;
  if (address.includes(".")) {
    const mapped = address.slice(address.lastIndexOf(":") + 1);
    return address.startsWith("::ffff:") && isPublicNetworkAddress(mapped);
  }
  const first = Number.parseInt(address.split(":", 1)[0] || "0", 16);
  if (first < 0x2000 || first > 0x3fff) return false;
  return !address.startsWith("2001:db8:") && !address.startsWith("2002:");
}

const defaultResolver = async (hostname) =>
  (await lookup(hostname, { all: true, verbatim: true })).map(({ address }) => address);

export async function isAllowedPublicHttpUrl(
  rawUrl,
  hostnameCache = new Map(),
  resolveHostname = defaultResolver
) {
  let url;
  try {
    url = new URL(rawUrl);
  } catch {
    return false;
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") return false;
  const hostname = url.hostname.replace(/^\[|\]$/g, "").toLowerCase();
  if (
    hostname === "localhost" ||
    hostname.endsWith(".localhost") ||
    hostname.endsWith(".local") ||
    hostname.endsWith(".internal") ||
    hostname.endsWith(".home.arpa")
  ) {
    return false;
  }
  if (isIP(hostname)) return isPublicNetworkAddress(hostname);
  if (hostnameCache.has(hostname)) return hostnameCache.get(hostname);

  let timer;
  try {
    const addresses = await Promise.race([
      resolveHostname(hostname),
      new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Error(`DNS lookup timed out for ${hostname}`)), DNS_TIMEOUT_MS);
      }),
    ]);
    const allowed = addresses.length > 0 && addresses.every(isPublicNetworkAddress);
    hostnameCache.set(hostname, allowed);
    return allowed;
  } catch {
    hostnameCache.set(hostname, false);
    return false;
  } finally {
    if (timer) clearTimeout(timer);
  }
}

export async function isAllowedPdfFileUrl(rawUrl, inputPath) {
  let url;
  try {
    url = new URL(rawUrl);
  } catch {
    return false;
  }
  if (url.protocol !== "file:") return false;
  try {
    const [inputRealPath, requestedRealPath] = await Promise.all([
      realpath(inputPath),
      realpath(fileURLToPath(url)),
    ]);
    const allowedRoot = dirname(inputRealPath);
    const rel = relative(allowedRoot, requestedRealPath);
    return rel === "" || (!rel.startsWith("..") && !isAbsolute(rel));
  } catch {
    return false;
  }
}

export function createPdfRouteGuard(inputPath, { resolveHostname = defaultResolver } = {}) {
  const hostnameCache = new Map();
  return async (route) => {
    if (route.request().resourceType() === "script") {
      await route.abort();
      return;
    }

    let currentUrl = route.request().url();
    let parsed;
    try {
      parsed = new URL(currentUrl);
    } catch {
      await route.abort();
      return;
    }
    if (INLINE_SCHEMES.has(parsed.protocol)) {
      await route.continue();
      return;
    }
    if (parsed.protocol === "file:") {
      if (await isAllowedPdfFileUrl(currentUrl, inputPath)) await route.continue();
      else await route.abort();
      return;
    }
    if (!(await isAllowedPublicHttpUrl(currentUrl, hostnameCache, resolveHostname))) {
      await route.abort();
      return;
    }

    let response = await route.fetch({ maxRedirects: 0 });
    for (let hop = 0; response.status() >= 300 && response.status() < 400; hop += 1) {
      const location = response.headers()["location"];
      if (!location || hop >= MAX_REDIRECT_HOPS) {
        await response.dispose();
        await route.abort();
        return;
      }
      const nextUrl = new URL(location, currentUrl).toString();
      if (!(await isAllowedPublicHttpUrl(nextUrl, hostnameCache, resolveHostname))) {
        await response.dispose();
        await route.abort();
        return;
      }
      await response.dispose();
      currentUrl = nextUrl;
      response = await route.fetch({ url: currentUrl, maxRedirects: 0 });
    }
    await route.fulfill({ response });
  };
}
