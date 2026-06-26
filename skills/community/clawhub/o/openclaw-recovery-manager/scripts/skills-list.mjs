#!/usr/bin/env node
// OpenClaw Recovery Manager — skills-list.mjs (SKILLS subsystem)
//
// Usage:
//   node skills-list.mjs            -> list all targets (global + each agent)
//   node skills-list.mjs global     -> list global skills history only
//   node skills-list.mjs <agent>    -> list that agent's skills history only

import { existsSync, readdirSync, statSync } from 'fs';
import { join } from 'path';
import {
  SKILLS_DIR,
  listAgents, resolveAgentSkillsDir, getGlobalSkillsDir,
  readTargetManifest, safeDirName
} from './utils.mjs';

const filter = process.argv[2]; // optional: "global" or agent id

function humanTs(isoZ) {
  if (!isoZ) return 'unknown';
  try {
    const d = new Date(isoZ);
    return d.toISOString().replace('T', ' ').replace(/Z?$/, '');
  } catch {
    return isoZ;
  }
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

let targets = allTargets();
if (filter) {
  if (filter === 'global') {
    targets = targets.filter(t => t.name === 'global');
  } else {
    const want = safeDirName(filter);
    targets = targets.filter(t => t.name === want);
  }
  if (targets.length === 0) {
    console.error(`ERROR: target "${filter}" not found. Known: global, ${listAgents().map(a => a.id).join(', ')}`);
    process.exit(1);
  }
}

console.log('Skills Snapshots');
console.log('================');

for (const t of targets) {
  const targetDir = join(SKILLS_DIR, t.name);
  const mf = readTargetManifest(targetDir);
  const snaps = Array.isArray(mf.snapshots) ? mf.snapshots : [];
  const sourceTag = t.agentId ? `agent: ${t.agentId}` : 'global';
  console.log(`\n[${t.name}]  (${sourceTag})`);
  console.log(`  source: ${t.dir}`);
  if (!existsSync(targetDir) || snaps.length === 0) {
    console.log('  (no snapshots)');
    continue;
  }
  snaps.sort((a, b) => a.slot - b.slot);
  for (const s of snaps) {
    const label = s.label || 'unlabeled';
    const ts = humanTs(s.timestamp);
    console.log(`  [${s.slot}] ${ts}  —  "${label}"`);
  }
}
console.log('');
