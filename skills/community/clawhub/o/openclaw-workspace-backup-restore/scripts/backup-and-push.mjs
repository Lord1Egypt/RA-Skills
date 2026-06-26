#!/usr/bin/env node

import { spawnSync } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_ROOT = path.resolve(__dirname, '..');
const BACKUP_DIR = process.env.OPENCLAW_BACKUP_DIR || path.join(os.homedir(), '.openclaw', 'backups', 'openclaw-backup-restore-clawlite');
const BACKUP_REPO_DIR = process.env.OPENCLAW_BACKUP_REPO_DIR || path.join(os.homedir(), '.openclaw', 'backup-repos', 'openclaw-backup-restore-clawlite');

const args = process.argv.slice(2);
const options = {
  branch: 'main',
  remote: 'clawlite-backup',
  message: null,
  rawOpenClawConfig: true
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--branch' && args[i + 1]) {
    options.branch = args[++i];
  } else if (args[i] === '--remote' && args[i + 1]) {
    options.remote = args[++i];
  } else if (args[i] === '--message' && args[i + 1]) {
    options.message = args[++i];
  } else if (args[i] === '--sanitized-config-only') {
    options.rawOpenClawConfig = false;
  }
}

function run(command, commandArgs, opts = {}) {
  const result = spawnSync(command, commandArgs, {
    stdio: 'pipe',
    encoding: 'utf8',
    ...opts
  });

  if (result.status !== 0) {
    const stderr = (result.stderr || '').trim();
    const stdout = (result.stdout || '').trim();
    const details = stderr || stdout || `exit ${result.status}`;
    throw new Error(`${command} ${commandArgs.join(' ')} failed: ${details}`);
  }

  return (result.stdout || '').trim();
}

function latestBackupDir() {
  const entries = fs.readdirSync(BACKUP_DIR, { withFileTypes: true })
    .filter(entry => entry.isDirectory() && entry.name !== 'named')
    .map(entry => entry.name)
    .sort();

  if (entries.length === 0) throw new Error('No backup directory found after backup run');
  return entries[entries.length - 1];
}

function ensureBackupRepo(remoteUrl) {
  if (!fs.existsSync(BACKUP_REPO_DIR)) {
    fs.mkdirSync(path.dirname(BACKUP_REPO_DIR), { recursive: true });
    run('git', ['clone', '--branch', options.branch, remoteUrl, BACKUP_REPO_DIR], { cwd: SKILL_ROOT });
    return;
  }

  if (!fs.existsSync(path.join(BACKUP_REPO_DIR, '.git'))) {
    throw new Error(`Backup repo dir exists but is not a git repo: ${BACKUP_REPO_DIR}`);
  }

  run('git', ['fetch', 'origin'], { cwd: BACKUP_REPO_DIR });
  run('git', ['checkout', options.branch], { cwd: BACKUP_REPO_DIR });
  run('git', ['pull', '--ff-only', 'origin', options.branch], { cwd: BACKUP_REPO_DIR });
}

function syncBackupsIntoRepo() {
  const target = path.join(BACKUP_REPO_DIR, 'backups');
  fs.rmSync(target, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(BACKUP_DIR, target, { recursive: true });
}

function main() {
  const backupArgs = ['scripts/backup.mjs'];
  if (options.rawOpenClawConfig) backupArgs.push('--raw-openclaw-config');

  console.log('🔍 Creating backup before git push...');
  run('node', backupArgs, { cwd: SKILL_ROOT });

  const latest = latestBackupDir();
  console.log(`✅ Latest backup: ${latest}`);

  const remoteUrl = run('git', ['remote', 'get-url', options.remote], { cwd: SKILL_ROOT });
  ensureBackupRepo(remoteUrl);
  syncBackupsIntoRepo();

  run('git', ['add', 'backups'], { cwd: BACKUP_REPO_DIR });

  const status = run('git', ['status', '--short', 'backups'], { cwd: BACKUP_REPO_DIR });
  if (!status) {
    console.log('ℹ️  No backup changes to commit.');
    return;
  }

  const message = options.message || `backup: ${latest}`;
  run('git', ['commit', '-m', message], { cwd: BACKUP_REPO_DIR });
  run('git', ['push', 'origin', options.branch], { cwd: BACKUP_REPO_DIR });

  console.log(`✅ Backup committed and pushed to ${remoteUrl} (${options.branch})`);
  console.log(`   Local backup repo: ${BACKUP_REPO_DIR}`);
  console.log(`   Commit message: ${message}`);
}

try {
  main();
} catch (error) {
  console.error(`❌ ${error.message}`);
  process.exit(1);
}
