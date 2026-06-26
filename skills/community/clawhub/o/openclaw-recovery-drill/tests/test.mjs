#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'openclaw-recovery-drill-'));
const workspace = path.join(tmpRoot, 'workspace');
const backupRoot = path.join(tmpRoot, 'backups');
fs.mkdirSync(workspace, { recursive: true });
fs.mkdirSync(backupRoot, { recursive: true });
fs.mkdirSync(path.join(workspace, 'memory'), { recursive: true });
fs.mkdirSync(path.join(workspace, 'docs'), { recursive: true });

for (const file of ['SOUL.md', 'USER.md', 'TOOLS.md', 'MEMORY.md', 'TODO.md', 'progress-log.md']) {
  fs.writeFileSync(path.join(workspace, file), `${file}\n`);
}
fs.writeFileSync(path.join(workspace, 'docs', 'recovery.md'), '# recovery\n');

const artifact = path.join(backupRoot, 'snapshot-1');
fs.mkdirSync(artifact, { recursive: true });
fs.writeFileSync(path.join(artifact, 'manifest.json'), '{}\n');

const output = execFileSync('node', ['scripts/recovery-drill.mjs', '--workspace', workspace, '--backup-root', backupRoot], {
  cwd: path.resolve(process.cwd()),
  encoding: 'utf8'
});
const data = JSON.parse(output);
assert.equal(data.verdict, 'PASS');
assert.equal(typeof data.score, 'number');
assert.ok(Array.isArray(data.drillPlan));
assert.ok(data.evidence.keyFiles['SOUL.md']);
assert.ok(data.evidence.backupRoots.some((entry) => entry.root === backupRoot && entry.exists));

console.log('recovery-drill test: PASS');
