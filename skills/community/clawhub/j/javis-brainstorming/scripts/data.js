#!/usr/bin/env node
/**
 * brainstorming — shared data helpers
 * Mirrors calendar-extractor/scripts/data.js. Boilerplate; path safety lives here.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

// Each HiJavis user runs in their own openclaw container with its own gateway
// token and data volume, so a per-container constant gives correct isolation.
// The userId is only a local dedup-state filename — server calls authenticate
// via OPENCLAW_GATEWAY_TOKEN, not this value.
const DEFAULT_USER_ID = 'self';

function sanitizeId(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) {
    console.error('❌ Invalid userId: letters/digits/-/_ only, length 1-128');
    process.exit(1);
  }
  return value;
}

function safeUserPath(userId) {
  const resolved = path.resolve(USERS_DIR, `${userId}.json`);
  if (!resolved.startsWith(path.resolve(USERS_DIR) + path.sep)) {
    console.error('❌ Illegal path');
    process.exit(1);
  }
  return resolved;
}

// Resolve a userId from an optional CLI arg. Falls back to OPENCLAW_USER_ID
// (forward-compat — unset today) and finally the DEFAULT_USER_ID constant, so
// the skill runs zero-config when invoked interactively without an explicit ID.
function resolveUserId(rawArg) {
  const candidate = (rawArg && String(rawArg).trim())
    || process.env.OPENCLAW_USER_ID
    || DEFAULT_USER_ID;
  return sanitizeId(candidate);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

// Atomic write: serialize to a sibling .tmp file then rename over the target.
// rename(2) is atomic on the same filesystem, so a kill mid-write can never
// leave a half-written (and thus unparseable) state file behind.
function writeJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tmp = `${filePath}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, filePath);
}

module.exports = { sanitizeId, safeUserPath, readJson, writeJson, resolveUserId, DEFAULT_USER_ID };
