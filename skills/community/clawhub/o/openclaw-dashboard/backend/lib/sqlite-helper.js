'use strict';
/**
 * Shared SQLite helper — uses sqlite3 CLI (no native deps).
 */
const { execFileSync } = require('child_process');

/**
 * Run a SQL query against a SQLite DB and return parsed JSON rows.
 * @param {string} dbFile - Absolute path to .sqlite/.db file
 * @param {string} sql    - SQL query
 * @returns {Array<Object>}
 */
function sqliteJson(dbFile, sql) {
  const out = execFileSync('sqlite3', ['-json', dbFile, sql], { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 });
  const txt = String(out || '').trim();
  if (!txt) return [];
  return JSON.parse(txt);
}

/**
 * Run a SQL query and return a single scalar value.
 */
function sqliteScalar(dbFile, sql) {
  const out = execFileSync('sqlite3', [dbFile, sql], { encoding: 'utf8', maxBuffer: 4 * 1024 * 1024 });
  const txt = String(out || '').trim();
  if (!txt) return null;
  const line = txt.split(/\r?\n/)[0].trim();
  if (line === '') return null;
  const n = Number(line);
  return Number.isNaN(n) ? line : n;
}

module.exports = { sqliteJson, sqliteScalar };
