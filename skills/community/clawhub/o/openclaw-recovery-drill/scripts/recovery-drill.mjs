#!/usr/bin/env node
import fs from 'fs';
import os from 'os';
import path from 'path';

const args = process.argv.slice(2);
function getArg(name, fallback = undefined) {
  const idx = args.indexOf(name);
  if (idx === -1) return fallback;
  return args[idx + 1] ?? fallback;
}

const workspace = path.resolve(getArg('--workspace', '/Users/m1/.openclaw/workspace'));
const home = os.homedir();
const backupRoots = [];
const cliBackupRoot = getArg('--backup-root');
if (cliBackupRoot) backupRoots.push(path.resolve(cliBackupRoot));
backupRoots.push(
  path.join(workspace, 'backups'),
  path.join(workspace, '.backups'),
  path.join(home, '.openclaw', 'backups'),
  path.join(home, '.openclaw', 'workspace-backups')
);

const findings = [];
const recommendations = [];
const evidence = { workspace, backupRoots: [], keyFiles: {}, backupSamples: [] };
let score = 100;

const keyFiles = ['SOUL.md', 'USER.md', 'TOOLS.md', 'MEMORY.md', 'TODO.md', 'progress-log.md'];
for (const file of keyFiles) {
  const full = path.join(workspace, file);
  const exists = fs.existsSync(full);
  evidence.keyFiles[file] = exists;
  if (!exists && ['SOUL.md', 'USER.md', 'TOOLS.md'].includes(file)) {
    findings.push({ level: 'HIGH', area: 'workspace', issue: `missing core operator file: ${file}` });
    recommendations.push(`Restore or recreate ${file}; recovery confidence is weak without it.`);
    score -= 12;
  }
}

const memoryDir = path.join(workspace, 'memory');
if (!fs.existsSync(memoryDir)) {
  findings.push({ level: 'MEDIUM', area: 'workspace', issue: 'memory directory not found' });
  recommendations.push('Ensure the workspace memory directory is included in backups and recovery tests.');
  score -= 8;
}

function collectBackupEntries(root) {
  if (!fs.existsSync(root)) return [];
  try {
    return fs.readdirSync(root, { withFileTypes: true })
      .map((entry) => {
        const full = path.join(root, entry.name);
        const stat = fs.statSync(full);
        return { name: entry.name, full, isDirectory: entry.isDirectory(), mtimeMs: stat.mtimeMs, size: stat.size };
      })
      .sort((a, b) => b.mtimeMs - a.mtimeMs);
  } catch {
    return [];
  }
}

let newestBackupAgeHours = null;
let foundAnyBackupRoot = false;
let foundAnyBackupArtifact = false;
for (const root of [...new Set(backupRoots)]) {
  const exists = fs.existsSync(root);
  const entries = exists ? collectBackupEntries(root) : [];
  evidence.backupRoots.push({ root, exists, count: entries.length });
  if (exists) foundAnyBackupRoot = true;
  if (entries.length > 0) {
    foundAnyBackupArtifact = true;
    const newest = entries[0];
    const ageHours = (Date.now() - newest.mtimeMs) / 36e5;
    newestBackupAgeHours = newestBackupAgeHours == null ? ageHours : Math.min(newestBackupAgeHours, ageHours);
    evidence.backupSamples.push(...entries.slice(0, 3).map((e) => ({ root, name: e.name, isDirectory: e.isDirectory, mtime: new Date(e.mtimeMs).toISOString(), size: e.size })));
  }
}

if (!foundAnyBackupRoot) {
  findings.push({ level: 'HIGH', area: 'backup', issue: 'no candidate backup root found' });
  recommendations.push('Create and document a real backup location before trusting this deployment.');
  score -= 35;
}
if (foundAnyBackupRoot && !foundAnyBackupArtifact) {
  findings.push({ level: 'HIGH', area: 'backup', issue: 'backup root exists but contains no visible backup artifacts' });
  recommendations.push('Run a backup now and verify that the artifact lands in the expected location.');
  score -= 25;
}
if (newestBackupAgeHours != null) {
  evidence.newestBackupAgeHours = Number(newestBackupAgeHours.toFixed(1));
  if (newestBackupAgeHours > 168) {
    findings.push({ level: 'HIGH', area: 'backup-freshness', issue: 'newest backup appears older than 7 days' });
    recommendations.push('Create a fresh backup and rehearse restore before making risky changes.');
    score -= 20;
  } else if (newestBackupAgeHours > 48) {
    findings.push({ level: 'MEDIUM', area: 'backup-freshness', issue: 'newest backup appears older than 48 hours' });
    recommendations.push('Refresh backups more frequently if this workspace changes daily.');
    score -= 8;
  }
}

const runbookSignals = [
  path.join(workspace, 'docs', 'recovery.md'),
  path.join(workspace, 'docs', 'disaster-recovery.md'),
  path.join(workspace, 'scripts', 'skills-backup.sh'),
  path.join(workspace, 'skills', 'openclaw-backup-restore', 'SKILL.md')
];
const presentSignals = runbookSignals.filter((p) => fs.existsSync(p));
evidence.runbookSignals = presentSignals;
if (presentSignals.length === 0) {
  findings.push({ level: 'MEDIUM', area: 'runbook', issue: 'no recovery runbook or backup automation signal found' });
  recommendations.push('Document the restore path or automate it; tribal knowledge is not a recovery plan.');
  score -= 10;
}

const drillPlan = [
  `1. Restore the newest backup into a safe test path such as ${workspace}-drill`,
  '2. Verify core files and the memory directory exist after restore',
  '3. Verify OpenClaw can reach a basic startup or status-check state in the restored copy',
  '4. Record actual restore duration, blockers, and missing secrets/config',
  '5. Convert every manual surprise into a script or explicit runbook step'
];

let verdict = 'PASS';
if (score < 60 || findings.some((f) => f.level === 'HIGH')) verdict = 'FAIL';
else if (score < 85 || findings.some((f) => f.level === 'MEDIUM')) verdict = 'WARN';

const summary = verdict === 'PASS'
  ? 'Backup and restore posture looks usable for a lightweight drill.'
  : verdict === 'WARN'
    ? 'Recovery posture is partial; run a drill before trusting it.'
    : 'Recovery confidence is too weak; do not confuse backup presence with restore readiness.';

console.log(JSON.stringify({ score, verdict, summary, findings, recommendations, drillPlan, evidence }, null, 2));
process.exit(verdict === 'FAIL' ? 1 : 0);
