// OpenClaw Emergency Rollback — shared utilities
// All JSON I/O goes through here. No string interpolation of user data into code.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';

const HOME = process.env.HOME || '/root';

export const ROLLBACK_DIR = join(HOME, '.openclaw/rollback');
export const CONFIG_FILE = join(ROLLBACK_DIR, 'rollback-config.json');
export const MANIFEST_FILE = join(ROLLBACK_DIR, 'manifest.json');
export const WATCHDOG_FILE = join(ROLLBACK_DIR, 'watchdog.json');
export const CHANGE_LOG = join(ROLLBACK_DIR, 'logs', 'change.log');
export const RESTORE_LOG = join(ROLLBACK_DIR, 'logs', 'restore.log');
export const SNAPSHOTS_DIR = join(ROLLBACK_DIR, 'snapshots');
export const RECOVERY_FILE = join(ROLLBACK_DIR, 'openclaw.recovery');

export function readJson(filepath) {
  try {
    return JSON.parse(readFileSync(filepath, 'utf8'));
  } catch {
    return null;
  }
}

export function writeJson(filepath, data) {
  mkdirSync(dirname(filepath), { recursive: true });
  writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
}

export function getConfig() {
  const config = readJson(CONFIG_FILE);
  if (!config) {
    console.error('ERROR: rollback-config.json not found. Run setup first.');
    process.exit(1);
  }
  return config;
}

export function getOpenclawHome() {
  const config = getConfig();
  return (config.openclawHome || '~/.openclaw').replace('~', HOME);
}

export function getOpenclawJson() {
  return join(getOpenclawHome(), 'openclaw.json');
}

export function getManifest() {
  return readJson(MANIFEST_FILE) || { watchdog_target: 'snapshot-1', snapshots: [] };
}

export function getWatchdog() {
  return readJson(WATCHDOG_FILE) || { armed: false };
}

export function appendLog(logFile, entry) {
  const ts = new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, '');
  mkdirSync(dirname(logFile), { recursive: true });
  const existing = existsSync(logFile) ? readFileSync(logFile, 'utf8') : '';
  writeFileSync(logFile, existing + `[${ts}] ${entry}\n---\n`);
}

export function timestamp() {
  return new Date().toISOString().replace(/\.\d+Z$/, 'Z');
}

export function timestampHuman() {
  return new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, '');
}
