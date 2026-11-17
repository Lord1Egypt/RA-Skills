#!/usr/bin/env node
// Listing URL -> a saved property. The single entrypoint for adding or
// refreshing: it scrapes, geocodes, downloads the photo, and writes the store.
//
// Runs the page through Camoufox (plain HTTP gets a bot wall), reads only
// standards-based surfaces, geocodes the address, and downloads the hero photo.
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as net from 'node:net';
import * as dns from 'node:dns/promises';
import * as http from 'node:http';
import * as https from 'node:https';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

import { extractScraped, geocodeQuery } from './extract.ts';
import type { PageSurfaces } from './extract.ts';
import { coerceScraped, readStore, slugify, upsertScraped, writeStore } from './store.ts';
import type { Scraped } from './store.ts';
import { resolveDataDir } from './properties.ts';

const require = createRequire(import.meta.url);

const RENDER_TIMEOUT_MS = 45_000;
const POLL_INTERVAL_MS = 750;
const MAX_PHOTO_REDIRECTS = 3;
const MAX_PHOTO_BYTES = 20 * 1024 * 1024;
const PHOTO_TIMEOUT_MS = 20_000;
const NOMINATIM = 'https://nominatim.openstreetmap.org/search';
// Nominatim's usage policy requires a descriptive agent identifying the app.
const USER_AGENT = 'property-hunt/0.1 (personal property tracker; https://clawhub.ai)';

const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));

/** A browser failure is a tool *result*, not a crashed command — see plow-browser-usage. */
function toolError(error: string): void {
  process.stdout.write(`${JSON.stringify({ type: 'tool_error', error })}\n`);
}

function note(message: string): void {
  process.stderr.write(`${message}\n`);
}

/**
 * Read the page's structured surfaces. Deliberately no DOM selectors: only
 * JSON-LD and Open Graph, so a cosmetic redesign can't break the scrape.
 */
async function harvest(browser: any, url: string): Promise<PageSurfaces> {
  const jsonldText: string[] = await browser.eval(
    `[...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent)`,
  );
  const og: Record<string, string> = await browser.eval(
    `Object.fromEntries([...document.querySelectorAll('meta[property^="og:"], meta[name^="twitter:"]')]
       .map(m => [m.getAttribute('property') || m.getAttribute('name'), m.content || '']))`,
  );
  const jsonld: unknown[] = [];
  for (const text of jsonldText ?? []) {
    try {
      jsonld.push(JSON.parse(text));
    } catch {
      // A single malformed block is normal; the others still carry the listing.
    }
  }
  return { url, jsonld, og: og ?? {} };
}

/**
 * `goto` resolves while the page is still a client-side shell — a fixed sleep
 * either wastes time or reads an empty page and looks exactly like a bot wall.
 * Poll instead, until the page yields a record the store will actually accept.
 *
 * Validating *inside* the loop is the point: a page can mount its JSON-LD
 * (whose PostalAddress often has no postalCode) before the og:title that
 * carries the full "…, San Francisco, CA 94131" line. Checking only after the
 * loop would abort on that half-rendered state when one more poll would have
 * produced a saveable record — the retry mechanism has to be able to see the
 * failure it exists to ride out.
 */
export async function scrapeRendered(
  browser: any,
  url: string,
  timeoutMs: number = RENDER_TIMEOUT_MS,
): Promise<{ scraped: Scraped; photoUrl: string | null }> {
  await browser.goto(url);
  const deadline = Date.now() + timeoutMs;
  let lastError = 'page never rendered a listing';
  while (Date.now() < deadline) {
    try {
      const { scraped, photoUrl } = extractScraped(await harvest(browser, url));
      // The same rules `upsert` applies — so anything unsaveable fails here,
      // before the geocode and photo download that would otherwise leave an
      // orphaned image named for a slug no row will ever carry.
      return { scraped: coerceScraped(scraped), photoUrl };
    } catch (err) {
      lastError = (err as Error).message;
      await sleep(POLL_INTERVAL_MS);
    }
  }
  // Everything the loop swallows lands here — a thin page, but also a bot
  // wall, a page crash, or a browser that went away mid-run. Only offer the
  // "try another site" remedy when the page actually rendered and simply
  // lacked a field; prescribing it for a browser failure sends the agent off
  // after the wrong problem.
  const missingField = /is required|could not find an address|no usable characters/.test(lastError);
  throw new Error(
    `could not read a saveable listing from ${url} after ${timeoutMs / 1000}s. ` +
      `Last problem: ${lastError}.` +
      (missingField
        ? ' If the page genuinely does not publish that field, try this property on another' +
          ' listing site — do not supply a value of your own.'
        : ''),
  );
}

/** Keyless, same OpenStreetMap ecosystem the map tiles come from. */
async function geocode(scraped: Scraped): Promise<{ lat: number; lng: number } | null> {
  const query = geocodeQuery(scraped);
  const response = await fetch(`${NOMINATIM}?q=${encodeURIComponent(query)}&format=json&limit=1`, {
    headers: { 'User-Agent': USER_AGENT, Accept: 'application/json' },
  });
  if (!response.ok) throw new Error(`geocoder returned HTTP ${response.status}`);
  const hits = (await response.json()) as Array<{ lat: string; lon: string }>;
  if (!hits.length) return null;
  return { lat: Number(hits[0].lat), lng: Number(hits[0].lon) };
}

/**
 * Is this address one we must never issue a request to?
 *
 * The hero-image URL comes from the listing page's own JSON-LD or og:image, so
 * it is attacker-controlled text. Without this, a hostile listing could point
 * og:image at 127.0.0.1 or a RFC1918 host and use us as a blind probe into
 * whatever the agent container can reach.
 */
export function isPrivateAddress(ip: string): boolean {
  if (net.isIPv4(ip)) {
    const [a, b] = ip.split('.').map(Number);
    if (a === 0 || a === 127 || a === 10) return true;
    if (a === 169 && b === 254) return true; // link-local, incl. cloud metadata
    if (a === 172 && b >= 16 && b <= 31) return true;
    if (a === 192 && b === 168) return true;
    if (a === 100 && b >= 64 && b <= 127) return true; // carrier-grade NAT
    return a >= 224; // multicast and reserved
  }
  // Judge v6 numerically, never by its text. One address has many spellings:
  // ::ffff:127.0.0.1 and ::ffff:7f00:1 are the same loopback, and matching the
  // dotted form alone let the hex form through to the very RPC port this guard
  // exists to protect.
  const bytes = ipv6Bytes(ip);
  if (!bytes) return true; // unparseable but isIP-accepted — fail closed
  if (bytes.every((b) => b === 0)) return true; // ::
  if (bytes.slice(0, 15).every((b) => b === 0) && bytes[15] === 1) return true; // ::1
  if ((bytes[0] & 0xfe) === 0xfc) return true; // fc00::/7 unique-local
  if (bytes[0] === 0xfe && (bytes[1] & 0xc0) === 0x80) return true; // fe80::/10 link-local
  if (bytes[0] === 0xff) return true; // ff00::/8 multicast

  // Anything embedding a v4 address is judged as that v4 address: ::/64 covers
  // v4-mapped and v4-translated; 64:ff9b::/96 is NAT64.
  const embedsV4 =
    bytes.slice(0, 8).every((b) => b === 0) ||
    (bytes[0] === 0x00 && bytes[1] === 0x64 && bytes[2] === 0xff && bytes[3] === 0x9b);
  return embedsV4 ? isPrivateAddress(bytes.slice(12).join('.')) : false;
}

/** Expand any IPv6 spelling to its 16 bytes, so the checks above compare values. */
function ipv6Bytes(ip: string): number[] | null {
  const clean = ip.toLowerCase().replace(/^\[|\]$/g, '').split('%')[0];
  if (!net.isIPv6(clean)) return null;

  // A trailing dotted quad ("::ffff:127.0.0.1") is two hextets in disguise.
  let text = clean;
  const dotted = text.match(/(\d{1,3}(?:\.\d{1,3}){3})$/);
  if (dotted) {
    const [a, b, c, d] = dotted[1].split('.').map(Number);
    text = `${text.slice(0, -dotted[1].length)}${((a << 8) | b).toString(16)}:${((c << 8) | d).toString(16)}`;
  }

  const [head, tail] = text.split('::');
  const headParts = head ? head.split(':').filter(Boolean) : [];
  const tailParts = text.includes('::') && tail ? tail.split(':').filter(Boolean) : [];
  const parts = text.includes('::')
    ? [...headParts, ...Array(8 - headParts.length - tailParts.length).fill('0'), ...tailParts]
    : headParts;
  if (parts.length !== 8) return null;

  const bytes: number[] = [];
  for (const part of parts) {
    const value = Number.parseInt(part, 16);
    if (!Number.isInteger(value) || value < 0 || value > 0xffff) return null;
    bytes.push((value >> 8) & 0xff, value & 0xff);
  }
  return bytes;
}

/**
 * Resolve a destination once and return the exact address we vetted.
 *
 * Returning the address is the whole point. Validating a *name* and then
 * letting the HTTP client resolve it again is two lookups, and an attacker who
 * controls the domain can answer them differently — public for the check,
 * loopback for the connect. The caller pins to this address, so there is only
 * ever one resolution to poison.
 */
export async function resolvePublicDestination(
  raw: string,
  base?: URL,
): Promise<{ url: URL; address: string; family: number }> {
  const url = new URL(raw, base);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`refusing a ${url.protocol} image URL`);
  }
  const literal = url.hostname.replace(/^\[|\]$/g, '');
  const resolved = net.isIP(literal)
    ? [{ address: literal, family: net.isIP(literal) }]
    : await dns.lookup(url.hostname, { all: true });

  if (resolved.length === 0) throw new Error(`could not resolve ${url.hostname}`);
  // Every answer must be public: accepting the name because *one* record is
  // public would let an attacker mix in a decoy and still win on the rest.
  if (resolved.some((entry) => isPrivateAddress(entry.address))) {
    throw new Error(`refusing a request to a non-public address (${url.hostname})`);
  }
  return { url, address: resolved[0].address, family: resolved[0].family };
}

/**
 * GET the vetted address, keeping the URL's Host header and TLS servername so
 * pinning breaks neither virtual hosting nor certificate validation.
 */
function getPinned(
  url: URL,
  address: string,
  family: number,
): Promise<{ status: number; location: string | null; type: string; body: Buffer }> {
  const client = url.protocol === 'https:' ? https : http;
  return new Promise((resolve, reject) => {
    const request = client.get(
      url,
      {
        headers: { 'User-Agent': USER_AGENT },
        // Connect to the address already vetted, not to whatever the name
        // resolves to on a second lookup. Node's happy-eyeballs path calls
        // lookup with { all: true } and expects an array — answering only the
        // single-address form yields "Invalid IP address: undefined".
        lookup: (_host: string, opts: { all?: boolean }, done: Function) =>
          opts?.all ? done(null, [{ address, family }]) : done(null, address, family),
        servername: url.hostname.replace(/^\[|\]$/g, ''),
      } as never,
      (response) => {
        const chunks: Buffer[] = [];
        let bytes = 0;
        response.on('data', (chunk: Buffer) => {
          bytes += chunk.length;
          if (bytes > MAX_PHOTO_BYTES) {
            request.destroy();
            reject(new Error(`image exceeds ${MAX_PHOTO_BYTES / 1024 / 1024} MB`));
            return;
          }
          chunks.push(chunk);
        });
        response.on('end', () =>
          resolve({
            status: response.statusCode ?? 0,
            location: (response.headers.location as string | undefined) ?? null,
            type: (response.headers['content-type'] as string | undefined) ?? '',
            body: Buffer.concat(chunks),
          }),
        );
        response.on('error', reject);
      },
    );
    request.on('error', reject);
    request.setTimeout(PHOTO_TIMEOUT_MS, () => request.destroy(new Error('image request timed out')));
  });
}

async function downloadPhoto(photoUrl: string, dir: string, id: string): Promise<string> {
  // Every hop is resolved and vetted, then connected to by address — a public
  // URL that 302s inward, or a name that rebinds between check and connect,
  // both fail here rather than reaching the network behind us.
  let hop = await resolvePublicDestination(photoUrl);
  let response = await getPinned(hop.url, hop.address, hop.family);

  for (let redirects = 0; response.status >= 300 && response.status < 400; redirects += 1) {
    if (redirects >= MAX_PHOTO_REDIRECTS) throw new Error(`too many redirects (over ${MAX_PHOTO_REDIRECTS})`);
    if (!response.location) throw new Error(`HTTP ${response.status} with no redirect target`);
    hop = await resolvePublicDestination(response.location, hop.url);
    response = await getPinned(hop.url, hop.address, hop.family);
  }

  if (response.status < 200 || response.status >= 300) throw new Error(`HTTP ${response.status}`);
  if (!response.type.startsWith('image/')) {
    throw new Error(`not an image (${response.type || 'no content-type'})`);
  }

  const ext = response.type.includes('png') ? '.png' : response.type.includes('webp') ? '.webp' : '.jpg';
  const relative = path.join('photos', `${id}${ext}`);
  const destination = path.join(dir, relative);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  // Same atomic discipline as the store: the page may be open on this file.
  const tmp = `${destination}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, response.body);
  fs.renameSync(tmp, destination);
  return relative;
}

/**
 * A refresh replaces `scraped` wholesale, so a transient geocoder outage or a
 * dead image host would blank a pin or photo we already had — losing data on
 * what is meant to be a routine price check. Enrichment that failed this run
 * keeps whatever the last successful run found. Returns what was kept.
 */
export function keepPreviousEnrichment(
  scraped: Scraped,
  previous: Scraped | undefined,
  dir: string,
): string[] {
  if (!previous) return [];
  const kept: string[] = [];
  if (scraped.lat === null && previous.lat !== null) {
    scraped.lat = previous.lat;
    scraped.lng = previous.lng;
    kept.push('coordinates');
  }
  // Only carry a photo whose file is still there. Keeping the path blind would
  // paper over a failed download with a record pointing at nothing, which the
  // map renders as a broken image — worse than the honest plain marker.
  const photoOnDisk = previous.photo !== null && fs.existsSync(path.join(dir, previous.photo));
  if (scraped.photo === null && photoOnDisk) {
    scraped.photo = previous.photo;
    kept.push('photo');
  }
  return kept;
}

async function main(): Promise<void> {
  const url = process.argv[2];
  if (!url || !/^https?:\/\//i.test(url)) {
    toolError("usage: node scrape.ts '<listing-url>'");
    return;
  }

  // Read before opening the browser. This is the guard: a missing or damaged
  // store fails here with an actionable message, rather than after the scrape,
  // the geocode, and a photo download that has already written an image.
  // It also gives us what this property looked like before the refresh.
  const dir = resolveDataDir();
  const before = readStore(dir);

  const { connect } = require('plow-browser');
  let browser: any;
  try {
    browser = connect(process.env.CAMOUFOX_RPC_ENDPOINT);
  } catch (err) {
    if ((err as Error & { name?: string })?.name === 'BrowserNotConnected') {
      return toolError('browser unavailable: endpoint not provisioned — enable Plow Browser in Settings');
    }
    throw err;
  }

  const { scraped, photoUrl } = await scrapeRendered(browser, url);
  const id = slugify(scraped);

  // Neither of the next two failures should lose the listing: a property with
  // no pin is still worth having, and the frontend surfaces it explicitly.
  try {
    const point = await geocode(scraped);
    if (point) {
      scraped.lat = point.lat;
      scraped.lng = point.lng;
    } else {
      note(`no coordinates found for "${scraped.address}" — it will show under "not on the map"`);
    }
  } catch (err) {
    note(`geocoding failed (${(err as Error).message}) — it will show under "not on the map"`);
  }

  if (photoUrl) {
    try {
      scraped.photo = await downloadPhoto(photoUrl, dir, id);
    } catch (err) {
      note(`photo download failed (${(err as Error).message}) — the pin will use a plain marker`);
    }
  }

  for (const field of keepPreviousEnrichment(scraped, before.find((row) => row.id === id)?.scraped, dir)) {
    note(`kept the previous ${field} for ${id}`);
  }

  const next = upsertScraped(before, scraped);
  writeStore(dir, next);
  process.stdout.write(`${next.length > before.length ? 'added' : 'refreshed'} ${id}\n`);
}

// Only run when invoked directly, so tests can import scrapeRendered.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    const name = (err as Error & { name?: string })?.name ?? 'Error';
    const detail = String((err as Error)?.message ?? err);
    toolError(
      name === 'BrowserNotConnected'
        ? 'browser unavailable: service unreachable (it may be restarting — retry once after 60s)'
        : detail.startsWith(`${name}:`)
          ? detail
          : `${name}: ${detail}`,
    );
  });
}
