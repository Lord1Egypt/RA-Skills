#!/usr/bin/env node
// OpenClaw Emergency Rollback — snapshot.mjs
// Usage: node snapshot.mjs "<label>" "<ai_summary>"
// Takes a labeled snapshot of all OpenClaw config files.

import { readFileSync, existsSync, mkdirSync, copyFileSync, renameSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { execSync } from 'child_process';
import { mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import {
  ROLLBACK_DIR, MANIFEST_FILE, SNAPSHOTS_DIR, CHANGE_LOG,
  readJson, writeJson, getOpenclawHome, getOpenclawJson, getManifest,
  appendLog, timestamp, timestampHuman
} from './utils.mjs';

const LABEL = process.argv[2] || 'unlabeled';
const AI_SUMMARY = process.argv[3] || 'No summary provided.';

const OC_HOME = getOpenclawHome();
const OC_JSON = getOpenclawJson();

if (!existsSync(OC_JSON)) {
  console.error(`ERROR: openclaw.json not found at ${OC_JSON}`);
  process.exit(1);
}

// Read openclaw.json to extract workspace paths and agent IDs
const ocConfig = readJson(OC_JSON);
const HOME = process.env.HOME || '/root';

// Extract workspace paths
const workspacePaths = new Set();
if (ocConfig?.agents) {
  if (ocConfig.agents.defaults?.workspace) {
    workspacePaths.add(ocConfig.agents.defaults.workspace.replace('~', HOME));
  }
  if (ocConfig.agents.list) {
    ocConfig.agents.list.forEach(a => {
      if (a.workspace) workspacePaths.add(a.workspace.replace('~', HOME));
    });
  }
}
if (workspacePaths.size === 0) {
  workspacePaths.add(join(HOME, '.openclaw', 'workspace'));
}

// Note: agent IDs are not extracted because auth-profiles.json is
// deliberately excluded from snapshots (sensitive credentials).

// Stage files into a temp dir preserving full absolute paths
const stageDir = mkdtempSync(join(tmpdir(), 'oc-snapshot-'));
const filesCaptured = [];

// Stage openclaw.json
const stagedOcJson = join(stageDir, OC_JSON);
mkdirSync(dirname(stagedOcJson), { recursive: true });
copyFileSync(OC_JSON, stagedOcJson);
filesCaptured.push(OC_JSON);

// Stage workspace config files
const WORKSPACE_FILES = ['SOUL.md', 'AGENTS.md', 'USER.md', 'IDENTITY.md', 'TOOLS.md', 'HEARTBEAT.md', 'BOOT.md'];
for (const wsPath of workspacePaths) {
  for (const wf of WORKSPACE_FILES) {
    const src = join(wsPath, wf);
    if (existsSync(src)) {
      const dest = join(stageDir, src);
      mkdirSync(dirname(dest), { recursive: true });
      copyFileSync(src, dest);
      filesCaptured.push(src);
    }
  }
}

// Auth profiles (auth-profiles.json) are deliberately NOT captured.
// They contain sensitive credentials and must never be stored in snapshots.

// Create zip from staging dir
const tmpZip = join(tmpdir(), 'oc-snapshot-tmp.tar.gz');
try { unlinkSync(tmpZip); } catch {}
execSync(`cd "${stageDir}" && tar -czf "${tmpZip}" .`, { stdio: 'ignore' });

// Clean up staging dir
execSync(`rm -rf "${stageDir}"`);

// Rotate snapshots: 2→3, 1→2, new→1
mkdirSync(SNAPSHOTS_DIR, { recursive: true });
const snap3 = join(SNAPSHOTS_DIR, 'snapshot-3.tar.gz');
const snap2 = join(SNAPSHOTS_DIR, 'snapshot-2.tar.gz');
const snap1 = join(SNAPSHOTS_DIR, 'snapshot-1.tar.gz');

if (existsSync(snap2)) {
  if (existsSync(snap3)) unlinkSync(snap3);
  renameSync(snap2, snap3);
}
if (existsSync(snap1)) {
  renameSync(snap1, snap2);
}
copyFileSync(tmpZip, snap1); unlinkSync(tmpZip);

// Update manifest.json — shift existing entries, add new slot 1
const manifest = getManifest();
const shifted = manifest.snapshots
  .filter(s => s.slot <= 2)
  .map(s => ({ ...s, slot: s.slot + 1, file: `snapshot-${s.slot + 1}.tar.gz` }));

shifted.unshift({
  slot: 1,
  file: 'snapshot-1.tar.gz',
  label: LABEL,
  timestamp: timestamp(),
  ai_summary: AI_SUMMARY
});

manifest.snapshots = shifted.filter(s => s.slot <= 3);
manifest.watchdog_target = 'snapshot-1';
writeJson(MANIFEST_FILE, manifest);

// Log
appendLog(CHANGE_LOG,
  `SNAPSHOT TAKEN\n  Slot: 1 (previous snapshots shifted)\n  Label: "${LABEL}"\n  Summary: ${AI_SUMMARY}\n  Files: ${filesCaptured.join(', ')}`
);

console.log(`Snapshot saved: slot 1 — ${LABEL} (${timestamp()})`);
