#!/usr/bin/env node
// OpenClaw Recovery Manager — projects-restore.mjs (PROJECTS subsystem)
//
// Usage:
//   node projects-restore.mjs all                      -> restore slot 1 for every project
//   node projects-restore.mjs <project> [slot]         -> restore a single project
//
// MANUAL ONLY. Never invoked by the watchdog timer or startup hook.

import { existsSync } from 'fs';
import { join } from 'path';
import {
  PROJECTS_DIR, CHANGE_LOG,
  listProjects, readTargetManifest, safeDirName,
  extractArchive, appendLog, timestamp
} from './utils.mjs';

const mode = process.argv[2];
const slotArg = parseInt(process.argv[3], 10);

if (!mode) {
  console.error('Usage: node projects-restore.mjs <all|PROJECT_NAME> [slot]');
  process.exit(1);
}

const allProjects = listProjects();

let plan;
if (mode === 'all') {
  plan = allProjects.map(p => ({ project: p, slot: 1 }));
  if (plan.length === 0) {
    console.error('No projects configured in openclaw.json.');
    process.exit(1);
  }
} else {
  const want = safeDirName(mode);
  const p = allProjects.find(x => x.name === mode || safeDirName(x.name) === want);
  if (!p) {
    console.error(`ERROR: project "${mode}" not found in openclaw.json.`);
    console.error(`Known: ${allProjects.map(x => x.name).join(', ')}`);
    process.exit(1);
  }
  plan = [{ project: p, slot: Number.isFinite(slotArg) && slotArg > 0 ? slotArg : 1 }];
}

const ts = timestamp();
const report = [];
let okCount = 0;

for (const { project, slot } of plan) {
  const targetDir = join(PROJECTS_DIR, safeDirName(project.name));
  const mf = readTargetManifest(targetDir);
  const entry = (mf.snapshots || []).find(s => s.slot === slot);
  if (!entry) {
    report.push({ name: project.name, status: 'skipped', reason: `no snapshot in slot ${slot}` });
    continue;
  }
  const zipPath = join(targetDir, entry.file);
  if (!existsSync(zipPath)) {
    report.push({ name: project.name, status: 'failed', reason: `archive missing: ${zipPath}` });
    continue;
  }
  const exit = extractArchive(zipPath);
  if (exit === 0) {
    okCount++;
    report.push({ name: project.name, status: 'ok', slot, label: entry.label, timestamp: entry.timestamp });
    appendLog(CHANGE_LOG,
      `PROJECT RESTORED\n  Project: ${project.name}\n  Path: ${project.path}\n  Slot: ${slot}\n  Label: "${entry.label || ''}"\n  Snapshot timestamp: ${entry.timestamp || 'unknown'}`
    );
  } else {
    report.push({ name: project.name, status: 'failed', reason: `tar exit code ${exit}` });
    appendLog(CHANGE_LOG,
      `PROJECT RESTORE FAILED\n  Project: ${project.name}\n  Slot: ${slot}\n  tar exit: ${exit}`
    );
  }
}

console.log(`Projects restore — ${ts}`);
for (const r of report) {
  if (r.status === 'ok') {
    console.log(`  ✓ ${r.name.padEnd(20)} slot ${r.slot}  "${r.label || ''}"  (${r.timestamp || ''})`);
  } else {
    console.log(`  ⚠ ${r.name.padEnd(20)} ${r.status}: ${r.reason}`);
  }
}

if (okCount === 0) {
  console.error('\nNo projects were restored.');
  process.exit(1);
}
console.log(`\n${okCount} project(s) restored.`);
console.log('NOTE: project restores never touch root config or the watchdog timer.');
