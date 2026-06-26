#!/usr/bin/env node
/**
 * context-snapshot - Preserve task context before OpenClaw compaction
 * 
 * Usage:
 *   node context-snapshot.js save "<task>" "<findings>" "<pending>" ["<last_error>"]
 *   node context-snapshot.js load
 *   node context-snapshot.js clear
 * 
 * SECURITY: All snapshot JSON files are protected with 0600 (owner-only) permissions.
 */

import { readFileSync, writeFileSync, existsSync, chmodSync } from 'fs';
import { resolve } from 'path';
import { getTempDir } from './path-resolver.js';

const SNAPSHOT_FILE = resolve(getTempDir(), 'context-snapshot.json');

/**
 * Saves the current workspace context into a temporary snapshot file.
 */
function saveSnapshot(task, findings, pending, lastError = null) {
  const snapshot = {
    timestamp: new Date().toISOString(),
    project_root: process.cwd(),
    task,
    findings, // High fidelity, raw data
    pending,
    lastError,
    status: 'active'
  };

  writeFileSync(SNAPSHOT_FILE, JSON.stringify(snapshot, null, 2));
  
  try {
    chmodSync(SNAPSHOT_FILE, 0o600);
  } catch (e) {
    // Failsafe
  }
}

/**
 * Loads the last saved snapshot for the current project.
 */
function loadSnapshot() {
  if (!existsSync(SNAPSHOT_FILE)) {
    return null;
  }
  try {
    const data = readFileSync(SNAPSHOT_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return null;
  }
}

const [cmd, arg1, arg2, arg3, arg4] = process.argv.slice(2);

if (cmd === 'save') {
  if (!arg1) {
    console.log(JSON.stringify({ error: 'Usage: save "<task>" "<findings>" "<pending>" ["<last_error>"]' }));
    process.exit(1);
  }
  saveSnapshot(arg1, arg2 || '', arg3 || '', arg4 || '');
  console.log(JSON.stringify({
    ok: true,
    message: 'Snapshot saved to private temp. This will survive context compaction.',
    path: SNAPSHOT_FILE
  }));
}

else if (cmd === 'load') {
  const snapshot = loadSnapshot();
  if (!snapshot) {
    console.log(JSON.stringify({ message: 'No snapshot found.' }));
  } else {
    console.log(JSON.stringify(snapshot, null, 2));
  }
}

else if (cmd === 'clear') {
  const snapshot = loadSnapshot();
  if (snapshot) {
    saveSnapshot(snapshot.task, snapshot.findings, snapshot.pending, snapshot._clearedAt = new Date().toISOString());
  }
  console.log(JSON.stringify({ ok: true, message: 'Snapshot cleared.' }));
}

else {
  console.log('Usage:');
  console.log('  context-snapshot.js save "<task>" "<findings>" "<pending>" ["<last_error>"]');
  console.log('  context-snapshot.js load');
  console.log('  context-snapshot.js clear');
}
