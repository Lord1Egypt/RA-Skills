#!/usr/bin/env node
/**
 * check-session.js
 * 
 * Check if a session exists without launching it
 * 
 * Usage:
 *   node check-session.js <platform> [account]
 * 
 * Exit codes:
 *   0 = Session exists
 *   1 = Session does not exist
 * 
 * Output:
 *   JSON object with { exists, platform, account, path }
 */

const { hasSession } = require(
  process.env.OTO_PATH ? 
    `${process.env.OTO_PATH}/lib/session-manager` : 
    `${require('path').join(require('os').homedir(), 'oto/lib/session-manager')}`
);
const path = require('path');

const platform = process.argv[2];
const account = process.argv[3] || 'default';

if (!platform) {
  console.error('Usage: node check-session.js <platform> [account]');
  process.exit(1);
}

const exists = hasSession(platform, account);
const sessionPath = path.join(
  process.env.OTO_PATH || path.join(require('os').homedir(), 'oto'),
  'sessions',
  `${platform}--${account}.json`
);

console.log(JSON.stringify({
  exists,
  platform,
  account,
  path: sessionPath
}, null, 2));

process.exit(exists ? 0 : 1);
