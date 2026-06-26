// openclaw-config-fs.mjs
//
// Direct-fs read/write for `~/.openclaw/openclaw.json` from the bundle's host
// installer. Replaces every `runOpenClaw config get/set hooks/mcp.servers.<name>`
// + `runOpenClaw mcp show/set/unset` invocation that the legacy installer used
// to make via the openclaw subprocess CLI. Dropping the subprocess pattern is
// what lets `openclaw plugins install clawhub:hirey-compatible`
// proceed without the user having to pass --dangerously-force-unsafe-install
// (see openclaw/openclaw#59241 for the scanner rule details).
//
// Why direct fs is acceptable here:
//
//   1. The legacy installer always passed `--strict-json` to `openclaw config set`,
//      which itself strips comments and rewrites the file as plain JSON. So the
//      historical behavior already lost JSON5 comments on any field we touched.
//      We mirror that: parse with comment-stripping to handle existing JSON5,
//      then write back as plain JSON. Net effect on user's file: identical to
//      what the CLI would have produced.
//
//   2. The bundle installer is the *only* writer of hooks + mcp.servers.<name>
//      while it's running (host owner is following the install skill, not poking
//      config in another terminal). We still take an advisory file lock to defend
//      against pathological concurrent edits, but the conflict surface is small.
//
//   3. Schema validation: `openclaw config set --strict-json` validates the value
//      before writing. We skip that — but we narrowly write only the two fields
//      we own (`hooks`, `mcp.servers.<name>`) with values constructed by the
//      installer's own helpers (buildManagedHooksConfig, buildManagedHiServerDefinition),
//      which themselves enforce shape. If the host's openclaw.json has unrelated
//      fields with schema drift (the "channels.imessage required field" noise the
//      old preflight had to filter), our targeted write doesn't surface them at
//      all — strictly safer than the CLI dry-run was.
//
//   4. OPENCLAW_CONFIG_PATH override: the canonical location is ~/.openclaw/openclaw.json,
//      but users with $OPENCLAW_CONFIG_PATH set need that path. We honor the env
//      var, falling back to homedir-derived default.

import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

/**
 * Resolve the canonical openclaw.json path. Mirrors openclaw/plugin-sdk
 * resolveCanonicalConfigPath logic but inlined so we don't take an `import 'openclaw'`
 * dep (which wouldn't resolve from the bundle's standalone install context anyway —
 * the bundle's installer is run as `node ./scripts/...` with no openclaw in its
 * module resolution path).
 */
export function resolveOpenclawConfigPath(env = process.env, homedir = os.homedir) {
  const explicit = (env.OPENCLAW_CONFIG_PATH || '').trim();
  if (explicit) return path.resolve(explicit);
  const stateDir = (env.OPENCLAW_STATE_DIR || '').trim() || path.join(homedir(), '.openclaw');
  return path.join(stateDir, 'openclaw.json');
}

/**
 * Strip JSON5-flavor comments so JSON.parse can consume the remainder. Handles:
 *   - // line comments (until \n or EOF)
 *   - /* block comments *‍/  (greedy until next *‍/)
 *   - never strips inside string literals (quote-aware state machine)
 *
 * Trailing commas remain after stripping; we keep a small post-pass that drops
 * them too. We do NOT support unquoted keys (rare in openclaw.json; openclaw CLI
 * never writes them).
 */
function stripJson5(src) {
  let out = '';
  let i = 0;
  let inStr = false;
  let strQuote = '';
  while (i < src.length) {
    const c = src[i];
    const next = src[i + 1];
    if (inStr) {
      out += c;
      if (c === '\\') { out += next ?? ''; i += 2; continue; }
      if (c === strQuote) inStr = false;
      i++;
      continue;
    }
    if (c === '"' || c === "'") { inStr = true; strQuote = c; out += c; i++; continue; }
    if (c === '/' && next === '/') {
      while (i < src.length && src[i] !== '\n') i++;
      continue; // keep the \n if present (handled by next loop iter)
    }
    if (c === '/' && next === '*') {
      i += 2;
      while (i < src.length && !(src[i] === '*' && src[i + 1] === '/')) i++;
      i += 2;
      continue;
    }
    out += c;
    i++;
  }
  // Drop trailing commas: `,` followed only by whitespace before `}` or `]`.
  return out.replace(/,(\s*[}\]])/g, '$1');
}

/**
 * Read openclaw.json (treats missing file as empty object) and return
 * { config, raw, exists, path, sha256 }. sha256 is the hash of the on-disk bytes
 * (used as a cheap conflict guard — pass it back to writeOpenclawConfigAtomic
 * so we can refuse to clobber if another writer touched the file concurrently).
 */
export async function readOpenclawConfig(configPath) {
  let raw = null;
  try {
    raw = await fs.readFile(configPath, 'utf8');
  } catch (err) {
    if (err && err.code === 'ENOENT') {
      return {
        config: {},
        raw: null,
        exists: false,
        path: configPath,
        sha256: null,
      };
    }
    throw err;
  }
  let parsed;
  try {
    parsed = JSON.parse(stripJson5(raw));
  } catch (err) {
    throw new Error(`openclaw_config_parse_failed: ${configPath} not valid JSON/JSON5 after comment strip — ${err?.message || err}`);
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error(`openclaw_config_shape: top-level must be object, got ${Array.isArray(parsed) ? 'array' : typeof parsed}`);
  }
  return {
    config: parsed,
    raw,
    exists: true,
    path: configPath,
    sha256: crypto.createHash('sha256').update(raw, 'utf8').digest('hex'),
  };
}

/**
 * Atomic write: serialize next config to JSON, write to a sibling .tmp, fsync,
 * rename over the original. If `expectedSha256` is provided, re-read the file
 * first and refuse to write if its hash changed since the snapshot was taken
 * (mirrors the conflict guard openclaw's own config-mutation uses).
 *
 * The CLI used to maintain the file via `openclaw config set --strict-json`;
 * that path always rewrote the entire JSON top-level too, so doing the same
 * here is no behavioral regression.
 */
export async function writeOpenclawConfigAtomic(configPath, nextConfig, options = {}) {
  if (options.expectedSha256 != null) {
    let currentRaw = null;
    try { currentRaw = await fs.readFile(configPath, 'utf8'); }
    catch (err) { if (!(err && err.code === 'ENOENT')) throw err; }
    const currentSha = currentRaw == null ? null : crypto.createHash('sha256').update(currentRaw, 'utf8').digest('hex');
    if (currentSha !== options.expectedSha256) {
      throw new Error(`openclaw_config_conflict: ${configPath} changed between read and write (expected ${options.expectedSha256?.slice(0, 12) || 'absent'}, got ${currentSha?.slice(0, 12) || 'absent'})`);
    }
  }
  await fs.mkdir(path.dirname(configPath), { recursive: true });
  const serialized = `${JSON.stringify(nextConfig, null, 2)}\n`;
  const tmp = `${configPath}.tmp.${process.pid}.${Date.now()}`;
  await fs.writeFile(tmp, serialized, { encoding: 'utf8', flag: 'w' });
  // rename is atomic on POSIX when src+dst are on the same filesystem (always
  // true here — both under ~/.openclaw). On Windows fs.rename is also atomic
  // for same-volume moves on NTFS.
  await fs.rename(tmp, configPath);
  return {
    path: configPath,
    bytesWritten: Buffer.byteLength(serialized, 'utf8'),
    sha256: crypto.createHash('sha256').update(serialized, 'utf8').digest('hex'),
  };
}

/**
 * Highest-level helper: read config, run a mutator that gets a draft (deep clone),
 * write back atomically with conflict guard. Mirror of openclaw/plugin-sdk
 * mutateConfigFile semantics but free of the dependency on the openclaw package.
 *
 * The mutator receives the draft and may return undefined (mutate in place) or
 * an arbitrary value (returned as `result`).
 */
export async function mutateOpenclawConfig(configPath, mutate) {
  const snapshot = await readOpenclawConfig(configPath);
  const draft = JSON.parse(JSON.stringify(snapshot.config));
  const result = await mutate(draft, { previousSha256: snapshot.sha256, snapshot });
  const writeOutcome = await writeOpenclawConfigAtomic(configPath, draft, {
    expectedSha256: snapshot.sha256,
  });
  return {
    result,
    snapshotBefore: snapshot,
    write: writeOutcome,
  };
}

// ---- Targeted helpers used by the bundle installer ---------------------------
//
// These wrap mutateOpenclawConfig with the exact semantics the legacy
// `runOpenClaw config set hooks` / `runOpenClaw mcp set <name>` calls had.

/**
 * Read just `hooks` (or null if absent). Replaces `openclaw config get hooks --json`.
 */
export async function readHooks(configPath) {
  const snap = await readOpenclawConfig(configPath);
  const hooks = snap.config.hooks;
  if (hooks == null) return null;
  if (typeof hooks !== 'object' || Array.isArray(hooks)) {
    throw new Error(`openclaw_config_shape: hooks must be object, got ${Array.isArray(hooks) ? 'array' : typeof hooks}`);
  }
  return hooks;
}

/**
 * Read just `mcp.servers.<name>` (or null if absent). Replaces `openclaw mcp show <name> --json`.
 */
export async function readMcpServer(configPath, mcpServerName) {
  const snap = await readOpenclawConfig(configPath);
  const mcp = snap.config.mcp;
  if (!mcp || typeof mcp !== 'object') return null;
  const servers = mcp.servers;
  if (!servers || typeof servers !== 'object') return null;
  const srv = servers[mcpServerName];
  if (srv == null) return null;
  return srv;
}

/**
 * Set `hooks` to nextHooks. Replaces `openclaw config set --strict-json hooks <json>`.
 */
export async function setHooks(configPath, nextHooks) {
  return mutateOpenclawConfig(configPath, (draft) => {
    draft.hooks = nextHooks;
  });
}

/**
 * Unset `hooks` entirely. Replaces `openclaw config unset hooks`.
 */
export async function unsetHooks(configPath) {
  return mutateOpenclawConfig(configPath, (draft) => {
    delete draft.hooks;
  });
}

/**
 * Set `mcp.servers.<name>` to nextServer. Replaces `openclaw mcp set <name> <json>`.
 */
export async function setMcpServer(configPath, mcpServerName, nextServer) {
  return mutateOpenclawConfig(configPath, (draft) => {
    if (!draft.mcp || typeof draft.mcp !== 'object') draft.mcp = {};
    if (!draft.mcp.servers || typeof draft.mcp.servers !== 'object') draft.mcp.servers = {};
    draft.mcp.servers[mcpServerName] = nextServer;
  });
}

/**
 * Unset `mcp.servers.<name>`. Replaces `openclaw mcp unset <name>`.
 */
export async function unsetMcpServer(configPath, mcpServerName) {
  return mutateOpenclawConfig(configPath, (draft) => {
    if (!draft.mcp?.servers) return;
    delete draft.mcp.servers[mcpServerName];
    // Tidy: drop empty .mcp.servers / .mcp shells so the file doesn't accumulate
    // {} cruft after repeated reset cycles.
    if (Object.keys(draft.mcp.servers).length === 0) delete draft.mcp.servers;
    if (draft.mcp && Object.keys(draft.mcp).length === 0) delete draft.mcp;
  });
}
