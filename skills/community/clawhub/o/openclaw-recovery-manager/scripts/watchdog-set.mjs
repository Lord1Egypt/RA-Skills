#!/usr/bin/env node
// OpenClaw Emergency Rollback — watchdog-set.mjs
// Usage: node watchdog-set.mjs <minutes>
// Arms the watchdog for the given number of minutes.

import { join } from "path";
import { existsSync } from "fs";
import {
  ROLLBACK_DIR, WATCHDOG_FILE, CHANGE_LOG, RESTORE_LOG,
  writeJson, getManifest, appendLog, timestamp
} from './utils.mjs';

const minutes = parseInt(process.argv[2], 10);
if (!minutes || minutes <= 0) {
  console.error('Usage: node watchdog-set.mjs <minutes>');
  process.exit(1);
}

const now = Math.floor(Date.now() / 1000);
const expiry = now + minutes * 60;
const setAt = timestamp();
const expiryDate = new Date(expiry * 1000);
const expiryHuman = expiryDate.toISOString().replace(/\.\d+Z$/, 'Z');
const expiryDisplay = expiryDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

// Read target snapshot label
const manifest = getManifest();
const snap1 = manifest.snapshots.find(s => s.slot === 1);
const targetLabel = snap1 ? snap1.label : 'no snapshot saved';

// Write watchdog.json
writeJson(WATCHDOG_FILE, {
  armed: true,
  setAt,
  expiryEpoch: expiry,
  expiryHuman,
  minutesSet: minutes,
  targetSnapshot: 'snapshot-1',
  targetLabel
});


import { spawn } from 'child_process';
const timerScript = join(ROLLBACK_DIR, 'scripts', 'watchdog-timer.mjs');
if (existsSync(timerScript)) {
  const child = spawn(process.execPath, [timerScript, String(minutes)], {
    detached: true,
    stdio: 'ignore',
    env: { ...process.env, WATCHDOG_SOURCE: 'watchdog-set' }
  });
  child.unref();
  appendLog(RESTORE_LOG, `WATCHDOG SET — spawned watchdog timer pid=${child.pid || 'unknown'} minutes=${minutes}`);
} else {
  appendLog(RESTORE_LOG, "WATCHDOG SET ERROR — watchdog-timer.mjs missing, timer won't fire.");
  console.error("WARNING: watchdog-timer.mjs missing, timer won't fire.");
}

// Log
appendLog(CHANGE_LOG,
  `WATCHDOG ARMED\n  Minutes: ${minutes}\n  Expiry: ${expiryHuman}\n  Target: snapshot-1 — "${targetLabel}"`
);

console.log(`Watchdog armed — ${minutes} minutes. Expires at ${expiryDisplay}. Target: ${targetLabel}`);
