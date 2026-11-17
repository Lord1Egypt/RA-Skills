#!/usr/bin/env node
/**
 * Clear the stored PowPow session (removes the local JWT file).
 * Run this when you are done, or on a shared machine.
 *
 * Usage: node logout.js
 */
const { clearSession, SESSION_PATH } = require('./lib/api-client');
const fs = require('fs');

if (fs.existsSync(SESSION_PATH)) {
  clearSession();
  console.log(`✅ Logged out. Session file removed: ${SESSION_PATH}`);
} else {
  console.log('No active session - nothing to do.');
}
