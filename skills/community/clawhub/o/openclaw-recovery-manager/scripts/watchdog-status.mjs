#!/usr/bin/env node
// OpenClaw Emergency Rollback — watchdog-status.mjs
// Reports current watchdog state and time remaining.

import { existsSync } from 'fs';
import { WATCHDOG_FILE, getWatchdog } from './utils.mjs';

if (!existsSync(WATCHDOG_FILE)) {
  console.log('NOT ARMED (no watchdog.json found)');
  process.exit(0);
}

const watchdog = getWatchdog();

if (!watchdog.armed) {
  console.log('NOT ARMED');
  process.exit(0);
}

const now = Math.floor(Date.now() / 1000);
const expiry = watchdog.expiryEpoch || 0;
const remaining = expiry - now;

if (remaining <= 0) {
  console.log('ARMED — timer expired, restore pending');
} else {
  const mins = Math.floor(remaining / 60);
  const secs = remaining % 60;
  console.log(`ARMED — ${mins}m ${secs}s remaining`);
}

console.log(`Target: ${watchdog.targetSnapshot || 'snapshot-1'} — "${watchdog.targetLabel || 'unknown'}"`);
console.log(`Expiry: ${watchdog.expiryHuman || 'unknown'}`);
