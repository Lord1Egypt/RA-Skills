'use strict';
// SKILL.md and repo wiring — R6 (low-risk dispatch route), R7 (extraction
// rules), R9 (the 9 categories), R25 (chat runs the counting script).
// TC-S0-3 (route declared), TC-S5-3 (SKILL.md routes both questions to the script).

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const DIR = path.join(__dirname, '..');
const md = fs.readFileSync(path.join(DIR, 'SKILL.md'), 'utf8');
const front = md.match(/^---\n([\s\S]*?)\n---/)[1];

test('SKILL.md [R6, TC-S0-3]: front matter declares the low-risk ledger route', () => {
  assert.match(front, /- route_id: ledger\n/);
  assert.match(front, /risk: low/);
});

test('SKILL.md [R1]: name and every route skill are the ClawHub listing name javis-todo-spend-tracker', () => {
  assert.match(front, /^name: javis-todo-spend-tracker$/m);
  // Also matches a route whose first key is skill (`- skill: x`).
  const skills = [...front.matchAll(/^\s+(?:-\s+)?skill:\s*(\S+)\s*$/gm)].map((m) => m[1]);
  assert.ok(skills.length >= 1, 'at least one metadata.routes[].skill');
  assert.deepEqual(skills.filter((s) => s !== 'javis-todo-spend-tracker'), []);
  // The dispatcher prompt names the installed skill (Run /<slug>), not the data label.
  assert.ok(md.includes('Run /javis-todo-spend-tracker for <unit>.'));
  assert.doesNotMatch(md, /Run \/todo-spend-tracker\b/);
});

// 0.1.2: bumped so the first GitHub release tag (javis-todo-spend-tracker-v0.1.2)
// is a new version (install-skill-without-clawhub spec §1/§2).
test('package.json [R1]: name javis-todo-spend-tracker, version 0.1.2', () => {
  const pkg = JSON.parse(fs.readFileSync(path.join(DIR, 'package.json'), 'utf8'));
  assert.equal(pkg.name, 'javis-todo-spend-tracker');
  assert.equal(pkg.version, '0.1.2');
});

test('data label [R3]: lib.js SLUG and the skill_data label stay todo-spend-tracker', () => {
  const { SLUG } = require('../scripts/lib');
  assert.equal(SLUG, 'todo-spend-tracker');
  assert.ok(md.includes('`skill_data` (`skill=todo-spend-tracker`)'));
});

test('SKILL.md [R9]: lists the 9 categories exactly, in order', () => {
  const line = md.split('\n').map((l) => l.trim()).find((l) => l.startsWith('Categories (exactly one): '));
  assert.ok(line, 'categories line');
  assert.equal(line.replace('Categories (exactly one): ', ''),
    '`Food & drink`, `Groceries`, `Transport`, `Shopping`, `Bills & subscriptions`, `Entertainment`, `Health`, `Travel`, `Other`');
});

test('SKILL.md [R7]: states the extraction rules', () => {
  for (const s of ['first person', 'speaker_', 'keyboard', 'calendar-extractor', 'fetch-open', '25 words', 'Chinese']) {
    assert.ok(md.includes(s), `SKILL.md should mention ${s}`);
  }
});

test('SKILL.md [R25, TC-S5-3]: chat questions run the counting script and copy its numbers', () => {
  assert.ok(md.includes('node scripts/ledger.js todos'));
  assert.ok(md.includes('node scripts/ledger.js spending'));
  assert.match(md, /copy its numbers/i);
  assert.ok(md.includes('javis://todos'));
  assert.ok(md.includes('javis://todos/month'));
});

test('SKILL.md [R0-6]: the push step never pipes user quotes through echo \'…\'', () => {
  assert.doesNotMatch(md, /\|\s*node scripts\/todo-spend-tracker\.js push/);
  assert.ok(md.includes('push --file'));
  assert.ok(md.includes("<<'JAVIS_LEDGER_JSON'"));
});

test('SKILL.md [R0-5, R0-4, R0-2]: documents the unit field, the date window and the no-fallback read', () => {
  assert.match(md, /"unit":/);
  assert.match(md, /last month\s+or this month/);
  assert.match(md, /source` is `unavailable`/);
  assert.doesNotMatch(md, /data\/users/);
});

// Catalog v3 (install-skill-without-clawhub R3): the skill ships from GitHub
// release tags, so it is listed under its installed name only, as a default
// skill from this folder. The old name resolves to gmail-wiki-ingest on
// ClawHub, so it never appears.
test('repo [R3, TC-S0-2]: hijavis-skills.json lists javis-todo-spend-tracker, never the old name', () => {
  const list = JSON.parse(fs.readFileSync(path.join(DIR, '..', 'hijavis-skills.json'), 'utf8'));
  assert.ok(!list.skills.includes('todo-spend-tracker'));
  assert.ok(list.skills.includes('javis-todo-spend-tracker'));
  const entry = list.catalog.find((e) => e.slug === 'javis-todo-spend-tracker');
  assert.ok(entry);
  assert.equal(entry.folder, 'todo-spend-tracker');
  assert.equal(entry.default, true);
});

test('repo: starters.json passes the shared validator', () => {
  const { validate } = require('../../scripts/validate-starters');
  const starters = JSON.parse(fs.readFileSync(path.join(DIR, 'starters.json'), 'utf8'));
  assert.deepEqual(validate(starters, md), []);
});
