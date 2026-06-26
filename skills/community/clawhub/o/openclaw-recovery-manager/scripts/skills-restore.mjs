#!/usr/bin/env node
// OpenClaw Recovery Manager — skills-restore.mjs (SKILLS subsystem)
//
// Usage:
//   node skills-restore.mjs all                     -> restore slot 1 for every target
//   node skills-restore.mjs global [slot]           -> restore global, defaults to slot 1
//   node skills-restore.mjs <agent> [slot]          -> restore a single agent's skills
//
// MANUAL ONLY. This script is never invoked by the watchdog timer or the
// gateway:startup hook. Skills are restored entirely by user request.
//
// Restore extracts each target's tar.gz directly to / so the absolute paths
// inside the archive go back where they came from.

import { existsSync } from 'fs';
import { join } from 'path';
import {
  SKILLS_DIR, CHANGE_LOG,
  listAgents, resolveAgentSkillsDir, getGlobalSkillsDir,
  readTargetManifest, safeDirName,
  extractArchive, appendLog, timestamp
} from './utils.mjs';

const mode = process.argv[2];
const slotArg = parseInt(process.argv[3], 10);

if (!mode) {
  console.error('Usage: node skills-restore.mjs <all|global|AGENT_NAME> [slot]');
  process.exit(1);
}

function allTargets() {
  const out = [];
  out.push({ name: 'global', dir: getGlobalSkillsDir(), agentId: null });
  for (const a of listAgents()) {
    const d = resolveAgentSkillsDir(a);
    if (d) out.push({ name: safeDirName(a.id), dir: d, agentId: a.id });
  }
  return out;
}

function resolveSingle(mode) {
  if (mode === 'global') return { name: 'global', dir: getGlobalSkillsDir(), agentId: null };
  const agents = listAgents();
  const agent = agents.find(a => a.id === mode || safeDirName(a.id) === safeDirName(mode));
  if (!agent) {
    console.error(`ERROR: target "${mode}" not found in openclaw.json.`);
    console.error(`Known: global, ${agents.map(a => a.id).join(', ')}`);
    process.exit(1);
  }
  const d = resolveAgentSkillsDir(agent);
  if (!d) {
    console.error(`ERROR: agent "${agent.id}" has no resolvable skills directory.`);
    process.exit(1);
  }
  return { name: safeDirName(agent.id), dir: d, agentId: agent.id };
}

const restoreList = mode === 'all'
  ? allTargets().map(t => ({ target: t, slot: 1 }))
  : [{ target: resolveSingle(mode), slot: Number.isFinite(slotArg) && slotArg > 0 ? slotArg : 1 }];

const ts = timestamp();
let okCount = 0;
const report = [];

for (const { target, slot } of restoreList) {
  const targetDir = join(SKILLS_DIR, target.name);
  const mf = readTargetManifest(targetDir);
  const entry = (mf.snapshots || []).find(s => s.slot === slot);
  if (!entry) {
    report.push({ name: target.name, status: 'skipped', reason: `no snapshot in slot ${slot}` });
    continue;
  }
  const zipPath = join(targetDir, entry.file);
  if (!existsSync(zipPath)) {
    report.push({ name: target.name, status: 'failed', reason: `archive missing: ${zipPath}` });
    continue;
  }
  const exit = extractArchive(zipPath);
  if (exit === 0) {
    okCount++;
    report.push({ name: target.name, status: 'ok', slot, label: entry.label, timestamp: entry.timestamp });
    appendLog(CHANGE_LOG,
      `SKILLS RESTORED\n  Target: ${target.name}\n  Slot: ${slot}\n  Label: "${entry.label || ''}"\n  Snapshot timestamp: ${entry.timestamp || 'unknown'}\n  Extracted to: /`
    );
  } else {
    report.push({ name: target.name, status: 'failed', reason: `tar exit code ${exit}` });
    appendLog(CHANGE_LOG,
      `SKILLS RESTORE FAILED\n  Target: ${target.name}\n  Slot: ${slot}\n  tar exit: ${exit}`
    );
  }
}

// Report
console.log(`Skills restore — ${ts}`);
for (const r of report) {
  if (r.status === 'ok') {
    console.log(`  ✓ ${r.name.padEnd(20)} slot ${r.slot}  "${r.label || ''}"  (${r.timestamp || ''})`);
  } else {
    console.log(`  ⚠ ${r.name.padEnd(20)} ${r.status}: ${r.reason}`);
  }
}

if (okCount === 0) {
  console.error('\nNo skills were restored.');
  process.exit(1);
}
console.log(`\n${okCount} target(s) restored.`);
console.log('NOTE: skills restores never touch config or the watchdog timer.');
