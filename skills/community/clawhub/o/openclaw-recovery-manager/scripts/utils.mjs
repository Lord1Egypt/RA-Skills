// OpenClaw Recovery Manager — shared utilities
// (Skill name openclaw-emergency-rollback preserved for install compatibility.)
//
// All JSON I/O goes through here. No string interpolation of user data into code.
//
// This file preserves every export the original config-only rollback relied on,
// and adds new helpers for the skills and projects snapshot subsystems.

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync, copyFileSync, renameSync, unlinkSync } from 'fs';
import { join, dirname, basename, resolve } from 'path';
import { execSync } from 'child_process';
import { mkdtempSync } from 'fs';
import { tmpdir } from 'os';

const HOME = process.env.HOME || '/root';

// ---- Paths: existing (do not rename, existing installs depend on them) ----
export const ROLLBACK_DIR    = join(HOME, '.openclaw/rollback');
export const CONFIG_FILE     = join(ROLLBACK_DIR, 'rollback-config.json');
export const MANIFEST_FILE   = join(ROLLBACK_DIR, 'manifest.json');
export const WATCHDOG_FILE   = join(ROLLBACK_DIR, 'watchdog.json');
export const CHANGE_LOG      = join(ROLLBACK_DIR, 'logs', 'change.log');
export const RESTORE_LOG     = join(ROLLBACK_DIR, 'logs', 'restore.log');
export const SNAPSHOTS_DIR   = join(ROLLBACK_DIR, 'snapshots');
export const RECOVERY_FILE   = join(ROLLBACK_DIR, 'openclaw.recovery');

// ---- Paths: new subsystems ----
export const SKILLS_DIR      = join(ROLLBACK_DIR, 'skills');   // per-target subfolders live under this
export const PROJECTS_DIR    = join(ROLLBACK_DIR, 'projects'); // per-project subfolders live under this

// ---- Generic JSON helpers ----
export function readJson(filepath) {
  try {
    return JSON.parse(readFileSync(filepath, 'utf8'));
  } catch {
    return null;
  }
}

export function writeJson(filepath, data) {
  mkdirSync(dirname(filepath), { recursive: true });
  writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
}

export function getConfig() {
  const config = readJson(CONFIG_FILE);
  if (!config) {
    console.error('ERROR: rollback-config.json not found. Run setup first.');
    process.exit(1);
  }
  return config;
}

export function getOpenclawHome() {
  const config = getConfig();
  return (config.openclawHome || '~/.openclaw').replace('~', HOME);
}

export function getOpenclawJson() {
  return join(getOpenclawHome(), 'openclaw.json');
}

export function getManifest() {
  return readJson(MANIFEST_FILE) || { watchdog_target: 'snapshot-1', snapshots: [] };
}

export function getWatchdog() {
  return readJson(WATCHDOG_FILE) || { armed: false };
}

export function appendLog(logFile, entry) {
  const ts = new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, '');
  mkdirSync(dirname(logFile), { recursive: true });
  const existing = existsSync(logFile) ? readFileSync(logFile, 'utf8') : '';
  writeFileSync(logFile, existing + `[${ts}] ${entry}\n---\n`);
}

export function timestamp() {
  return new Date().toISOString().replace(/\.\d+Z$/, 'Z');
}

export function timestampHuman() {
  return new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, '');
}

// ---- Path expansion ----
export function expandHome(p) {
  if (!p) return p;
  return p.replace(/^~/, HOME);
}

// ---------------------------------------------------------------------------
// Dynamic discovery from openclaw.json
// ---------------------------------------------------------------------------
//
// These helpers read the user's live openclaw.json every time they're called,
// so adding or renaming an agent/project is automatically reflected. Nothing
// is hardcoded.
// ---------------------------------------------------------------------------

/** Return the parsed openclaw.json, or null if unreadable/missing. */
export function getOpenclawConfig() {
  return readJson(getOpenclawJson());
}

/**
 * List agents configured in openclaw.json.
 * Returns array of { id, workspace, skills } where:
 *   - id is the agent's identifier (falls back to workspace basename)
 *   - workspace is the absolute path (~ expanded) or null
 *   - skills is the agent's skills dir if explicitly set, else null
 *     (callers that want the workspace-fallback path should compute it)
 */
export function listAgents() {
  const cfg = getOpenclawConfig();
  if (!cfg?.agents?.list || !Array.isArray(cfg.agents.list)) return [];
  return cfg.agents.list.map((a, idx) => {
    const id = a.id || a.name || (a.workspace ? basename(expandHome(a.workspace)) : `agent-${idx}`);
    const workspace = a.workspace ? expandHome(a.workspace) : null;
    const skills = a.skills ? expandHome(a.skills) : null;
    return { id, workspace, skills };
  });
}

/**
 * Resolve an agent's skills directory.
 * Priority: explicit agent.skills > {workspace}/skills > null.
 */
export function resolveAgentSkillsDir(agent) {
  if (agent.skills) return agent.skills;
  if (agent.workspace) return join(agent.workspace, 'skills');
  return null;
}

/** Global skills directory: ~/.openclaw/skills. */
export function getGlobalSkillsDir() {
  return join(getOpenclawHome(), 'skills');
}

/**
 * List projects configured in openclaw.json.
 * Tolerant to several common shapes:
 *   - projects.list: [{ name, path }]
 *   - projects: [{ name, path }]
 *   - projects: { myproj: "~/path", other: { path: "~/x" } }
 * Returns array of { name, path } with ~ expanded.
 * Projects without a resolvable path are filtered out.
 */
export function listProjects() {
  const cfg = getOpenclawConfig();
  if (!cfg?.projects) return [];
  const out = [];
  const seen = new Set();
  const push = (name, path) => {
    if (!name || !path) return;
    const abs = expandHome(path);
    if (seen.has(name)) return;
    seen.add(name);
    out.push({ name, path: abs });
  };

  if (Array.isArray(cfg.projects)) {
    cfg.projects.forEach((p, i) => {
      if (typeof p === 'string') push(basename(p), p);
      else if (p && typeof p === 'object') push(p.name || p.id || `project-${i}`, p.path);
    });
  } else if (Array.isArray(cfg.projects.list)) {
    cfg.projects.list.forEach((p, i) => {
      if (typeof p === 'string') push(basename(p), p);
      else if (p && typeof p === 'object') push(p.name || p.id || `project-${i}`, p.path);
    });
  } else if (typeof cfg.projects === 'object') {
    Object.entries(cfg.projects).forEach(([key, v]) => {
      if (typeof v === 'string') push(key, v);
      else if (v && typeof v === 'object' && v.path) push(key, v.path);
    });
  }
  return out;
}

/** Sanitize a name for safe use as a directory name. */
export function safeDirName(name) {
  return String(name).replace(/[^A-Za-z0-9._-]+/g, '_').replace(/^_+|_+$/g, '') || 'unnamed';
}

// ---------------------------------------------------------------------------
// Per-target slot rotation (shared by skills and projects subsystems)
// ---------------------------------------------------------------------------
//
// A "target" is a single subfolder under skills/ or projects/ that owns its
// own independent 3-slot history. Slot 1 = most recent. Slot 3 = oldest.
// A 4th snapshot pushes slot 3 out. Identical behavior to the original config
// snapshot rotation, just scoped per target.
// ---------------------------------------------------------------------------

/** Ensure a target directory and its manifest exist; returns the manifest. */
export function ensureTargetManifest(targetDir) {
  mkdirSync(targetDir, { recursive: true });
  const mf = join(targetDir, 'manifest.json');
  const existing = readJson(mf);
  if (existing) return existing;
  const fresh = { snapshots: [] };
  writeJson(mf, fresh);
  return fresh;
}

export function readTargetManifest(targetDir) {
  return readJson(join(targetDir, 'manifest.json')) || { snapshots: [] };
}

export function writeTargetManifest(targetDir, manifest) {
  writeJson(join(targetDir, 'manifest.json'), manifest);
}

/**
 * Rotate an existing staged archive into a target's 3-slot history.
 *   targetDir:  absolute path of the per-target folder
 *   stagedZip:  absolute path to the tar.gz that should become slot 1
 *   entry:      { label, timestamp, ai_summary, ...extras } for the new slot 1
 * Returns the updated manifest.
 */
export function rotateIntoTarget(targetDir, stagedZip, entry) {
  mkdirSync(targetDir, { recursive: true });
  const snap1 = join(targetDir, 'snapshot-1.tar.gz');
  const snap2 = join(targetDir, 'snapshot-2.tar.gz');
  const snap3 = join(targetDir, 'snapshot-3.tar.gz');

  if (existsSync(snap2)) {
    if (existsSync(snap3)) unlinkSync(snap3);
    renameSync(snap2, snap3);
  }
  if (existsSync(snap1)) {
    renameSync(snap1, snap2);
  }
  copyFileSync(stagedZip, snap1);
  try { unlinkSync(stagedZip); } catch {}

  const manifest = readTargetManifest(targetDir);
  const shifted = (manifest.snapshots || [])
    .filter(s => s.slot <= 2)
    .map(s => ({ ...s, slot: s.slot + 1, file: `snapshot-${s.slot + 1}.tar.gz` }));

  shifted.unshift({
    slot: 1,
    file: 'snapshot-1.tar.gz',
    label: entry.label || 'unlabeled',
    timestamp: entry.timestamp || timestamp(),
    ai_summary: entry.ai_summary || '',
    ...(entry.extra || {})
  });

  manifest.snapshots = shifted.filter(s => s.slot <= 3);
  writeTargetManifest(targetDir, manifest);
  return manifest;
}

// ---------------------------------------------------------------------------
// Archive helpers (tar.gz — matches existing config subsystem)
// ---------------------------------------------------------------------------

/** Create a tar.gz of a source path, preserving its absolute-path layout. */
export function makeStagedArchive(sourcePaths, { excludeGlobs = [], dirTreeOnly = [] } = {}) {
  const stage = mkdtempSync(join(tmpdir(), 'oc-rm-stage-'));
  let captured = 0;

  for (const src of sourcePaths) {
    if (!src || !existsSync(src)) continue;
    const dest = join(stage, src); // preserve absolute layout inside stage
    try {
      if (statSync(src).isDirectory()) {
        mkdirSync(dest, { recursive: true });
        // rsync would be ideal; fall back to cp -a with excludes via find
        copyDirRecursive(src, dest, excludeGlobs);
        captured++;
      } else {
        mkdirSync(dirname(dest), { recursive: true });
        copyFileSync(src, dest);
        captured++;
      }
    } catch (e) {
      // continue — best-effort capture
    }
  }

  // For "tree only" paths: recreate directory structure but skip file content.
  for (const src of dirTreeOnly) {
    if (!src || !existsSync(src)) continue;
    try {
      if (statSync(src).isDirectory()) {
        const dest = join(stage, src);
        mkdirSync(dest, { recursive: true });
        copyDirStructureOnly(src, dest);
        captured++;
      }
    } catch {}
  }

  if (captured === 0) {
    execSync(`rm -rf "${stage}"`);
    return null;
  }

  const outZip = join(tmpdir(), `oc-rm-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.tar.gz`);
  try { unlinkSync(outZip); } catch {}
  execSync(`cd "${stage}" && tar -czf "${outZip}" .`, { stdio: 'ignore' });
  execSync(`rm -rf "${stage}"`);
  return outZip;
}

/** Copy a directory recursively, honoring top-level exclude names. */
function copyDirRecursive(src, dest, excludeNames = []) {
  const exclude = new Set(excludeNames);
  const entries = readdirSync(src, { withFileTypes: true });
  for (const ent of entries) {
    if (exclude.has(ent.name)) continue;
    const s = join(src, ent.name);
    const d = join(dest, ent.name);
    if (ent.isDirectory()) {
      mkdirSync(d, { recursive: true });
      copyDirRecursive(s, d, excludeNames);
    } else if (ent.isFile()) {
      copyFileSync(s, d);
    }
    // symlinks and other types: skip silently
  }
}

/** Recreate directory tree structure only (no files). */
function copyDirStructureOnly(src, dest) {
  const entries = readdirSync(src, { withFileTypes: true });
  for (const ent of entries) {
    if (!ent.isDirectory()) continue;
    const s = join(src, ent.name);
    const d = join(dest, ent.name);
    mkdirSync(d, { recursive: true });
    copyDirStructureOnly(s, d);
  }
  // Leave an empty .dirtree marker at leaves so the tree isn't entirely empty
  // (optional, but helpful for verifying the tree capture worked).
  if (entries.filter(e => e.isDirectory()).length === 0) {
    try { writeFileSync(join(dest, '.dirtree'), ''); } catch {}
  }
}

/** Extract a tar.gz into /, overwriting. Returns exit code (0 = success). */
export function extractArchive(zipPath) {
  try {
    execSync(`tar -xzf "${zipPath}" -C /`, { stdio: 'ignore' });
    return 0;
  } catch (e) {
    return e.status || 1;
  }
}
