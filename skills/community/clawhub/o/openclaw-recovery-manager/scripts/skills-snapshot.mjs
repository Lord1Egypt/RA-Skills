#!/usr/bin/env node
// OpenClaw Recovery Manager — skills-snapshot.mjs (SKILLS subsystem)
//
// Usage:
//   node skills-snapshot.mjs all      "<description>"
//   node skills-snapshot.mjs global   "<description>"
//   node skills-snapshot.mjs <agent>  "<description>"
//
// Snapshots skills directories. Each target (global + each configured agent)
// maintains its own independent 3-slot history under ~/.openclaw/rollback/skills/.
//
// Skills snapshots are ENTIRELY MANUAL. They are never auto-restored by the
// watchdog timer or the gateway:startup hook. That remains config-only.

import { existsSync, statSync } from 'fs';
import { join } from 'path';
import {
  SKILLS_DIR, CHANGE_LOG,
  listAgents, resolveAgentSkillsDir, getGlobalSkillsDir,
  makeStagedArchive, rotateIntoTarget, safeDirName,
  appendLog, timestamp
} from './utils.mjs';

const mode = process.argv[2];
const description = process.argv[3] || 'unlabeled';

if (!mode) {
  console.error('Usage: node skills-snapshot.mjs <all|global|AGENT_NAME> "<description>"');
  process.exit(1);
}

/** Build the list of {name, dir} targets this invocation should snapshot. */
function resolveTargets(mode) {
  const targets = [];
  const globalDir = getGlobalSkillsDir();
  const agents = listAgents();

  if (mode === 'all') {
    targets.push({ name: 'global', dir: globalDir });
    for (const a of agents) {
      const d = resolveAgentSkillsDir(a);
      if (d) targets.push({ name: safeDirName(a.id), dir: d, agentId: a.id });
    }
    return targets;
  }
  if (mode === 'global') {
    return [{ name: 'global', dir: globalDir }];
  }
  // Agent by id
  const agent = agents.find(a => a.id === mode || safeDirName(a.id) === safeDirName(mode));
  if (!agent) {
    console.error(`ERROR: agent "${mode}" not found in openclaw.json.`);
    console.error(`Known agents: ${agents.map(a => a.id).join(', ') || '(none)'}`);
    process.exit(1);
  }
  const d = resolveAgentSkillsDir(agent);
  if (!d) {
    console.error(`ERROR: agent "${agent.id}" has no skills directory (no agent.skills and no workspace).`);
    process.exit(1);
  }
  return [{ name: safeDirName(agent.id), dir: d, agentId: agent.id }];
}

const targets = resolveTargets(mode);
const ts = timestamp();
const results = [];

for (const t of targets) {
  if (!existsSync(t.dir) || !statSync(t.dir).isDirectory()) {
    results.push({ name: t.name, status: 'skipped', reason: `skills dir not found at ${t.dir}` });
    continue;
  }

  const staged = makeStagedArchive([t.dir]);
  if (!staged) {
    results.push({ name: t.name, status: 'skipped', reason: 'skills dir empty or unreadable' });
    continue;
  }

  const targetDir = join(SKILLS_DIR, t.name);
  const manifest = rotateIntoTarget(targetDir, staged, {
    label: description,
    timestamp: ts,
    ai_summary: '',
    extra: { source: t.dir, scope: t.name === 'global' ? 'global' : 'agent', agentId: t.agentId || null }
  });

  appendLog(CHANGE_LOG,
    `SKILLS SNAPSHOT TAKEN\n  Target: ${t.name}\n  Source: ${t.dir}\n  Slot: 1\n  Description: "${description}"`
  );

  results.push({ name: t.name, status: 'ok', slot: 1, dir: t.dir, slots: manifest.snapshots.length });
}

// Report
console.log(`Skills snapshot — ${ts}`);
for (const r of results) {
  if (r.status === 'ok') {
    console.log(`  ✓ ${r.name.padEnd(20)} slot 1  (${r.dir})`);
  } else {
    console.log(`  ⚠ ${r.name.padEnd(20)} ${r.status}: ${r.reason}`);
  }
}

const ok = results.filter(r => r.status === 'ok').length;
if (ok === 0) {
  console.error('No skills snapshots taken.');
  process.exit(1);
}
console.log(`\n${ok} target(s) snapshotted. Description: "${description}"`);
