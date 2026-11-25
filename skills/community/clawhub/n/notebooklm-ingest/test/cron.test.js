'use strict';
// U5 — openclaw cron registration. R13 (TC-S4-4), R22 (TC-S4-5).
//
// The deployed binary is 2026.5.12-beta.1, which rejects the positional
// `cron add "<expr>" "<prompt>"` form openclaw's docs still show. A cron that
// fails to register fails SILENTLY — no job, no run, no error — so the argv
// shape is asserted element by element rather than by spot-checking a flag.

const { test } = require('node:test');
const assert = require('node:assert/strict');

const cron = require('../scripts/cron.js');

// ---------------------------------------------------------------------------
// R13 — the add argv
// ---------------------------------------------------------------------------

test('R13 TC-S4-4: cron add is built from flags, in full, never from positionals', () => {
  const argv = cron.buildCronAdd({ cron: '0 7 * * *', tz: 'America/Los_Angeles' });
  assert.deepEqual(argv.slice(0, 2), ['cron', 'add']);

  // Every flag the trigger contract requires, with its value.
  const pairs = {};
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i].startsWith('--')) pairs[argv[i]] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true;
  }
  assert.equal(pairs['--name'], cron.JOB_NAME);
  assert.equal(pairs['--cron'], '0 7 * * *');
  assert.equal(pairs['--agent'], 'main');
  assert.equal(pairs['--session'], 'isolated');
  assert.equal(pairs['--tz'], 'America/Los_Angeles');
  assert.equal(pairs['--no-deliver'], true);
  assert.equal(typeof pairs['--message'], 'string');

  // And nothing is positional: every element after `cron add` is a flag or a
  // flag's value.
  assert.equal(argv[2], '--name', 'the first thing after the verb must be a flag');
});

test('R13: --tz is omitted entirely when the zone is unknown, so openclaw defaults', () => {
  const argv = cron.buildCronAdd({ cron: '0 7 * * *' });
  assert.equal(argv.includes('--tz'), false);
  // But a zone that IS known must be passed, or the job fires in UTC.
  assert.ok(cron.buildCronAdd({ cron: '0 7 * * *', tz: 'Asia/Shanghai' }).includes('--tz'));
});

test('R13: a missing schedule throws rather than defaulting to some hour', () => {
  assert.throws(() => cron.buildCronAdd({}), /--cron is required/);
  assert.throws(() => cron.buildCronAdd({ cron: '   ' }), /--cron is required/);
});

test('R13: a missing name or message throws (openclaw keys by name; a turn has no dispatcher)', () => {
  assert.throws(() => cron.buildCronAdd({ cron: '0 7 * * *', name: '' }), /--name is required/);
  assert.throws(() => cron.buildCronAdd({ cron: '0 7 * * *', message: '' }), /--message is required/);
});

test('R13: the non-flags --schedule / --command are refused however they arrive', () => {
  assert.deepEqual(cron.INVALID_FLAGS, ['--schedule', '--command']);
  assert.throws(() => cron.buildCronAdd({ cron: '--schedule 0 7 * * *' }), /not an openclaw cron flag/);
  assert.throws(() => cron.buildCronAdd({ cron: '0 7 * * *', message: 'do it --command x' }), /not an openclaw cron flag/);
  assert.throws(() => cron.buildCronAdd({ cron: '0 7 * * *', name: 'x --schedule' }), /not an openclaw cron flag/);
  // And the constructor itself never emits one.
  const argv = cron.buildCronAdd({ cron: '0 7 * * *' });
  for (const flag of cron.INVALID_FLAGS) assert.equal(argv.includes(flag), false);
});

test('R13: a hostile schedule string stays one argv element', () => {
  const argv = cron.buildCronAdd({ cron: '0 7 * * * ; rm -rf /' });
  assert.equal(argv.filter((a) => a.includes('rm -rf')).length, 1);
});

test('R13: the baked message spells out the steps and names report as the only output path', () => {
  // A cron turn gets no body.tools from javis-server, so chat_emit_* is absent
  // on it and `report` is all it has. The message has to say so, because the
  // bundle alone cannot reach a job whose text was baked at registration.
  assert.match(cron.MESSAGE, /notebooklm-ingest\/SKILL\.md/);
  assert.match(cron.MESSAGE, /"trigger":"schedule"/);
  assert.match(cron.MESSAGE, /report/);
  assert.match(cron.MESSAGE, /no chat_emit_\* tools/);
  assert.match(cron.MESSAGE, /fetched nothing/, 'the empty-run rule must survive into the baked prompt');
});

test('R13: the baked message can actually run — fetch is given its stdin', () => {
  // The -v1 message said `fetch --trigger schedule` and nothing else. fetch
  // refuses without `{"notes":[…]}` on stdin, so the daily job produced
  // bad_input every morning and ingested nothing, silently. A prompt that
  // cannot complete its own first step is the failure here, and it is only
  // visible by reading the prompt against the command's contract.
  const steps = cron.MESSAGE.split('\n');
  const fetchStep = steps.find((l) => /notebooklm-ingest\.js fetch/.test(l));
  assert.ok(fetchStep, 'the message must name fetch');
  const piped = steps.find((l) => /\| node scripts\/notebooklm-ingest\.js fetch/.test(l));
  assert.ok(piped, 'fetch reads stdin: the message must show the note ids being piped in');
  assert.match(cron.MESSAGE, /"notes":\[\{"id"/, 'the stdin shape fetch validates');
  // And the selection it fetches FROM has to come from somewhere.
  assert.match(cron.MESSAGE, /notebooks/, 'the run reads the user\'s selected notebooks');
  assert.match(cron.MESSAGE, /notes --notebook/);
  assert.match(cron.MESSAGE, /do not pick notebooks on their behalf/);
});

test('R13: the message version and the legacy list moved together', () => {
  // Rule 3 of this module: a message baked at registration can only be
  // replaced by a new NAME, so every superseded name stays listed or a dormant
  // container keeps firing a prompt that cannot work.
  assert.equal(cron.JOB_NAME, 'notebooklm-ingest-daily-v2');
  assert.ok(cron.LEGACY_NAMES.includes('notebooklm-ingest-daily-v1'));
});

test('R13: the job name is versioned, with a legacy list beside it', () => {
  assert.match(cron.JOB_NAME, /-v\d+$/, 'a message baked at registration can only be replaced by a new name');
  assert.ok(Array.isArray(cron.LEGACY_NAMES));
  assert.equal(cron.LEGACY_NAMES.includes(cron.JOB_NAME), false, 'the current name is never its own legacy');
});

// ---------------------------------------------------------------------------
// list and remove
// ---------------------------------------------------------------------------

test('R13: list asks for json and all jobs; remove is positional by id', () => {
  assert.deepEqual(cron.buildCronList(), ['cron', 'list', '--json', '--all']);
  assert.deepEqual(cron.buildCronRemove('job-7'), ['cron', 'remove', 'job-7']);
});

test('R13: remove refuses an empty id and refuses a flag dressed as one', () => {
  assert.throws(() => cron.buildCronRemove(''), /job id is required/);
  assert.throws(() => cron.buildCronRemove('--name'), /not a flag/);
});

test('R13: the job listing parses a bare array, a {jobs} object, and junk', () => {
  assert.deepEqual(
    cron.parseJobs('[{"id":"a","name":"n","cron":"0 7 * * *"}]'),
    [{ id: 'a', name: 'n', cron: '0 7 * * *' }],
  );
  assert.equal(cron.parseJobs('{"jobs":[{"id":"b","name":"m","schedule":"0 8 * * *"}]}')[0].cron, '0 8 * * *');
  assert.deepEqual(cron.parseJobs('not json'), []);
  assert.deepEqual(cron.parseJobs(''), []);
  assert.deepEqual(cron.parseJobs('{"ok":true}'), []);
});

// ---------------------------------------------------------------------------
// R13 — the plan, and its ordering
// ---------------------------------------------------------------------------

test('R13 TC-S4-4: a fresh container gets one add and nothing else', () => {
  const plan = cron.planRegistration({ cron: '0 7 * * *', tz: 'America/Los_Angeles', jobs: [] });
  assert.equal(plan.status, 'create');
  assert.ok(plan.add);
  assert.deepEqual(plan.replace, []);
  assert.deepEqual(plan.remove, []);
});

test('R13: re-registering the same name at the same schedule is a no-op', () => {
  const jobs = [{ id: 'j1', name: cron.JOB_NAME, cron: '0 7 * * *' }];
  const plan = cron.planRegistration({ cron: '0 7 * * *', jobs });
  assert.equal(plan.status, 'unchanged');
  assert.equal(plan.add, null, 'idempotent: no second add for a job that already matches');
  assert.deepEqual(plan.remove, []);
  // And it stays a no-op however many times it is run.
  assert.deepEqual(cron.planRegistration({ cron: ' 0 7 * * * ', jobs }).add, null, 'whitespace is not a change');
});

test('R13: a schedule change removes the same-named job FIRST, then adds', () => {
  // openclaw keys a job by name, so an add under an existing name is a no-op —
  // the old job has to go before the new schedule can land.
  const plan = cron.planRegistration({
    cron: '30 20 * * *',
    jobs: [{ id: 'j1', name: cron.JOB_NAME, cron: '0 7 * * *' }],
  });
  assert.equal(plan.status, 'replace');
  assert.deepEqual(plan.replace, [['cron', 'remove', 'j1']]);
  assert.ok(plan.add.includes('30 20 * * *'));
});

test('R13: legacy jobs are removed AFTER the add, so a failed add leaves a job standing', () => {
  const plan = cron.planRegistration({
    cron: '0 7 * * *',
    jobs: [{ id: 'old', name: 'notebooklm-ingest-daily-v0', cron: '0 6 * * *' }],
    legacy: ['notebooklm-ingest-daily-v0'],
  });
  assert.ok(plan.add, 'the add comes first');
  assert.deepEqual(plan.remove, [['cron', 'remove', 'old']]);
  assert.deepEqual(plan.replace, [], 'a legacy name is not the same-name replace case');
});

test('R13: a container holding only a legacy job still converges without a duplicate add', () => {
  const plan = cron.planRegistration({
    cron: '0 7 * * *',
    jobs: [
      { id: 'cur', name: cron.JOB_NAME, cron: '0 7 * * *' },
      { id: 'old', name: 'notebooklm-ingest-daily-v0', cron: '0 6 * * *' },
    ],
    legacy: ['notebooklm-ingest-daily-v0'],
  });
  assert.equal(plan.status, 'legacy_only');
  assert.equal(plan.add, null);
  assert.deepEqual(plan.remove, [['cron', 'remove', 'old']]);
});

test('R13: duplicate jobs under the current name are collapsed to one', () => {
  const plan = cron.planRegistration({
    cron: '0 7 * * *',
    jobs: [
      { id: 'a', name: cron.JOB_NAME, cron: '0 7 * * *' },
      { id: 'b', name: cron.JOB_NAME, cron: '0 7 * * *' },
    ],
  });
  assert.equal(plan.status, 'replace');
  assert.equal(plan.replace.length, 2);
  assert.ok(plan.add);
});

test('R13: no schedule is a named refusal with a next action, not an exception', () => {
  const plan = cron.planRegistration({ jobs: [] });
  assert.equal(plan.ok, false);
  assert.equal(plan.error, 'schedule_missing');
  assert.match(plan.next, /ask the user for a time/);
});

test('R13: schedule --off removes every job this skill owns and adds nothing', () => {
  const plan = cron.planRemoval({
    jobs: [
      { id: 'cur', name: cron.JOB_NAME, cron: '0 7 * * *' },
      { id: 'old', name: 'notebooklm-ingest-daily-v0', cron: '0 6 * * *' },
      { id: 'other', name: 'gmail-wiki-ingest-daily-v3', cron: '0 7 * * *' },
    ],
    legacy: ['notebooklm-ingest-daily-v0'],
  });
  assert.equal(plan.status, 'remove');
  assert.deepEqual(plan.remove, [['cron', 'remove', 'cur'], ['cron', 'remove', 'old']]);
  assert.equal(plan.add, null);
  assert.equal(
    plan.remove.some((argv) => argv.includes('other')), false,
    'another skill\'s job is never touched',
  );
});

test('R13: schedule --off on a container with no job is absent, not an error', () => {
  const plan = cron.planRemoval({ jobs: [] });
  assert.equal(plan.status, 'absent');
  assert.deepEqual(plan.remove, []);
});

test('every refusal code carries one reason and one next action (R4, R5)', () => {
  for (const [code, r] of Object.entries(cron.REFUSALS)) {
    assert.match(code, /^[a-z][a-z0-9_]*$/);
    assert.ok(r.reason && !r.reason.includes('\n'));
    assert.ok(r.next && r.next.length > 10);
  }
});
