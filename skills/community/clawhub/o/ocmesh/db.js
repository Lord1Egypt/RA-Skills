/**
 * db.js
 * SQLite setup using Node.js built-in node:sqlite (Node 22.5+).
 */

const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const os = require('os');
const fs = require('fs');

const DATA_DIR = path.join(os.homedir(), '.ocmesh');
fs.mkdirSync(DATA_DIR, { recursive: true });

const db = new DatabaseSync(path.join(DATA_DIR, 'ocmesh.db'));

db.exec(`
  CREATE TABLE IF NOT EXISTS identity (
    sk TEXT NOT NULL,
    pk TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS peers (
    pk          TEXT PRIMARY KEY,
    first_seen  INTEGER NOT NULL,
    last_seen   INTEGER NOT NULL,
    handshake   INTEGER DEFAULT 0,
    meta        TEXT
  );

  CREATE TABLE IF NOT EXISTS messages (
    id            TEXT PRIMARY KEY,
    from_pk       TEXT NOT NULL,
    to_pk         TEXT NOT NULL,
    content       TEXT NOT NULL,
    msg_type      TEXT DEFAULT 'text',
    received_at   INTEGER NOT NULL,
    read          INTEGER DEFAULT 0,
    delivered     INTEGER DEFAULT 0,
    read_by_peer  INTEGER DEFAULT 0
  );
`);

module.exports = db;
