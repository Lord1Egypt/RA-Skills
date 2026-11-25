'use strict';
// U4 — prefs, the ingest ledger and run state. R6 (TC-S6-10), R10 (TC-S6-11),
// R12 (TC-S4-6), R20 (TC-S6-9).
//
// Every test injects its own file paths. The bundle's own data/ belongs to
// whatever container the checkout is sitting in, where clobbering it would
// destroy a real run's only history (there is no server-side copy — see the
// module docblock).

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const state = require('../scripts/state.js');

const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'notebooklm-ingest-state-'));
process.on('exit', () => fs.rmSync(SCRATCH, { recursive: true, force: true }));

const T0 = Date.parse('2026-10-30T07:00:00Z');
const HOUR = 60 * 60 * 1000;

let seq = 0;
function deps(extra = {}) {
  seq += 1;
  const dir = path.join(SCRATCH, `run-${seq}`);
  return Object.assign({
    now: T0,
    paths: {
      prefs: path.join(dir, 'prefs.json'),
      ingests: path.join(dir, 'ingests.json'),
      run: path.join(dir, 'last-run.json'),
    },
  }, extra);
}

// ---------------------------------------------------------------------------
// R12 — the host field
// ---------------------------------------------------------------------------

test('R12 TC-S4-6: the host defaults to the per-user openclaw container', () => {
  const d = deps();
  assert.equal(state.readPrefs(d).host, 'openclaw-container');
  assert.equal(state.DEFAULT_HOST, 'openclaw-container');
});

test('R12 TC-S4-6: the host is settable and the change persists into a later read', () => {
  const d = deps();
  const out = state.setHost('javis-mac', d);
  assert.equal(out.ok, true);
  assert.equal(out.prefs.host, 'javis-mac');
  // A fresh read, as a later turn would do it.
  assert.equal(state.readPrefs(d).host, 'javis-mac', 'the setting must survive the turn');
  assert.equal(out.prefs.updated_at, '2026-10-30T07:00:00.000Z');
});

test('R12: javis-mac is the documented alternative, and the list is exactly two', () => {
  assert.deepEqual(state.HOSTS, ['openclaw-container', 'javis-mac']);
});

test('R12: an unknown host is refused with the allowed list, not stored', () => {
  const d = deps();
  const out = state.setHost('my-laptop', d);
  assert.equal(out.ok, false);
  assert.equal(out.error, 'unknown_host');
  assert.match(out.next, /openclaw-container or javis-mac/);
  assert.equal(state.readPrefs(d).host, 'openclaw-container', 'the typo must not become the setting');
});

test('R12: a prefs file carrying a bogus host reads back as the default', () => {
  const d = deps();
  state.writeJson(d.paths.prefs, { host: 'nowhere', notebooks: 'not-an-array' });
  const prefs = state.readPrefs(d);
  assert.equal(prefs.host, 'openclaw-container');
  assert.deepEqual(prefs.notebooks, []);
});

test('R13: the schedule and timezone live beside the host and round-trip', () => {
  const d = deps();
  state.writePrefs({ schedule: '0 7 * * *', tz: 'America/Los_Angeles', notebooks: ['nb-1'] }, d);
  const prefs = state.readPrefs(d);
  assert.equal(prefs.schedule, '0 7 * * *');
  assert.equal(prefs.tz, 'America/Los_Angeles');
  assert.deepEqual(prefs.notebooks, ['nb-1']);
  assert.equal(prefs.host, 'openclaw-container', 'an unrelated write must not reset the host');
});

// ---------------------------------------------------------------------------
// R6 — the ingest ledger
// ---------------------------------------------------------------------------

test('R6 TC-S6-10: a row carries notebook, note, trigger, date and page count', () => {
  const d = deps();
  const row = state.appendIngest({
    notebook: 'Thermodynamics', note: '新建记事', source_id: 'u-1', trigger: 'schedule', pages: 3,
  }, d);
  assert.deepEqual(Object.keys(row).sort(), ['date', 'note', 'notebook', 'pages', 'source_id', 'trigger']);
  assert.equal(row.date, '2026-10-30T07:00:00.000Z');
  assert.equal(row.pages, 3);
});

test('R6 TC-S6-10: three ingests from three triggers come back newest first', () => {
  const d = deps();
  state.appendIngest({ notebook: 'A', note: 'one', trigger: 'chat', pages: 1, date: '2026-10-28T10:00:00.000Z' }, d);
  state.appendIngest({ notebook: 'B', note: 'two', trigger: 'schedule', pages: 2, date: '2026-10-29T10:00:00.000Z' }, d);
  state.appendIngest({ notebook: 'C', note: 'three', trigger: 'hand-fed', pages: 4, date: '2026-10-30T10:00:00.000Z' }, d);

  const rows = state.readIngests(d);
  assert.deepEqual(rows.map((r) => r.note), ['three', 'two', 'one']);
  assert.deepEqual(rows.map((r) => r.trigger), ['hand-fed', 'schedule', 'chat']);
});

test('R6: an absent or corrupt ledger reads as empty history, not as an error', () => {
  const d = deps();
  assert.deepEqual(state.readIngests(d), []);
  fs.mkdirSync(path.dirname(d.paths.ingests), { recursive: true });
  fs.writeFileSync(d.paths.ingests, '{not json');
  assert.deepEqual(state.readIngests(d), []);
  fs.writeFileSync(d.paths.ingests, '{"rows":[]}');
  assert.deepEqual(state.readIngests(d), []);
});

test('R6: a missing trigger is recorded as unknown rather than guessed', () => {
  const d = deps();
  assert.equal(state.appendIngest({ notebook: 'A', note: 'x' }, d).trigger, 'unknown');
});

test('R6: the ledger is bounded, and the oldest rows are the ones that go', () => {
  const d = deps();
  for (let i = 0; i < state.MAX_INGESTS + 5; i += 1) {
    state.appendIngest({
      notebook: 'A', note: `n${i}`, trigger: 'chat', pages: 1,
      date: new Date(T0 + i * 1000).toISOString(),
    }, d);
  }
  const rows = state.readIngests(d);
  assert.equal(rows.length, state.MAX_INGESTS);
  assert.equal(rows[0].note, `n${state.MAX_INGESTS + 4}`, 'newest kept');
  assert.equal(rows.some((r) => r.note === 'n0'), false, 'oldest dropped');
});

// ---------------------------------------------------------------------------
// R10 / R20 — run state
// ---------------------------------------------------------------------------

test('R10: startRun overwrites and mergeRun merges, so an empty run still has state', () => {
  const d = deps();
  state.startRun({ trigger: 'schedule', notebooks: ['nb-1'], fetched: 0 }, d);
  assert.equal(state.readRun(d).fetched, 0);

  state.mergeRun({ pushed: 2, pages: [{ title: 'Entropy', status: 'new' }] }, d);
  const run = state.readRun(d);
  assert.equal(run.trigger, 'schedule', 'the merge must not drop what startRun wrote');
  assert.equal(run.pushed, 2);
  assert.equal(run.pages[0].status, 'new');

  // And a second start wipes the previous run rather than blending the two.
  state.startRun({ trigger: 'chat' }, d);
  assert.equal(state.readRun(d).pushed, undefined);
});

test('R10 TC-S6-11: the trigger is recorded, so a scheduled run can name what started it', () => {
  const d = deps();
  state.startRun({ trigger: 'schedule' }, d);
  const got = state.runForReport(d);
  assert.equal(got.ok, true);
  assert.equal(got.state.trigger, 'schedule');
});

test('R10: no run state is no_recent_run, with a next action and no digest', () => {
  const out = state.runForReport(deps());
  assert.equal(out.ok, false);
  assert.equal(out.error, 'no_recent_run');
  assert.match(out.next, /do not invent a digest/);
});

test('R10: a run older than six hours is stale_run, and the boundary is exact', () => {
  const d = deps();
  state.startRun({ trigger: 'schedule' }, d);

  const atLimit = state.runForReport(Object.assign({}, d, { now: T0 + state.STALE_AFTER_MS }));
  assert.equal(atLimit.ok, true, 'exactly six hours is still this run');

  const past = state.runForReport(Object.assign({}, d, { now: T0 + state.STALE_AFTER_MS + 1 }));
  assert.equal(past.ok, false);
  assert.equal(past.error, 'stale_run');
  assert.equal(past.started_at, '2026-10-30T07:00:00.000Z');
  assert.equal(state.STALE_AFTER_MS, 6 * HOUR);
});

test('R10: an unparseable started_at is stale_run, not a run dated zero', () => {
  const d = deps();
  state.writeJson(d.paths.run, { started_at: 'yesterday-ish', trigger: 'schedule' });
  assert.equal(state.runForReport(d).error, 'stale_run');
});

test('R10: clearRun removes the file and is safe to call twice', () => {
  const d = deps();
  state.startRun({ trigger: 'chat' }, d);
  assert.equal(state.clearRun(d), true);
  assert.equal(state.clearRun(d), false);
  assert.equal(state.readRun(d), null);
});

// ---------------------------------------------------------------------------
// Durability
// ---------------------------------------------------------------------------

test('writes are tmp-then-rename, leaving no .tmp behind', () => {
  const d = deps();
  state.writePrefs({ notebooks: ['a'] }, d);
  const dir = path.dirname(d.paths.prefs);
  assert.deepEqual(fs.readdirSync(dir), ['prefs.json']);
});

test('a failed state write never throws at the caller (a good push must not become a failure)', () => {
  // A path whose parent is a FILE: mkdirSync fails, so the write cannot happen.
  const blocker = path.join(SCRATCH, 'blocker');
  fs.writeFileSync(blocker, 'not a directory');
  const d = { now: T0, paths: { prefs: path.join(blocker, 'prefs.json'), ingests: path.join(blocker, 'i.json'), run: path.join(blocker, 'r.json') } };
  assert.doesNotThrow(() => state.appendIngest({ notebook: 'A', note: 'x', trigger: 'chat' }, d));
  assert.doesNotThrow(() => state.startRun({ trigger: 'chat' }, d));
  assert.equal(state.saveJson(path.join(blocker, 'x.json'), {}), false);
});

test('the bundle\'s own paths resolve against the module directory, not cwd', () => {
  // A cron turn's cwd is not the bundle (gmail-wiki-ingest's STATE_PATH note).
  for (const file of Object.values(state.PATHS)) {
    assert.ok(path.isAbsolute(file), file);
    assert.equal(path.dirname(file), state.DATA_DIR);
  }
  assert.equal(path.basename(state.DATA_DIR), 'data');
});

test('every refusal code carries one reason and one next action (R4, R5)', () => {
  for (const [code, r] of Object.entries(state.REFUSALS)) {
    assert.match(code, /^[a-z][a-z0-9_]*$/);
    assert.ok(r.reason && !r.reason.includes('\n'));
    assert.ok(r.next && r.next.length > 10);
  }
});
