#!/usr/bin/env node
// Combined config update + dashboard refresh in a single script.
// Reduces LLM round-trips: one command instead of two sequential scripts.
//
// Usage: node config-handler.js <field> [value]
//   Toggle:  node config-handler.js preset
//   Value:   node config-handler.js protection medium
//   Value:   node config-handler.js bidprice 75

'use strict';

const fs   = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const field = process.argv[2];
const value = process.argv[3];

if (!field) {
  process.stderr.write('[ConfigHandler] Usage: config-handler.js <field> [value]\n');
  process.exit(1);
}

// Step 1: Update config
const updateArgs = [path.join(__dirname, 'config-update.js'), field];
if (value) updateArgs.push(value);
try {
  execFileSync('node', updateArgs, { stdio: 'inherit' });
} catch (err) {
  process.stderr.write(`[ConfigHandler] config-update failed: ${err.message}\n`);
  process.exit(1);
}

// Step 2: Refresh dashboard (edit-in-place if messageId exists)
const DASHBOARD_MSGID_PATH = '/tmp/dashboard_msgid.txt';
const dashArgs = [path.join(__dirname, 'dashboard.js')];
if (fs.existsSync(DASHBOARD_MSGID_PATH)) {
  const msgId = fs.readFileSync(DASHBOARD_MSGID_PATH, 'utf-8').trim();
  if (msgId) dashArgs.push('--message-id', msgId);
}
try {
  execFileSync('node', dashArgs, { stdio: 'inherit' });
} catch (_) {
  // Dashboard refresh failure is non-blocking
}
