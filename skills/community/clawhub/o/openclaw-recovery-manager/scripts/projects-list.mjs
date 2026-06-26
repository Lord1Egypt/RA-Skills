#!/usr/bin/env node
// OpenClaw Recovery Manager — projects-list.mjs (PROJECTS subsystem)
//
// Usage:
//   node projects-list.mjs              -> list all projects + histories
//   node projects-list.mjs <project>    -> list that project's 3-slot history

import { existsSync } from 'fs';
import { join } from 'path';
import {
  PROJECTS_DIR,
  listProjects, readTargetManifest, safeDirName
} from './utils.mjs';

const filter = process.argv[2];

function humanTs(isoZ) {
  if (!isoZ) return 'unknown';
  try {
    return new Date(isoZ).toISOString().replace('T', ' ').replace(/Z?$/, '');
  } catch { return isoZ; }
}

let projects = listProjects();
if (filter) {
  const want = safeDirName(filter);
  projects = projects.filter(p => p.name === filter || safeDirName(p.name) === want);
  if (projects.length === 0) {
    console.error(`ERROR: project "${filter}" not found in openclaw.json.`);
    process.exit(1);
  }
}

console.log('Project Snapshots');
console.log('=================');

if (projects.length === 0) {
  console.log('\n(no projects configured in openclaw.json)');
  process.exit(0);
}

for (const p of projects) {
  const targetDir = join(PROJECTS_DIR, safeDirName(p.name));
  const mf = readTargetManifest(targetDir);
  const snaps = Array.isArray(mf.snapshots) ? mf.snapshots : [];
  console.log(`\n[${p.name}]`);
  console.log(`  path: ${p.path}`);
  if (!existsSync(targetDir) || snaps.length === 0) {
    console.log('  (no snapshots)');
    continue;
  }
  snaps.sort((a, b) => a.slot - b.slot);
  for (const s of snaps) {
    console.log(`  [${s.slot}] ${humanTs(s.timestamp)}  —  "${s.label || 'unlabeled'}"`);
  }
}
console.log('');
