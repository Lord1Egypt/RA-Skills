'use strict';

// Tests for scripts/data.js — focused on the userId path-traversal guard.
// sanitizeId / safeUserPath call process.exit(1) on a bad id, so we exercise
// them in a child process and assert the non-zero exit + the error message.
// The happy-path (a valid id resolves under data/users/) runs in-process.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const { spawnSync } = require('child_process');

const DATA = path.join(__dirname, '../scripts/data.js');
const USERS_DIR = path.resolve(__dirname, '../data/users');

function runGuard(snippet) {
  return spawnSync(process.execPath, ['-e', `const d=require(${JSON.stringify(DATA)});${snippet}`], {
    encoding: 'utf8',
  });
}

test('sanitizeId rejects path-traversal userIds (exits non-zero)', () => {
  for (const bad of ['../etc/passwd', '..', 'a/../../b', 'foo/bar']) {
    const r = runGuard(`d.sanitizeId(${JSON.stringify(bad)})`);
    assert.notEqual(r.status, 0, `"${bad}" must be rejected`);
    assert.match(r.stderr, /Invalid userId/);
  }
});

test('safeUserPath rejects an id whose resolved path escapes data/users/ (exits non-zero)', () => {
  for (const escaping of ['../../etc/passwd', '../outside']) {
    const r = runGuard(`d.safeUserPath(${JSON.stringify(escaping)})`);
    assert.notEqual(r.status, 0, `"${escaping}" must be rejected by safeUserPath`);
    assert.match(r.stderr, /Illegal path/);
  }
});

test('sanitizeId rejects out-of-charset and over-length ids', () => {
  const tooLong = 'a'.repeat(129);
  for (const bad of ['has space', 'dollar$', tooLong, '']) {
    const r = runGuard(`d.sanitizeId(${JSON.stringify(bad)})`);
    assert.notEqual(r.status, 0, `"${bad}" must be rejected`);
  }
});

test('a valid userId resolves to a path under data/users/', () => {
  const { safeUserPath } = require('../scripts/data');
  const p = safeUserPath('self');
  assert.ok(p.startsWith(USERS_DIR + path.sep), 'resolved path must stay under data/users/');
  assert.ok(p.endsWith(`${path.sep}self.json`));
});

test('resolveUserId falls back to the default when no arg/env is given', () => {
  const { resolveUserId, DEFAULT_USER_ID } = require('../scripts/data');
  const saved = process.env.OPENCLAW_USER_ID;
  try {
    delete process.env.OPENCLAW_USER_ID;
    assert.equal(resolveUserId(null), DEFAULT_USER_ID);
    assert.equal(resolveUserId('  custom-1 '), 'custom-1');
  } finally {
    if (saved === undefined) delete process.env.OPENCLAW_USER_ID; else process.env.OPENCLAW_USER_ID = saved;
  }
});

// A state file written by an OLDER bundle — `seen` present, `sessionWindows`
// absent (design 2026-09-11 §B added the map) — must load through the real
// readJson/writeJson round-trip, and the first `fetch` must ADD the map without
// disturbing `seen` or `lastRunAt`. The file is removed afterwards.
test('an older bundle state file gains sessionWindows on the first fetch, leaving seen/lastRunAt untouched', async () => {
  const fs = require('fs');
  const { safeUserPath, readJson, writeJson } = require('../scripts/data');
  const { doFetch } = require('../scripts/brainstorming');

  const userId = `legacy-state-${process.pid}`;
  const file = safeUserPath(userId);
  const seen = { 'an-old-card|deadbeef': '2026-09-01T00:00:00.000Z' };
  const legacy = { userId, seen, lastRunAt: '2026-09-01T00:00:00.000Z' };
  writeJson(file, legacy);
  const nowIso = new Date().toISOString();

  try {
    assert.ok(!('sessionWindows' in readJson(file)), 'the legacy file has no map to start with');
    await doFetch(
      { token: 't', sessionFilter: null, kbdFilter: null, hours: 24, limit: 50, tz: 'America/Los_Angeles' },
      {
        httpGet: async () => ({
          sessions: [
            { session_id: 'aud-1', source: 'audio', started_at: '2026-06-09T19:05:00.000Z', ended_at: '2026-06-09T19:30:00.000Z' },
          ],
        }),
        now: () => nowIso,
        emit: () => {},
        load: () => readJson(file),
        save: (s) => writeJson(file, s),
      }
    );

    const after = readJson(file);
    assert.deepEqual(after.sessionWindows, {
      'aud-1': {
        started_at: '2026-06-09T19:05:00.000Z',
        ended_at: '2026-06-09T19:30:00.000Z',
        seen_at: nowIso,
      },
    });
    assert.deepEqual(after.seen, seen, '`seen` is carried through untouched');
    assert.equal(after.lastRunAt, legacy.lastRunAt, '`lastRunAt` stays push-owned');
    assert.equal(after.userId, userId);
  } finally {
    fs.rmSync(file, { force: true });
  }
});
