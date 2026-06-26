#!/usr/bin/env node
// OpenClaw Emergency Rollback — watchdog-extend.mjs
// Usage: node watchdog-extend.mjs <additional_minutes>

import {
  WATCHDOG_FILE, CHANGE_LOG,
  getWatchdog, writeJson, appendLog
} from './utils.mjs';

const addMinutes = parseInt(process.argv[2], 10);
if (!addMinutes || addMinutes <= 0) {
  console.error('Usage: node watchdog-extend.mjs <additional_minutes>');
  process.exit(1);
}

const watchdog = getWatchdog();
if (!watchdog.armed) {
  console.error('ERROR: Watchdog is not armed. Use watchdog-set first.');
  process.exit(1);
}

const oldExpiry = watchdog.expiryEpoch;
const newExpiry = oldExpiry + addMinutes * 60;
const newExpiryDate = new Date(newExpiry * 1000);
const newExpiryHuman = newExpiryDate.toISOString().replace(/\.\d+Z$/, 'Z');
const newExpiryDisplay = newExpiryDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

const now = Math.floor(Date.now() / 1000);
const remaining = Math.floor((newExpiry - now) / 60);

// Update watchdog.json
watchdog.expiryEpoch = newExpiry;
watchdog.expiryHuman = newExpiryHuman;
writeJson(WATCHDOG_FILE, watchdog);

// No need to touch the running timer process. It calls restore-if-armed.mjs,
// which reads expiry from watchdog.json dynamically when it fires.

appendLog(CHANGE_LOG,
  `WATCHDOG EXTENDED\n  Added: ${addMinutes} minutes\n  New expiry: ${newExpiryHuman}\n  Remaining: ~${remaining}m`
);

console.log(`Watchdog extended. New expiry: ${newExpiryDisplay} (~${remaining}m remaining)`);
