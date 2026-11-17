#!/usr/bin/env node
// Qualify one public original task by extracting the pinned correspondence client.
import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import {
  closeSync,
  constants,
  fsyncSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  openSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  unlinkSync,
  writeFileSync,
  writeSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, relative, resolve, sep } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import { gunzipSync } from "node:zlib";

const SCHEMA = "samedaydesk.original-task-qualification-skill.v1";
const CACHE_SCHEMA = "samedaydesk.original-task-qualification-cache.v1";
const COMMANDS = new Set(["acquire", "describe", "map", "submit", "read"]);
const PAYMENT_FLAGS = new Set(["--pay", "--settle", "--sign", "--wallet", "--purchase"]);
const DROPPED = new Set([
  "authorization",
  "bearer",
  "email",
  "password",
  "proof",
  "projectid",
  "registrationid",
  "secret",
  "token",
]);
const EXPECTED = {
  schema: "samedaydesk.original-task-qualification-pins.v1",
  origin: "https://samedaydesk.com",
  discoveryPath: "/discovery/original-task-correspondence.json",
  archivePath: "/for-agents/original-task/original-task-client.tar.gz",
  sha256: "9b5b9bf82119d7c8c0d4e277e34e85f6e9c0711ed4cfc84017c7a79b47bed887",
  bytes: 23811,
  basePath: "/api/correspondence",
  client: "server/lib/original-task/cli.mjs",
};
const OWNER_NAME = "cache-owner.json";
const ARCHIVE_NAME = "original-task-client.tar.gz";
const DISCOVERY_NAME = "discovery.json";
const SOURCE_NAME = "source.json";
const ALLOWED_FILES = new Set([OWNER_NAME, DISCOVERY_NAME, SOURCE_NAME, ARCHIVE_NAME]);
const IGNORED_ENTRY = "client";
const TEMP_PREFIX = "otq-141430-";
const GRACE_MS = 250;
const STDOUT_MAX = 1_000_000;
const STDERR_MAX = 64_000;

function blank(command) {
  return {
    schema: SCHEMA,
    command,
    acquisition: null,
    encounter: null,
    install: null,
    registration: null,
    submission: null,
    disposition: null,
    delivery: null,
    acceptance: null,
    payment: null,
    repeatUse: null,
    result: null,
    error: null,
  };
}

function emit(observation, code) {
  console.log(JSON.stringify(observation));
  if (code) process.exitCode = 1;
}

function fail(observation, code) {
  observation.error = { code };
  emit(observation, code);
}

function safeCode(value, fallback = "request_failed") {
  return typeof value === "string" && /^[a-z0-9_]{1,80}$/.test(value) ? value : fallback;
}

function flag(value) {
  if (value === true) return true;
  if (value === false) return false;
  return null;
}

function redact(value, depth = 0) {
  if (depth > 6) return null;
  if (typeof value === "string") {
    if (value.length > 8000) return "[redacted]";
    return value.replace(/Bearer\s+\S+/gi, "Bearer [redacted]");
  }
  if (!value || typeof value !== "object") return value;
  if (Array.isArray(value)) return value.slice(0, 50).map((item) => redact(item, depth + 1));
  const out = {};
  for (const [key, item] of Object.entries(value)) {
    if (DROPPED.has(key.toLowerCase())) continue;
    out[key] = redact(item, depth + 1);
  }
  return out;
}

function loadPins() {
  const file = fileURLToPath(new URL("../references/pins.json", import.meta.url));
  const info = lstatSync(file);
  if (!info.isFile() || info.size < 1 || info.size > 8192) {
    throw Object.assign(new Error("pins"), { code: "pins_refused" });
  }
  const pins = JSON.parse(readFileSync(file, "utf8"));
  const archive = pins?.archive;
  const discovery = pins?.discovery;
  if (pins?.schema !== EXPECTED.schema) throw Object.assign(new Error("pins"), { code: "pins_refused" });
  if (discovery?.origin !== EXPECTED.origin || discovery?.pathname !== EXPECTED.discoveryPath) {
    throw Object.assign(new Error("pins"), { code: "pins_refused" });
  }
  if (archive?.pathname !== EXPECTED.archivePath || archive?.sha256 !== EXPECTED.sha256 || archive?.bytes !== EXPECTED.bytes) {
    throw Object.assign(new Error("pins"), { code: "pins_refused" });
  }
  if (pins.basePath !== EXPECTED.basePath || pins.client !== EXPECTED.client) {
    throw Object.assign(new Error("pins"), { code: "pins_refused" });
  }
  return pins;
}

function skillRoot() {
  return realpathSync(fileURLToPath(new URL("..", import.meta.url)));
}

function nodeSupported() {
  const major = Number(process.versions.node.split(".")[0]);
  return major >= 22;
}

function flagsOf(rest) {
  const flags = new Map();
  for (let index = 0; index < rest.length; index += 2) {
    const key = rest[index];
    const value = rest[index + 1];
    if (typeof key !== "string" || !key.startsWith("--") || key.length > 40) return { error: "arguments_rejected" };
    if (typeof value !== "string" || value.startsWith("--") || value.length > 2048) return { error: "arguments_rejected" };
    if (flags.has(key)) return { error: "arguments_rejected" };
    flags.set(key, value);
  }
  return { flags };
}

function unknownFlag(flags, allowed) {
  for (const key of flags.keys()) {
    if (!allowed.includes(key)) return "arguments_rejected";
  }
  return null;
}

function timeoutOf(flags) {
  if (!flags.has("--timeout-ms")) return 20000;
  const value = flags.get("--timeout-ms");
  if (!/^[0-9]+$/.test(value)) return { error: "arguments_rejected" };
  const timeout = Number(value);
  if (!Number.isInteger(timeout) || timeout < 1000 || timeout > 60000) return { error: "arguments_rejected" };
  return timeout;
}

function loopback(hostname) {
  return hostname === "127.0.0.1" || hostname === "localhost";
}

function parseUrl(value) {
  try {
    const url = new URL(value);
    if (url.username || url.password || url.search || url.hash) return null;
    return url;
  } catch {
    return null;
  }
}

function allowedDiscovery(value) {
  const url = parseUrl(value);
  if (!url || url.pathname !== EXPECTED.discoveryPath) return null;
  if (url.origin === EXPECTED.origin && url.protocol === "https:") return url;
  if (url.protocol === "http:" && loopback(url.hostname)) return url;
  return null;
}

function allowedBase(value) {
  const url = parseUrl(value);
  if (!url || url.pathname !== EXPECTED.basePath) return null;
  if (url.origin === EXPECTED.origin && url.protocol === "https:") return url.href;
  if (url.protocol === "http:" && loopback(url.hostname)) return url.href;
  return null;
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function lstatSyncOrNull(file) {
  try { return lstatSync(file); }
  catch { return null; }
}

function regularFile(file) {
  const info = lstatSyncOrNull(file);
  return info?.isFile() ? info : null;
}

function existsPath(file) {
  return Boolean(lstatSyncOrNull(file));
}

function insideSkill(directory) {
  const root = skillRoot();
  const prefix = root.endsWith(sep) ? root : root + sep;
  return directory === root || directory.startsWith(prefix);
}

function outsideSkill(directory) {
  try { return !insideSkill(realpathSync(directory)); }
  catch { return false; }
}

function markerBytes() {
  return Buffer.from(`${JSON.stringify({ schema: CACHE_SCHEMA, package: "original-task-qualification" })}\n`);
}

function markerValid(cache) {
  const info = regularFile(join(cache, OWNER_NAME));
  if (!info || info.size > 512) return false;
  try {
    const parsed = JSON.parse(readFileSync(join(cache, OWNER_NAME), "utf8"));
    return parsed?.schema === CACHE_SCHEMA
      && parsed?.package === "original-task-qualification"
      && Object.keys(parsed).length === 2;
  } catch {
    return false;
  }
}

function cacheEntriesAccepted(cache) {
  let names;
  try { names = readdirSync(cache); }
  catch { return false; }
  for (const name of names) {
    if (name === IGNORED_ENTRY) continue;
    if (!ALLOWED_FILES.has(name)) return false;
    const info = lstatSyncOrNull(join(cache, name));
    if (!info?.isFile()) return false;
  }
  return true;
}

function writeOwnedFile(cache, name, bytes, mode) {
  if (!ALLOWED_FILES.has(name)) return { error: "cache_refused" };
  const dest = join(cache, name);
  let existing = lstatSyncOrNull(dest);
  if (existing?.isSymbolicLink()) {
    try { unlinkSync(dest); }
    catch { return { error: "cache_refused" }; }
    existing = null;
  } else if (existing && !existing.isFile()) {
    return { error: "cache_refused" };
  }
  const flags = existing
    ? constants.O_WRONLY | constants.O_TRUNC | constants.O_NOFOLLOW
    : constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY | constants.O_NOFOLLOW;
  let fd;
  try {
    fd = openSync(dest, flags, mode);
    writeSync(fd, bytes);
    fsyncSync(fd);
  } catch {
    return { error: "cache_refused" };
  } finally {
    if (fd !== undefined) closeSync(fd);
  }
  if (!regularFile(dest)) return { error: "cache_refused" };
  return null;
}

function prepareCache(cachePath) {
  if (!cachePath) return { error: "arguments_required" };
  const resolved = resolve(cachePath);
  const parent = dirname(resolved);
  const parentInfo = lstatSyncOrNull(parent);
  if (!parentInfo?.isDirectory()) return { error: "cache_refused" };
  let parentReal;
  try { parentReal = realpathSync(parent); }
  catch { return { error: "cache_refused" }; }
  const prospective = join(parentReal, basename(resolved));
  if (insideSkill(prospective)) return { error: "cache_refused" };
  if (!existsPath(resolved)) {
    mkdirSync(resolved, { mode: 0o700 });
    let cache;
    try { cache = realpathSync(resolved); }
    catch { return { error: "cache_refused" }; }
    if (cache !== prospective || insideSkill(cache)) return { error: "cache_refused" };
    const wrote = writeOwnedFile(cache, OWNER_NAME, markerBytes(), 0o644);
    if (wrote?.error) return wrote;
    return { cache };
  }
  const info = lstatSyncOrNull(resolved);
  if (!info?.isDirectory()) return { error: "cache_refused" };
  let cache;
  try { cache = realpathSync(resolved); }
  catch { return { error: "cache_refused" }; }
  if (insideSkill(cache)) return { error: "cache_refused" };
  if (!cacheEntriesAccepted(cache) || !markerValid(cache)) return { error: "cache_refused" };
  return { cache };
}

function discoveryMatchesPin(discovery) {
  const claimed = discovery?.acquisition?.archive;
  return Boolean(
    discovery
    && typeof discovery === "object"
    && !Array.isArray(discovery)
    && claimed?.sha256 === EXPECTED.sha256
    && claimed?.bytes === EXPECTED.bytes
    && claimed?.path === EXPECTED.archivePath,
  );
}

function parseJson(bytes) {
  try { return { ok: true, value: JSON.parse(bytes.toString("utf8")) }; }
  catch { return { malformed: true }; }
}

function pathInsideSkill(file) {
  const root = skillRoot();
  const prefix = root.endsWith(sep) ? root : root + sep;
  return file === root || file.startsWith(prefix);
}

function readRegularInside(rel, max) {
  const file = join(skillRoot(), rel);
  const info = lstatSyncOrNull(file);
  if (!info || !info.isFile() || info.size < 1 || info.size > max) return null;
  let real;
  try { real = realpathSync(file); }
  catch { return null; }
  if (!pathInsideSkill(real)) return null;
  try { return readFileSync(file); }
  catch { return null; }
}

function archiveMembers(gzipped) {
  let raw;
  try { raw = gunzipSync(gzipped, { maxOutputLength: 2_000_000 }); }
  catch { return null; }
  const members = new Map();
  let offset = 0;
  while (offset + 512 <= raw.length) {
    const header = raw.subarray(offset, offset + 512);
    if (header.every((byte) => byte === 0)) break;
    const name = header.toString("utf8", 0, 100).replace(/\0.*$/, "");
    const prefix = header.toString("utf8", 345, 500).replace(/\0.*$/, "");
    const member = prefix ? `${prefix}/${name}` : name;
    const size = Number.parseInt(header.toString("utf8", 124, 136).replace(/\0.*$/, "").trim(), 8);
    const typeflag = header[156];
    if (!member || !Number.isInteger(size) || size < 0 || size > 1_000_000) return null;
    if (member.startsWith("/") || member.split("/").includes("..") || member.includes("\\")) return null;
    if (typeflag !== 48 && typeflag !== 0) return null;
    const start = offset + 512;
    const end = start + size;
    if (end > raw.length) return null;
    if (members.has(member)) return null;
    members.set(member, Buffer.from(raw.subarray(start, end)));
    offset = start + (Math.ceil(size / 512) * 512);
  }
  if (!members.has(EXPECTED.client)) return null;
  return members;
}

function sourceMatchesArchive(sourceRoot, members) {
  const listed = lstatSyncOrNull(sourceRoot);
  if (!listed?.isDirectory()) return false;
  let base;
  try { base = realpathSync(sourceRoot); }
  catch { return false; }
  if (!pathInsideSkill(base)) return false;
  const seen = new Set();
  const pending = [base];
  while (pending.length) {
    const current = pending.pop();
    let names;
    try { names = readdirSync(current); }
    catch { return false; }
    for (const name of names) {
      const full = join(current, name);
      const entry = lstatSyncOrNull(full);
      if (!entry || entry.isSymbolicLink()) return false;
      if (entry.isDirectory()) {
        pending.push(full);
        continue;
      }
      if (!entry.isFile()) return false;
      let real;
      try { real = realpathSync(full); }
      catch { return false; }
      if (!pathInsideSkill(real)) return false;
      const rel = relative(base, full).split(sep).join("/");
      const body = members.get(rel);
      if (!body || body.length !== entry.size || !readFileSync(full).equals(body)) return false;
      seen.add(rel);
    }
  }
  for (const name of members.keys()) {
    if (!seen.has(name)) return false;
  }
  return true;
}

function loadIncluded() {
  const archiveBytes = readRegularInside(join("client", ARCHIVE_NAME), EXPECTED.bytes);
  if (!archiveBytes || archiveBytes.length !== EXPECTED.bytes || sha256(archiveBytes) !== EXPECTED.sha256) {
    return { error: "archive_refused" };
  }
  const members = archiveMembers(archiveBytes);
  if (!members) return { error: "archive_refused" };
  const sourceRoot = join(skillRoot(), "client", "source");
  if (!sourceMatchesArchive(sourceRoot, members)) return { error: "source_refused" };
  const discoveryBytes = readRegularInside(join("client", "included-discovery.json"), 262144);
  if (!discoveryBytes) return { error: "source_refused" };
  const parsed = parseJson(discoveryBytes);
  if (!parsed.ok || !discoveryMatchesPin(parsed.value)) return { error: "source_refused" };
  return { archiveBytes, discoveryBytes, discovery: parsed.value };
}

function containedExtract(clientRoot) {
  const base = realpathSync(clientRoot);
  const pending = [base];
  while (pending.length) {
    const current = pending.pop();
    for (const name of readdirSync(current)) {
      const full = join(current, name);
      const info = lstatSync(full);
      if (info.isSymbolicLink()) return false;
      if (info.isDirectory()) pending.push(full);
      else if (!info.isFile()) return false;
    }
  }
  const cli = realpathSync(join(clientRoot, EXPECTED.client));
  const prefix = base.endsWith(sep) ? base : base + sep;
  return cli.startsWith(prefix);
}

function minimalEnv() {
  return {
    PATH: process.env.PATH || "",
    HOME: process.env.HOME || "",
    TMPDIR: process.env.TMPDIR || tmpdir(),
    LANG: "C.UTF-8",
  };
}

function takeBytes(current, chunk, max) {
  if (current.length >= max) return current;
  const room = max - current.length;
  const piece = chunk.length > room ? chunk.subarray(0, room) : chunk;
  return piece.length ? Buffer.concat([current, piece]) : current;
}

export async function runOwnedChild(command, args, options) {
  const timeoutMs = options.timeoutMs;
  const maxStdout = options.maxStdout ?? STDOUT_MAX;
  const maxStderr = options.maxStderr ?? STDERR_MAX;
  const graceMs = options.graceMs ?? GRACE_MS;
  let child;
  try {
    child = spawn(command, args, {
      cwd: options.cwd,
      env: options.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
  } catch {
    return { error: "client_failed", gone: true, code: null, signal: null, stdout: "", stderr: "" };
  }
  let stdout = Buffer.alloc(0);
  let stderr = Buffer.alloc(0);
  let error = null;
  let timer = null;
  let killTimer = null;
  let finished = false;
  const onAbort = () => beginKill("client_cancelled");

  function stopTimers() {
    if (timer) clearTimeout(timer);
    if (killTimer) clearTimeout(killTimer);
    timer = null;
    killTimer = null;
    options.signal?.removeEventListener("abort", onAbort);
  }

  function beginKill(reason) {
    if (error === null) error = reason;
    try { child.stdout.destroy(); } catch { /* already closed */ }
    try { child.stderr.destroy(); } catch { /* already closed */ }
    try { child.kill("SIGTERM"); } catch { /* already exited */ }
    if (!killTimer) {
      killTimer = setTimeout(() => {
        try { child.kill("SIGKILL"); } catch { /* already exited */ }
      }, graceMs);
    }
  }

  return new Promise((resolvePromise) => {
    function finish(code, signal) {
      if (finished) return;
      finished = true;
      stopTimers();
      const pid = child.pid;
      let gone = true;
      if (pid) {
        try {
          process.kill(pid, 0);
          gone = false;
        } catch (err) {
          gone = err?.code === "ESRCH";
        }
      }
      if (!gone) {
        try { process.kill(pid, "SIGKILL"); } catch { /* already exited */ }
        resolvePromise({ error: error || "client_timeout", code, signal, gone: false, stdout: "", stderr: "" });
        return;
      }
      if (error) {
        resolvePromise({ error, code, signal, gone: true, stdout: "", stderr: "" });
        return;
      }
      resolvePromise({
        code,
        signal,
        gone: true,
        stdout: stdout.toString("utf8"),
        stderr: stderr.toString("utf8"),
      });
    }

    timer = setTimeout(() => beginKill("client_timeout"), timeoutMs);
    if (options.signal) {
      if (options.signal.aborted) beginKill("client_cancelled");
      else options.signal.addEventListener("abort", onAbort, { once: true });
    }
    child.stdout.on("data", (chunk) => {
      const buf = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      const overflow = stdout.length + buf.length > maxStdout;
      stdout = takeBytes(stdout, buf, maxStdout);
      if (overflow) beginKill("client_output");
    });
    child.stderr.on("data", (chunk) => {
      const buf = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      const overflow = stderr.length + buf.length > maxStderr;
      stderr = takeBytes(stderr, buf, maxStderr);
      if (overflow) beginKill("client_output");
    });
    child.once("error", () => {
      if (error === null) error = "client_failed";
      finish(null, null);
    });
    child.once("exit", (code, signal) => finish(code, signal));
  });
}

function removeOwnedTemp(directory, identity) {
  let current;
  try { current = realpathSync(directory); }
  catch { return; }
  const info = lstatSyncOrNull(current);
  if (!info?.isDirectory() || info.dev !== identity.dev || info.ino !== identity.ino) return;
  let root;
  try { root = realpathSync(tmpdir()); }
  catch { return; }
  const prefix = root.endsWith(sep) ? root : root + sep;
  if (!current.startsWith(prefix)) return;
  const rest = current.slice(prefix.length);
  if (rest.includes(sep) || !rest.startsWith(TEMP_PREFIX)) return;
  rmSync(current, { recursive: true, force: true });
}

async function withVerifiedExtract(archiveBytes, discoveryBytes, timeoutMs, fn) {
  if (!Buffer.isBuffer(archiveBytes) || archiveBytes.length !== EXPECTED.bytes || sha256(archiveBytes) !== EXPECTED.sha256 || !inspectTar(archiveBytes).ok) {
    return { error: "archive_refused" };
  }
  let root;
  try { root = realpathSync(tmpdir()); }
  catch { return { error: "archive_refused" }; }
  const directory = mkdtempSync(join(root, TEMP_PREFIX));
  const created = lstatSync(directory);
  const identity = { dev: created.dev, ino: created.ino };
  try {
    let real;
    try { real = realpathSync(directory); }
    catch { return { error: "archive_refused" }; }
    if (real !== directory || !created.isDirectory()) return { error: "archive_refused" };
    const clientRoot = join(directory, "client");
    mkdirSync(clientRoot, { mode: 0o700 });
    const archivePath = join(directory, ARCHIVE_NAME);
    writeFileSync(archivePath, archiveBytes, { mode: 0o644 });
    const discoveryPath = join(directory, DISCOVERY_NAME);
    if (discoveryBytes) writeFileSync(discoveryPath, discoveryBytes, { mode: 0o644 });
    const extracted = await runOwnedChild("tar", ["-xzf", archivePath, "-C", clientRoot], {
      cwd: directory,
      env: minimalEnv(),
      timeoutMs,
      maxStdout: 1024,
      maxStderr: 8192,
    });
    if (extracted.error === "client_failed") return { error: "tar_required" };
    if (extracted.error === "client_timeout" || extracted.error === "client_cancelled") return { error: "extract_timeout" };
    if (extracted.error || extracted.code !== 0) return { error: "archive_refused" };
    if (!containedExtract(clientRoot)) return { error: "archive_refused" };
    return await fn({ clientRoot, archivePath, discoveryPath });
  } catch {
    return { error: "archive_refused" };
  } finally {
    removeOwnedTemp(directory, identity);
  }
}

function inspectTar(gzipped) {
  return { ok: Boolean(archiveMembers(gzipped)) };
}

async function readLimited(response, maxBytes) {
  if (!response.body) return { ok: true, bytes: Buffer.alloc(0) };
  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;
  while (true) {
    const step = await reader.read();
    if (step.done) break;
    total += step.value.byteLength;
    if (total > maxBytes) {
      await reader.cancel();
      return { ok: false, error: "oversized" };
    }
    chunks.push(Buffer.from(step.value));
  }
  return { ok: true, bytes: Buffer.concat(chunks) };
}

async function fetchBytes(url, maxBytes, timeoutMs) {
  let response;
  try {
    response = await fetch(url, {
      redirect: "manual",
      headers: { accept: "application/octet-stream, application/json" },
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch {
    return { error: "unavailable" };
  }
  if (response.status >= 300 && response.status < 400) {
    await response.body?.cancel();
    return { error: "redirect_refused" };
  }
  if (response.status !== 200) {
    await response.body?.cancel();
    return { error: "unavailable" };
  }
  try {
    const body = await readLimited(response, maxBytes);
    if (!body.ok) return { error: "oversized" };
    return { ok: true, bytes: body.bytes };
  } catch {
    return { error: "unavailable" };
  }
}

function registrationCode(directory) {
  if (!directory) return null;
  const info = regularFile(join(directory, "registration.secret"));
  if (!info || info.size < 32 || info.size > 200) return "absent";
  return "present";
}

function continuationPresent(directory) {
  const info = regularFile(join(directory, "continuation.json"));
  return Boolean(info && info.size > 1 && info.size <= 65536);
}

function taskFileOk(file) {
  const info = regularFile(file);
  return Boolean(info && info.size > 1 && info.size <= 65536);
}

function sameOrNested(parent, child) {
  if (parent === child) return true;
  const prefix = parent.endsWith(sep) ? parent : parent + sep;
  return child.startsWith(prefix);
}

function realpathOrNull(file) {
  try { return realpathSync(file); }
  catch { return null; }
}

function pathsOverlap(cachePath, privatePath) {
  if (!cachePath || !privatePath) return false;
  const cacheResolved = resolve(cachePath);
  const privateResolved = resolve(privatePath);
  if (sameOrNested(cacheResolved, privateResolved) || sameOrNested(privateResolved, cacheResolved)) return true;
  const cacheReal = realpathOrNull(cacheResolved);
  const privateReal = realpathOrNull(privateResolved);
  if (cacheReal && privateReal && (sameOrNested(cacheReal, privateReal) || sameOrNested(privateReal, cacheReal))) return true;
  return false;
}

function applyIncluded(observation, discovery) {
  observation.acquisition = {
    source: "included",
    sha256: EXPECTED.sha256,
    bytes: EXPECTED.bytes,
    matched: true,
    fetched: false,
  };
  observation.encounter = {
    descriptorUrl: null,
    schema: typeof discovery?.schema === "string" ? discovery.schema : null,
  };
}

function liveRefused(discovery) {
  return discovery?.schema !== "samedaydesk.original-task-correspondence.v1"
    || discovery.deliveryPromise !== false
    || discovery.payment !== false
    || discovery.acceptance !== false
    || discovery.thisDescriptorPerformsNoRequest !== true;
}

async function openIncluded(observation, flags) {
  const prepared = prepareCache(flags.get("--cache"));
  if (prepared.error) return prepared.error;
  const included = loadIncluded();
  if (included.error) return included.error;
  applyIncluded(observation, included.discovery);
  return { cache: prepared.cache, ...included };
}

async function readLiveDescriptor(observation, cache, discoveryUrl, timeoutMs) {
  observation.acquisition = null;
  observation.encounter = { descriptorUrl: discoveryUrl.href, schema: null };
  const fetched = await fetchBytes(discoveryUrl, 262144, timeoutMs);
  if (fetched.error === "redirect_refused") return "redirect_refused";
  if (fetched.error) return "descriptor_unavailable";
  let discovery;
  try { discovery = JSON.parse(fetched.bytes.toString("utf8")); }
  catch { return "descriptor_unavailable"; }
  if (!discovery || typeof discovery !== "object" || Array.isArray(discovery)) return "descriptor_unavailable";
  observation.encounter.schema = typeof discovery.schema === "string" ? discovery.schema : null;
  const claimed = discovery.acquisition?.archive;
  if (!discoveryMatchesPin(discovery)) {
    observation.acquisition = {
      source: "included",
      sha256: typeof claimed?.sha256 === "string" ? claimed.sha256 : null,
      bytes: Number.isInteger(claimed?.bytes) ? claimed.bytes : null,
      matched: false,
      fetched: false,
    };
    return "stale_discovery";
  }
  const wroteDiscovery = writeOwnedFile(cache, DISCOVERY_NAME, fetched.bytes, 0o644);
  if (wroteDiscovery?.error) return wroteDiscovery.error;
  const wroteSource = writeOwnedFile(cache, SOURCE_NAME, Buffer.from(`${JSON.stringify({ descriptorUrl: discoveryUrl.href })}\n`), 0o644);
  if (wroteSource?.error) return wroteSource.error;
  observation.acquisition = {
    source: "included",
    sha256: EXPECTED.sha256,
    bytes: EXPECTED.bytes,
    matched: true,
    fetched: false,
  };
  return { discovery, discoveryBytes: fetched.bytes };
}

function applyDecision(observation, parsed) {
  observation.result = redact(parsed);
  observation.disposition = {
    action: typeof parsed.action === "string" ? parsed.action : null,
    code: typeof parsed.code === "string" ? parsed.code : null,
  };
  observation.delivery = { delivered: null, promised: flag(parsed.deliveryPromise) };
  observation.acceptance = { accepted: flag(parsed.acceptance) };
  observation.payment = { payment: flag(parsed.payment) };
}

function applyReceipt(observation, parsed) {
  observation.result = redact(parsed);
  observation.disposition = {
    stage: typeof parsed.stage === "string" ? parsed.stage : null,
    disposition: typeof parsed.disposition === "string" ? parsed.disposition : null,
  };
  observation.delivery = { delivered: flag(parsed.delivered), promised: flag(parsed.deliveryPromise) };
  observation.acceptance = { accepted: flag(parsed.accepted) };
  observation.payment = { payment: flag(parsed.payment) };
  observation.submission = { submitted: flag(parsed.submitted), intentional: true };
}

function applyDescriptor(observation, parsed) {
  observation.result = redact(parsed);
  observation.delivery = { delivered: null, promised: flag(parsed.deliveryPromise) };
  observation.acceptance = { accepted: flag(parsed.acceptance) };
  observation.payment = { payment: flag(parsed.payment) };
}

function runClient(clientRoot, args, timeoutMs) {
  return runOwnedChild(process.execPath, [join(clientRoot, EXPECTED.client), ...args], {
    cwd: clientRoot,
    env: minimalEnv(),
    timeoutMs,
    maxStdout: STDOUT_MAX,
    maxStderr: STDERR_MAX,
  });
}

function parseClient(result) {
  if (!result || result.error) return { error: result?.error || "client_failed" };
  if (result.code === 0) {
    try {
      const parsed = JSON.parse(result.stdout.trim());
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return { error: "client_output" };
      return { parsed };
    } catch {
      return { error: "client_output" };
    }
  }
  try {
    const parsed = JSON.parse(result.stderr.trim());
    return { error: safeCode(parsed?.error?.code) };
  } catch {
    return { error: "request_failed" };
  }
}

function discoveryUrlOf(flags, { required }) {
  if (!flags.has("--discovery-url")) return required ? `${EXPECTED.origin}${EXPECTED.discoveryPath}` : null;
  return flags.get("--discovery-url");
}

async function proveExtract(observation, ensured, timeoutMs) {
  const proved = await withVerifiedExtract(ensured.archiveBytes, ensured.discoveryBytes, timeoutMs, async () => ({ ok: true }));
  if (!proved?.ok) return proved?.error || "archive_refused";
  observation.install = { clientExtracted: true, client: EXPECTED.client };
  return null;
}

async function commandAcquire(observation, flags, timeoutMs) {
  const rejected = unknownFlag(flags, ["--cache", "--discovery-url", "--timeout-ms", "--refresh"]);
  if (rejected) return fail(observation, rejected);
  const opened = await openIncluded(observation, flags);
  if (typeof opened === "string") return fail(observation, opened);
  const discoveryUrl = allowedDiscovery(discoveryUrlOf(flags, { required: true }));
  if (!discoveryUrl) return fail(observation, "origin_refused");
  const live = await readLiveDescriptor(observation, opened.cache, discoveryUrl, timeoutMs);
  if (typeof live === "string") return fail(observation, live);
  const failed = await proveExtract(observation, opened, timeoutMs);
  if (failed) return fail(observation, failed);
  emit(observation);
}

async function commandDescribe(observation, flags, timeoutMs) {
  const rejected = unknownFlag(flags, ["--cache", "--discovery-url", "--timeout-ms", "--refresh"]);
  if (rejected) return fail(observation, rejected);
  const opened = await openIncluded(observation, flags);
  if (typeof opened === "string") return fail(observation, opened);
  const ran = await withVerifiedExtract(opened.archiveBytes, opened.discoveryBytes, timeoutMs, (paths) => {
    observation.install = { clientExtracted: true, client: EXPECTED.client };
    return runClient(paths.clientRoot, ["describe"], timeoutMs);
  });
  const parsed = parseClient(ran);
  if (parsed.error) return fail(observation, parsed.error);
  applyDescriptor(observation, parsed.parsed);
  emit(observation);
}

async function commandMap(observation, flags, timeoutMs) {
  const rejected = unknownFlag(flags, ["--cache", "--discovery-url", "--timeout-ms", "--refresh", "--task-file", "--directory", "--handle"]);
  if (rejected) return fail(observation, rejected);
  const taskFile = flags.get("--task-file");
  if (!taskFile || !taskFileOk(taskFile)) return fail(observation, "arguments_required");
  if (flags.has("--directory")) {
    const directory = flags.get("--directory");
    if (pathsOverlap(flags.get("--cache"), directory)) return fail(observation, "cache_private_overlap");
    if (existsPath(directory) && !outsideSkill(directory)) return fail(observation, "arguments_rejected");
  }
  const opened = await openIncluded(observation, flags);
  if (typeof opened === "string") return fail(observation, opened);
  let discoveryBytes = opened.discoveryBytes;
  const requested = discoveryUrlOf(flags, { required: false });
  if (requested) {
    const discoveryUrl = allowedDiscovery(requested);
    if (!discoveryUrl) return fail(observation, "origin_refused");
    const live = await readLiveDescriptor(observation, opened.cache, discoveryUrl, timeoutMs);
    if (typeof live === "string") return fail(observation, live);
    discoveryBytes = live.discoveryBytes;
  }
  const ran = await withVerifiedExtract(opened.archiveBytes, discoveryBytes, timeoutMs, (paths) => {
    observation.install = { clientExtracted: true, client: EXPECTED.client };
    const args = ["map", "--discovery-file", paths.discoveryPath, "--archive", paths.archivePath, "--task-file", taskFile];
    if (flags.has("--directory")) args.push("--directory", flags.get("--directory"));
    if (flags.has("--handle")) args.push("--handle", flags.get("--handle"));
    return runClient(paths.clientRoot, args, timeoutMs);
  });
  const parsed = parseClient(ran);
  if (parsed.error) return fail(observation, parsed.error);
  applyDecision(observation, parsed.parsed);
  if (flags.has("--directory")) observation.registration = { code: registrationCode(flags.get("--directory")) };
  emit(observation);
}

async function commandSubmit(observation, flags, timeoutMs) {
  const rejected = unknownFlag(flags, ["--cache", "--discovery-url", "--timeout-ms", "--refresh", "--task-file", "--directory", "--base-url", "--submit"]);
  if (rejected) return fail(observation, rejected);
  if (flags.get("--submit") !== "yes") return fail(observation, "submission_required");
  const taskFile = flags.get("--task-file");
  const directory = flags.get("--directory");
  const base = allowedBase(flags.get("--base-url") || "");
  if (!taskFile || !taskFileOk(taskFile) || !directory || !base) return fail(observation, !base && flags.has("--base-url") ? "origin_refused" : "arguments_required");
  if (pathsOverlap(flags.get("--cache"), directory)) return fail(observation, "cache_private_overlap");
  const directoryInfo = lstatSyncOrNull(directory);
  if (!directoryInfo?.isDirectory()) {
    return fail(observation, directoryInfo?.isSymbolicLink() ? "missing_private_authority" : "arguments_required");
  }
  if (!outsideSkill(directory)) return fail(observation, "arguments_rejected");
  const opened = await openIncluded(observation, flags);
  if (typeof opened === "string") return fail(observation, opened);
  const requested = discoveryUrlOf(flags, { required: false });
  if (requested) {
    const discoveryUrl = allowedDiscovery(requested);
    if (!discoveryUrl) return fail(observation, "origin_refused");
    const live = await readLiveDescriptor(observation, opened.cache, discoveryUrl, timeoutMs);
    if (typeof live === "string") return fail(observation, live);
    if (liveRefused(live.discovery)) return fail(observation, "stale_discovery");
  }
  const ran = await withVerifiedExtract(opened.archiveBytes, opened.discoveryBytes, timeoutMs, (paths) => {
    observation.install = { clientExtracted: true, client: EXPECTED.client };
    return runClient(paths.clientRoot, [
      "submit",
      "--base-url", base,
      "--directory", directory,
      "--task-file", taskFile,
    ], timeoutMs);
  });
  const parsed = parseClient(ran);
  observation.registration = { code: registrationCode(directory) };
  if (parsed.error) return fail(observation, parsed.error);
  applyReceipt(observation, parsed.parsed);
  emit(observation);
}

async function commandRead(observation, flags, timeoutMs) {
  const rejected = unknownFlag(flags, ["--cache", "--timeout-ms", "--directory"]);
  if (rejected) return fail(observation, rejected);
  const directory = flags.get("--directory");
  if (!directory) return fail(observation, "arguments_required");
  if (pathsOverlap(flags.get("--cache"), directory)) return fail(observation, "cache_private_overlap");
  const directoryInfo = lstatSyncOrNull(directory);
  if (directoryInfo?.isSymbolicLink()) return fail(observation, "missing_private_authority");
  if (directoryInfo && !outsideSkill(directory)) return fail(observation, "arguments_rejected");
  const repeat = continuationPresent(directory);
  const opened = await openIncluded(observation, flags);
  if (typeof opened === "string") return fail(observation, opened);
  const ran = await withVerifiedExtract(opened.archiveBytes, opened.discoveryBytes, timeoutMs, (paths) => {
    observation.install = { clientExtracted: true, client: EXPECTED.client };
    return runClient(paths.clientRoot, ["read", "--directory", directory], timeoutMs);
  });
  const parsed = parseClient(ran);
  observation.registration = { code: registrationCode(directory) };
  if (repeat) {
    observation.repeatUse = {
      kind: "local_continuation_retrieval",
      acceptedUsefulJob: false,
      customerDemand: false,
    };
  }
  if (parsed.error) return fail(observation, parsed.error);
  applyReceipt(observation, parsed.parsed);
  observation.submission = null;
  emit(observation);
}

async function main() {
  const argv = process.argv.slice(2);
  const [command = "unknown", ...rest] = argv;
  const observation = blank(COMMANDS.has(command) ? command : "unknown");
  if (argv.some((arg) => PAYMENT_FLAGS.has(arg))) return fail(observation, "payment_refused");
  if (!nodeSupported()) return fail(observation, "runtime_refused");
  if (!COMMANDS.has(command)) return fail(observation, "invalid_command");
  let pins;
  try { pins = loadPins(); }
  catch (error) { return fail(observation, safeCode(error?.code, "pins_refused")); }
  if (!pins) return fail(observation, "pins_refused");
  const parsed = flagsOf(rest);
  if (parsed.error) return fail(observation, parsed.error);
  // Bind caller paths before the client runs from its invocation-owned extract.
  for (const key of ["--cache", "--task-file", "--directory"]) {
    if (parsed.flags.has(key)) {
      parsed.flags.set(key, resolve(parsed.flags.get(key)));
    }
  }
  const timeout = timeoutOf(parsed.flags);
  if (timeout?.error) return fail(observation, timeout.error);
  if (command === "acquire") return commandAcquire(observation, parsed.flags, timeout);
  if (command === "describe") return commandDescribe(observation, parsed.flags, timeout);
  if (command === "map") return commandMap(observation, parsed.flags, timeout);
  if (command === "submit") return commandSubmit(observation, parsed.flags, timeout);
  return commandRead(observation, parsed.flags, timeout);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(() => {
    const observation = blank("unknown");
    fail(observation, "request_failed");
  });
}
