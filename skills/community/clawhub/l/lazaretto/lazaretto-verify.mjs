/**
 * Lazaretto distribution skill (PRD §10) — free, minimal, auditable.
 *
 * This skill does NOTHING but (a) call the Lazaretto HTTPS API and (b) hash
 * local files. It never executes, imports, or shells out to any artifact, and it
 * touches no credentials beyond an optional API key you pass it (§8.3). It is
 * dependency-free (Node built-ins only) so it is trivial to audit.
 *
 * Core value (§10, closing the TOCTOU gap): after you install something a scan
 * reported on, re-hash what actually landed on disk and compare it to the
 * report's `target_hash`. If they differ, the thing you installed is NOT the
 * thing that was scanned — treat it as UNSCANNED.
 *
 * The `target_hash` algorithm is reproduced here EXACTLY as the server computes
 * it (docs/API.md, F5): order-independent sha256 over sorted per-file hashes.
 *
 * Usage:
 *   node lazaretto-verify.mjs lookup  <sha256> [--api <baseUrl>]
 *   node lazaretto-verify.mjs scan    <type> <ref|file> [--depth full|lookup] [--api <url>] [--key <apiKey>]
 *   node lazaretto-verify.mjs verify  <dir|file> <expected-target-hash>
 */
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';

const DEFAULT_API = process.env.LAZARETTO_API ?? 'https://lazaretto-api.fly.dev';
// Files never part of a scanned artifact; excluded so on-disk hashing matches
// what the scanner analyzed (archives already omit these).
const IGNORE = new Set(['.git', 'node_modules', '.DS_Store']);

export function sha256Hex(input) {
  return createHash('sha256').update(input).digest('hex');
}

/** EXACT server algorithm (src/analyzer/hash.ts, canonicalArtifactHash). */
export function canonicalArtifactHash(files) {
  if (files.length === 1) {
    return 'sha256:' + sha256Hex(Buffer.from(files[0].content, 'utf8'));
  }
  const lines = files
    .map((f) => `${f.path}\n${sha256Hex(Buffer.from(f.content, 'utf8'))}`)
    .sort();
  return 'sha256:' + sha256Hex(Buffer.from(lines.join('\n') + '\n', 'utf8'));
}

/** Recursively collect { path, content } for every file under `dir`. */
export function readTree(dir) {
  const out = [];
  const walk = (abs, rel) => {
    for (const name of readdirSync(abs)) {
      if (IGNORE.has(name)) continue;
      const childAbs = path.join(abs, name);
      const childRel = rel ? `${rel}/${name}` : name;
      const st = statSync(childAbs);
      if (st.isDirectory()) walk(childAbs, childRel);
      else if (st.isFile()) out.push({ path: childRel, content: readFileSync(childAbs, 'utf8') });
    }
  };
  walk(dir, '');
  return out;
}

/** Hash a path on disk (single file or directory) the way the server would. */
export function hashPath(target) {
  const st = statSync(target);
  if (st.isFile()) {
    return canonicalArtifactHash([{ path: path.basename(target), content: readFileSync(target, 'utf8') }]);
  }
  return canonicalArtifactHash(readTree(target));
}

/** §10 verification: does the on-disk artifact match the scanned target_hash? */
export function verifyInstalled(target, expectedTargetHash) {
  const actual = hashPath(target);
  const expected = expectedTargetHash.startsWith('sha256:') ? expectedTargetHash : `sha256:${expectedTargetHash}`;
  return {
    match: actual === expected,
    actual,
    expected,
    message:
      actual === expected
        ? 'OK: on-disk artifact matches the scanned target_hash.'
        : 'MISMATCH: the thing you installed is NOT the thing that was scanned — treat as UNSCANNED.',
  };
}

async function apiLookup(sha256, api) {
  const res = await fetch(`${api}/v1/known-bad/${encodeURIComponent(sha256)}`);
  return res.json();
}

async function apiScan(target, depth, api, key) {
  const headers = { 'content-type': 'application/json' };
  if (key) headers['x-api-key'] = key;
  const res = await fetch(`${api}/v1/scan`, { method: 'POST', headers, body: JSON.stringify({ target, depth }) });
  return { status: res.status, body: await res.json() };
}

async function main(argv) {
  const args = argv.slice(2);
  const cmd = args[0];
  const flag = (name, def) => {
    const i = args.indexOf(`--${name}`);
    return i !== -1 && args[i + 1] ? args[i + 1] : def;
  };
  const api = flag('api', DEFAULT_API);

  if (cmd === 'lookup') {
    const out = await apiLookup(args[1], api);
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
    process.exit(out.known_bad?.matched === true ? 2 : 0); // exit 2 => known-bad
  } else if (cmd === 'scan') {
    const type = args[1];
    const refOrFile = args[2];
    const target = type === 'inline' ? { type, content: readFileSync(refOrFile, 'utf8') } : { type, ref: refOrFile };
    const { status, body } = await apiScan(target, flag('depth', 'full'), api, flag('key'));
    process.stdout.write(JSON.stringify(body, null, 2) + '\n');
    process.exit(status === 200 && body.verdict !== 'malicious' ? 0 : 2);
  } else if (cmd === 'verify') {
    const result = verifyInstalled(args[1], args[2]);
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    process.exit(result.match ? 0 : 1); // §10: non-zero on mismatch
  } else {
    process.stderr.write('usage: lazaretto-verify <lookup|scan|verify> …\n');
    process.exit(64);
  }
}

// Run as CLI only when invoked directly (not when imported by tests).
if (import.meta.url === `file://${process.argv[1]}`) {
  main(process.argv).catch((e) => {
    process.stderr.write(`error: ${e.message}\n`);
    process.exit(1);
  });
}
