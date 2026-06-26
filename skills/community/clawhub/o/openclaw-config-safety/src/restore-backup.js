/**
 * restore-backup.js — Backup and restore helpers
 *
 * Creates timestamped backups before any write operation.
 * Provides restore-from-latest-backup functionality.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const CONFIG_PATH = process.env.OPENCLAW_CONFIG || `${process.env.HOME}/.openclaw/openclaw.json`;

/**
 * Create a timestamped backup of the current config.
 * @returns {{ backupPath: string, timestamp: string }}
 */
function createBackup() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const backupPath = `${CONFIG_PATH}.bak-${timestamp}`;
  try {
    fs.copyFileSync(CONFIG_PATH, backupPath);
  } catch (err) {
    if (err.code !== "ENOENT") throw err;
    // Config doesn't exist yet — nothing to backup
  }
  return { backupPath, timestamp };
}

/**
 * Restore from the most recent backup matching the timestamp pattern.
 * @param {string} timestamp — ISO timestamp used in backup filename
 * @returns {boolean} true if restored successfully
 */
function restoreBackup(timestamp) {
  const backupPath = `${CONFIG_PATH}.bak-${timestamp}`;
  if (!fs.existsSync(backupPath)) {
    console.error(`Backup not found: ${backupPath}`);
    return false;
  }
  fs.copyFileSync(backupPath, CONFIG_PATH);
  return true;
}

/**
 * List available backups for this config.
 * @returns {{ timestamp: string, path: string }[]}
 */
function listBackups() {
  const dir = path.dirname(CONFIG_PATH);
  const base = path.basename(CONFIG_PATH);
  const prefix = `${base}.bak-`;
  try {
    const files = fs.readdirSync(dir)
      .filter((f) => f.startsWith(prefix))
      .sort()
      .reverse();
    return files.map((f) => ({
      timestamp: f.slice(prefix.length),
      path: path.join(dir, f),
    }));
  } catch {
    return [];
  }
}

module.exports = { createBackup, restoreBackup, listBackups, CONFIG_PATH };
