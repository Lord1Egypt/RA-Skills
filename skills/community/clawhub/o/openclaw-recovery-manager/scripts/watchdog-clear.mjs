#!/usr/bin/env node
// OpenClaw Emergency Rollback — watchdog-clear.mjs
// Disarms the watchdog. Called when user accepts changes.

import { execSync } from 'child_process';
import {
  WATCHDOG_FILE, CHANGE_LOG,
  getWatchdog, writeJson, appendLog
} from './utils.mjs';

const watchdog = getWatchdog();
const now = Math.floor(Date.now() / 1000);

// Calculate time remaining at disarm
let remainingMsg = 'unknown';
if (watchdog.expiryEpoch) {
  if (watchdog.expiryEpoch > now) {
    const secs = watchdog.expiryEpoch - now;
    remainingMsg = `${Math.floor(secs / 60)}m ${secs % 60}s`;
  } else {
    remainingMsg = 'already expired';
  }
}

// Disarm watchdog.json
watchdog.armed = false;
writeJson(WATCHDOG_FILE, watchdog);


// Kill any detached watchdog-timer.mjs processes
try {
  execSync('pkill -f watchdog-timer.mjs || true', { stdio: 'ignore' });
} catch {}

appendLog(CHANGE_LOG,
  `WATCHDOG DISARMED\n  Disarmed by: user accepted changes\n  Time remaining: ${remainingMsg}`
);

console.log(`Watchdog disarmed. Time remaining was: ${remainingMsg}`);
