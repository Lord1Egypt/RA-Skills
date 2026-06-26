#!/usr/bin/env node
// OpenClaw Recovery Manager — projects-snapshot.mjs (PROJECTS subsystem)
//
// Usage:
//   node projects-snapshot.mjs all           "<description>"
//   node projects-snapshot.mjs <project>     "<description>"
//
// Project paths are discovered dynamically from ~/.openclaw/openclaw.json.
// Each project has its own 3-slot history under
// ~/.openclaw/rollback/projects/<project-name>/.
//
// Projects snapshots are ENTIRELY MANUAL. They are never auto-restored by the
// watchdog timer or the gateway:startup hook.
//
// What gets captured PER PROJECT (if present inside the project folder):
//   - openclaw.json                (project-level manifest)
//   - mcp_config.json              (external tool bridge config)
//   - package.json                 (local MCP server deps manifest)
//   - TASKS.json, PROCESSES.json, SPRINT_CURRENT.json   (state files)
//   - ./tools/                     (local MCP server source scripts)
//   - ./skills/                    (project-local skills)
//   - .openclaw/workspace.state.json   (project structural state)
//   - ./comms/                     (TREE STRUCTURE ONLY — no file content)
//
// What is explicitly NOT captured:
//   - node_modules/
//   - memory/
//   - auth-profiles.json
//   - ~/.openclaw/ root contents (covered by config snapshots)
//   - working content, repos, large data files

import { existsSync, statSync, mkdirSync, writeFileSync, copyFileSync, readdirSync, renameSync, unlinkSync } from 'fs';
import { join, dirname, basename } from 'path';
import { execSync } from 'child_process';
import { mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import {
  PROJECTS_DIR, CHANGE_LOG,
  listProjects, safeDirName,
  rotateIntoTarget, appendLog, timestamp
} from './utils.mjs';

const mode = process.argv[2];
const description = process.argv[3] || 'unlabeled';

if (!mode) {
  console.error('Usage: node projects-snapshot.mjs <all|PROJECT_NAME> "<description>"');
  process.exit(1);
}

const PROJECT_FILES = [
  'openclaw.json',
  'mcp_config.json',
  'package.json',
  'TASKS.json',
  'PROCESSES.json',
  'SPRINT_CURRENT.json'
];

const PROJECT_SUBDIR_FULL = ['tools', 'skills'];
// .openclaw/workspace.state.json — single specific file under a hidden subdir
// comms/ — tree structure only

const EXCLUDE_IN_SUBDIR = ['node_modules', 'memory', '.git', '.env']; // extra-defensive

/**
 * Build a per-project staged archive.
 * Returns path to tar.gz, or null if the project produced nothing worth saving.
 */
function snapshotProject(project) {
  const root = project.path;
  if (!existsSync(root) || !statSync(root).isDirectory()) {
    return { staged: null, reason: `project path not found: ${root}` };
  }

  const stage = mkdtempSync(join(tmpdir(), 'oc-proj-'));
  let captured = 0;

  // 1) Individual config / state files at project root
  for (const f of PROJECT_FILES) {
    const src = join(root, f);
    if (existsSync(src) && statSync(src).isFile()) {
      const dest = join(stage, src);
      mkdirSync(dirname(dest), { recursive: true });
      copyFileSync(src, dest);
      captured++;
    }
  }

  // 2) Full-content subdirs: tools/ and skills/ (with exclude list)
  for (const subdir of PROJECT_SUBDIR_FULL) {
    const src = join(root, subdir);
    if (existsSync(src) && statSync(src).isDirectory()) {
      const dest = join(stage, src);
      mkdirSync(dest, { recursive: true });
      copyRecursiveExclude(src, dest, EXCLUDE_IN_SUBDIR);
      captured++;
    }
  }

  // 3) .openclaw/workspace.state.json
  const wsState = join(root, '.openclaw', 'workspace.state.json');
  if (existsSync(wsState) && statSync(wsState).isFile()) {
    const dest = join(stage, wsState);
    mkdirSync(dirname(dest), { recursive: true });
    copyFileSync(wsState, dest);
    captured++;
  }

  // 4) comms/ — tree structure only, no file content
  const commsDir = join(root, 'comms');
  if (existsSync(commsDir) && statSync(commsDir).isDirectory()) {
    const dest = join(stage, commsDir);
    mkdirSync(dest, { recursive: true });
    copyStructureOnly(commsDir, dest);
    captured++;
  }

  if (captured === 0) {
    try { execSync(`rm -rf "${stage}"`); } catch {}
    return { staged: null, reason: 'project contains none of the backed-up files' };
  }

  const outZip = join(tmpdir(), `oc-proj-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.tar.gz`);
  try { unlinkSync(outZip); } catch {}
  execSync(`cd "${stage}" && tar -czf "${outZip}" .`, { stdio: 'ignore' });
  try { execSync(`rm -rf "${stage}"`); } catch {}
  return { staged: outZip, captured };
}

function copyRecursiveExclude(src, dest, excludeNames = []) {
  const exclude = new Set(excludeNames);
  const entries = readdirSync(src, { withFileTypes: true });
  for (const ent of entries) {
    if (exclude.has(ent.name)) continue;
    const s = join(src, ent.name);
    const d = join(dest, ent.name);
    if (ent.isDirectory()) {
      mkdirSync(d, { recursive: true });
      copyRecursiveExclude(s, d, excludeNames);
    } else if (ent.isFile()) {
      copyFileSync(s, d);
    }
  }
}

function copyStructureOnly(src, dest) {
  let anyDir = false;
  for (const ent of readdirSync(src, { withFileTypes: true })) {
    if (!ent.isDirectory()) continue;
    anyDir = true;
    const s = join(src, ent.name);
    const d = join(dest, ent.name);
    mkdirSync(d, { recursive: true });
    copyStructureOnly(s, d);
  }
  if (!anyDir) {
    try { writeFileSync(join(dest, '.dirtree'), ''); } catch {}
  }
}

// -- Resolve targets --
const allProjects = listProjects();

let targets;
if (mode === 'all') {
  targets = allProjects;
  if (targets.length === 0) {
    console.error('No projects found in openclaw.json.');
    process.exit(1);
  }
} else {
  const wanted = safeDirName(mode);
  const found = allProjects.find(p => p.name === mode || safeDirName(p.name) === wanted);
  if (!found) {
    console.error(`ERROR: project "${mode}" not found in openclaw.json.`);
    console.error(`Known projects: ${allProjects.map(p => p.name).join(', ') || '(none)'}`);
    process.exit(1);
  }
  targets = [found];
}

const ts = timestamp();
const results = [];

for (const project of targets) {
  const res = snapshotProject(project);
  if (!res.staged) {
    results.push({ name: project.name, status: 'skipped', reason: res.reason });
    continue;
  }
  const targetDir = join(PROJECTS_DIR, safeDirName(project.name));
  const manifest = rotateIntoTarget(targetDir, res.staged, {
    label: description,
    timestamp: ts,
    ai_summary: '',
    extra: { source: project.path, projectName: project.name }
  });
  appendLog(CHANGE_LOG,
    `PROJECT SNAPSHOT TAKEN\n  Project: ${project.name}\n  Source: ${project.path}\n  Slot: 1\n  Description: "${description}"`
  );
  results.push({ name: project.name, status: 'ok', slot: 1, path: project.path, slots: manifest.snapshots.length });
}

console.log(`Projects snapshot — ${ts}`);
for (const r of results) {
  if (r.status === 'ok') {
    console.log(`  ✓ ${r.name.padEnd(20)} slot 1  (${r.path})`);
  } else {
    console.log(`  ⚠ ${r.name.padEnd(20)} ${r.status}: ${r.reason}`);
  }
}

const ok = results.filter(r => r.status === 'ok').length;
if (ok === 0) {
  console.error('No project snapshots taken.');
  process.exit(1);
}
console.log(`\n${ok} project(s) snapshotted. Description: "${description}"`);
