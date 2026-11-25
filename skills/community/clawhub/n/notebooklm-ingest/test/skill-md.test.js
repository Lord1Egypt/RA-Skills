'use strict';
// U7 — the bundle's own prose. R4/R5 (the Errors table), R8, R10, R12, R15,
// R19, R21.
//
// These read the documentation, which is unusual for a test suite and is the
// point. The script never decides which notebook matters, what a note means, or
// what to do when a refusal arrives — the AGENT does, out of SKILL.md. So the
// only thing standing between a refusal code the script emits and a reply the
// user can act on is what the prose says that code means. A doc that describes
// the wrong code is not a cosmetic defect here; it is the whole of the
// contract, and nothing else in this bundle can catch it.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const DIR = path.join(__dirname, '..');
const cli = require('../scripts/notebooklm-ingest.js');
const nlm = require('../scripts/nlm-cli.js');
const srv = require('../scripts/server.js');
const st = require('../scripts/state.js');
const cronMod = require('../scripts/cron.js');

const read = (rel) => fs.readFileSync(path.join(DIR, rel), 'utf8');

const SKILL_MD = read('SKILL.md');
const FRONT = SKILL_MD.match(/^---\n([\s\S]*?)\n---/)[1];
const DOCS = {
  'SKILL.md': SKILL_MD,
  'README.md': read('README.md'),
  'references/tool-contract.md': read('references/tool-contract.md'),
  'references/cli-contract.md': read('references/cli-contract.md'),
  'references/trigger-contract.md': read('references/trigger-contract.md'),
  'references/credential-contract.md': read('references/credential-contract.md'),
};

/** Every text file in the bundle: docs, scripts, tests, json. */
function bundleFiles(dir = DIR, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === 'data' || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) bundleFiles(full, acc);
    else if (/\.(js|md|json)$/.test(entry.name)) acc.push(path.relative(DIR, full));
  }
  return acc;
}

// ---------------------------------------------------------------------------
// Frontmatter and bundle layout
// ---------------------------------------------------------------------------

test('the frontmatter name equals the directory name (the starter\'s slash command)', () => {
  assert.match(FRONT, /^name: notebooklm-ingest$/m);
  assert.equal(path.basename(DIR), 'notebooklm-ingest');
  // Renaming it later would strand every registered cron job, so it is pinned
  // in four places at once.
  assert.equal(JSON.parse(read('package.json')).name, 'notebooklm-ingest');
  assert.equal(srv.SKILL, 'notebooklm-ingest');
  assert.match(cronMod.JOB_NAME, /^notebooklm-ingest-daily-v\d+$/);
});

test('the frontmatter carries a description and keywords', () => {
  assert.match(FRONT, /^description: \S/m);
  assert.match(FRONT, /^keywords: \S/m);
  // The keywords must cover the trigger phrases SKILL.md tells the agent about.
  for (const phrase of ['fetch my notebooklm', 'notebooklm to wiki', '同步我的 notebooklm']) {
    assert.ok(FRONT.includes(phrase), `keywords/description should name "${phrase}"`);
    assert.ok(SKILL_MD.includes(phrase), `SKILL.md should name "${phrase}"`);
  }
});

test('the bundle has the house layout', () => {
  for (const f of [
    'SKILL.md', 'README.md', 'package.json', 'starters.json',
    'scripts/notebooklm-ingest.js', 'scripts/normalize.js', 'scripts/nlm-cli.js',
    'scripts/server.js', 'scripts/state.js', 'scripts/cron.js',
    'references/tool-contract.md', 'references/cli-contract.md',
    'references/trigger-contract.md', 'references/credential-contract.md',
  ]) {
    assert.ok(fs.existsSync(path.join(DIR, f)), `missing ${f}`);
  }
});

test('package.json has a test script and no dependencies (the container\'s Node only)', () => {
  const pkg = JSON.parse(read('package.json'));
  assert.equal(pkg.scripts.test, 'node --test');
  assert.equal(pkg.license, 'MIT');
  assert.equal(pkg.engines.node, '>=18');
  assert.equal(pkg.dependencies, undefined);
  assert.equal(pkg.devDependencies, undefined);
});

test('starters.json ends with exactly one trailing newline (the root suite checks it)', () => {
  const raw = read('starters.json');
  assert.ok(raw.endsWith('}\n'));
  assert.equal(raw.endsWith('}\n\n'), false);
  const obj = JSON.parse(raw);
  assert.equal(obj.version, 1);
  assert.ok(Array.from(obj.title).length <= 30);
  // `requires` must be EMPTY: the repo-root validator hard-codes
  // ['has_recording', 'google_connected'], so a NotebookLM-connected flag
  // would fail the build — and google_connected is the wrong flag anyway,
  // because the OAuth Google provider covers Calendar and Gmail and there is
  // no NotebookLM API for a scope to cover.
  for (const s of obj.starters) assert.deepEqual(s.requires, []);
});

// ---------------------------------------------------------------------------
// R15 — curl_cffi appears nowhere except to be refused
// ---------------------------------------------------------------------------

test('R15 TC-S4-3: the banned transport is named in the bundle ONLY in a refusing context', () => {
  const banned = nlm.FORBIDDEN_TRANSPORT;
  const allowed = /forbidden|banned|never|refus|must not|not select|unset|anti-goal|impersonat/i;
  const offences = [];
  for (const rel of bundleFiles()) {
    const text = fs.readFileSync(path.join(DIR, rel), 'utf8');
    text.split('\n').forEach((line, i) => {
      if (!line.includes(banned)) return;
      if (!allowed.test(line)) offences.push(`${rel}:${i + 1}: ${line.trim()}`);
    });
  }
  assert.deepEqual(offences, [], `the banned transport is named without a refusing context:\n${offences.join('\n')}`);
});

test('R15: no code path can set NOTEBOOKLM_TRANSPORT, only delete it', () => {
  const offences = [];
  for (const rel of bundleFiles().filter((f) => f.startsWith('scripts/'))) {
    const text = fs.readFileSync(path.join(DIR, rel), 'utf8');
    text.split('\n').forEach((line, i) => {
      if (/NOTEBOOKLM_TRANSPORT\s*[:=]\s*['"`]/.test(line)) offences.push(`${rel}:${i + 1}`);
    });
  }
  assert.deepEqual(offences, [], 'a script assigns NOTEBOOKLM_TRANSPORT a value');
  assert.match(
    read('scripts/nlm-cli.js'), /delete env\.NOTEBOOKLM_TRANSPORT/,
    'the pin is by removal, so it survives an upstream rename of the default',
  );
});

test('R15: SKILL.md states the pin as a rule the agent may not "fix"', () => {
  assert.match(SKILL_MD, /^## Rules you may not "fix"$/m);
  const section = SKILL_MD.split(/^## Rules you may not "fix"$/m)[1].split(/^## /m)[0];
  assert.match(section, /NOTEBOOKLM_TRANSPORT/);
  assert.match(section, /pinned to the library default/);
  assert.match(section, /never an ops fix/);
  assert.match(section, /transport_forbidden/);
});

// ---------------------------------------------------------------------------
// R4 / R5 — the Errors table and the code registry agree, in both directions
// ---------------------------------------------------------------------------

/** The codes the Errors table lists, read out of its first column. */
function documentedCodes() {
  const table = SKILL_MD.split(/^## Errors$/m)[1].split(/^## /m)[0];
  return table
    .split('\n')
    .map((l) => l.match(/^\| `([a-z0-9_]+)` \| (\d+) \|/))
    .filter(Boolean)
    .map((m) => ({ code: m[1], exit: Number(m[2]) }));
}

test('R4 R5: every code in the code appears in the Errors table', () => {
  const documented = new Set(documentedCodes().map((r) => r.code));
  const missing = Object.keys(cli.REFUSALS).filter((c) => !documented.has(c));
  assert.deepEqual(missing, [], `codes with no Errors row: ${missing.join(', ')}`);
});

test('R4 R5: every code in the Errors table exists in the code', () => {
  const extra = documentedCodes().map((r) => r.code).filter((c) => !cli.REFUSALS[c]);
  assert.deepEqual(extra, [], `Errors rows for codes nothing emits: ${extra.join(', ')}`);
});

test('R4 R5: every Errors row names the exit code the script actually returns', () => {
  const wrong = documentedCodes().filter((r) => cli.EXIT_CODES[r.code] !== r.exit);
  assert.deepEqual(
    wrong.map((r) => `${r.code}: doc ${r.exit} vs code ${cli.EXIT_CODES[r.code]}`), [],
  );
});

test('R5: every Errors row says what to do, not only what went wrong', () => {
  const table = SKILL_MD.split(/^## Errors$/m)[1].split(/^## /m)[0];
  const rows = table.split('\n').filter((l) => /^\| `[a-z0-9_]+` \|/.test(l));
  assert.ok(rows.length >= 20, `only ${rows.length} rows`);
  for (const row of rows) {
    const cells = row.split(' | ');
    assert.equal(cells.length, 4, `malformed row: ${row.slice(0, 60)}`);
    const action = cells[3];
    assert.ok(action.length > 25, `the action column is too short to be an action: ${row.slice(0, 60)}`);
  }
});

test('R11: the dead-session row promises what R11 requires — nothing lost, re-auth offered', () => {
  const table = SKILL_MD.split(/^## Errors$/m)[1].split(/^## /m)[0];
  const row = table.split('\n').find((l) => l.startsWith('| `session_dead`'));
  assert.ok(row);
  assert.match(row, /no wiki content was lost/);
  assert.match(row, /re-authoris/i);
  assert.match(row, /chat_emit_action_buttons/);
});

// ---------------------------------------------------------------------------
// R19 / R21 — what the skill cannot do, said out loud
// ---------------------------------------------------------------------------

test('R19: SKILL.md says the agent proposes and the server disposes, and that nothing reads back', () => {
  assert.match(SKILL_MD, /^## The agent proposes; the server disposes$/m);
  const section = SKILL_MD.split(/^## The agent proposes; the server disposes$/m)[1].split(/^## /m)[0];
  assert.match(section, /cannot read the\s+wiki/);
  assert.match(section, /another user/);
  assert.match(section, /A note body is \*\*data\*\*/);
});

test('R19: no doc claims a read path through the push endpoint', () => {
  for (const [name, text] of Object.entries(DOCS)) {
    assert.doesNotMatch(text, /GET \/api\/skill\/sources/, name);
  }
  assert.match(DOCS['references/tool-contract.md'], /exactly two endpoints and both are writes/);
});

test('R21: wiki_ingest_external_tool is documented as the Google-free fallback', () => {
  assert.match(SKILL_MD, /wiki_ingest_external_tool/);
  const section = SKILL_MD.split(/^## Rules you may not "fix"$/m)[1].split(/^## /m)[0];
  assert.match(section, /wiki_ingest_external_tool[\s\S]{0,400}no NotebookLM access/);
  assert.match(DOCS['references/tool-contract.md'], /wiki_ingest_external_tool[\s\S]{0,300}survives a Google breakage/);
});

test('R21: no notebooklm_* MCP tool is ever named as a thing to call', () => {
  const offences = [];
  for (const rel of bundleFiles()) {
    const text = fs.readFileSync(path.join(DIR, rel), 'utf8');
    text.split('\n').forEach((line, i) => {
      if (!/notebooklm_[a-z]/.test(line)) return;
      // The only permitted mentions are the ones saying there are none.
      if (!/no |never|not |dropped|superseded|do not/i.test(line)) offences.push(`${rel}:${i + 1}: ${line.trim()}`);
    });
  }
  assert.deepEqual(offences, [], `notebooklm_* tools named as callable:\n${offences.join('\n')}`);
  assert.match(SKILL_MD, /There are no `notebooklm_\*` tools/);
});

// ---------------------------------------------------------------------------
// R10 — the always-reply rule, matching the repo-root wording
// ---------------------------------------------------------------------------

test('R10: SKILL.md has the "On-demand runs always reply" section in the house wording', () => {
  assert.match(SKILL_MD, /^## On-demand runs always reply$/m);
  const section = SKILL_MD.split(/^## On-demand runs always reply$/m)[1].split(/^## /m)[0];
  assert.match(section, /ALWAYS\s+ends with a chat\s+reply/);
  assert.match(section, /slash\s+command/);
  assert.match(section, /nothing/i);
  assert.match(section, /scheduled|dispatcher/i);
  // F26's regression: nothing may tie silence to the dispatcher path.
  assert.doesNotMatch(SKILL_MD, /silence is for the dispatcher/i);
});

test('R10: SKILL.md says chat_emit_* exists only on the on-demand turn', () => {
  assert.match(SKILL_MD, /^## Surfaces$/m);
  const section = SKILL_MD.split(/^## Surfaces$/m)[1].split(/^## /m)[0];
  assert.match(section, /chat_emit_action_buttons/);
  assert.match(section, /chat_emit_success_card/);
  assert.match(section, /scheduled[\s\S]{0,300}none of those tools exists/);
  assert.match(section, /body\.tools/);
});

test('R6: SKILL.md says history is markdown because no card shape fits it', () => {
  assert.match(SKILL_MD, /chat_emit_event_list[\s\S]{0,300}TestFlight/);
  assert.match(SKILL_MD, /Render history as markdown/);
});

test('R6: SKILL.md states the container-local history limitation', () => {
  assert.match(SKILL_MD, /ledger lives in this container and nowhere else/);
  assert.match(SKILL_MD, /rebuilt from an image starts with empty history/);
  assert.match(read('scripts/state.js'), /KNOWN LIMITATION/);
});

// ---------------------------------------------------------------------------
// R12 — the host field, and what setting it does not do
// ---------------------------------------------------------------------------

test('R12: SKILL.md names both hosts and says setting the field does not relocate anything', () => {
  for (const host of st.HOSTS) assert.ok(SKILL_MD.includes(host), `SKILL.md should name ${host}`);
  assert.match(SKILL_MD, /javis-mac.{0,60}documented alternative/s);
  assert.match(SKILL_MD, /records a preference, it does not relocate anything/);
  assert.match(SKILL_MD, /cannot execute itself on another machine/);
});

// ---------------------------------------------------------------------------
// R18 — the ordering, documented where it is read
// ---------------------------------------------------------------------------

test('R18: every doc that describes the hash says normalise FIRST', () => {
  assert.match(SKILL_MD, /NORMALISE\s+the text and only then hashes it|normalises.{0,40}then hashes/s);
  assert.match(DOCS['references/tool-contract.md'], /Normalise then hash/);
  assert.match(DOCS['references/tool-contract.md'], /never the reverse/);
  assert.match(DOCS['references/tool-contract.md'], /body_hash does not match the text/);
  // And the ordering must be stated as the failure it prevents, not as a style.
  assert.match(SKILL_MD, /hash taken before normalising makes every upload\s+refuse/);
});

test('R18: the documented size limit is the server\'s own constant', () => {
  const { MAX_TEXT_BYTES } = require('../scripts/normalize.js');
  assert.equal(MAX_TEXT_BYTES, 256 * 1024);
  assert.ok(SKILL_MD.includes(String(MAX_TEXT_BYTES)), 'the Errors table must name the real byte limit');
  assert.ok(DOCS['references/tool-contract.md'].includes('262144'));
});

// ---------------------------------------------------------------------------
// The wire shape is documented where it is pinned
// ---------------------------------------------------------------------------

test('the push endpoint path and source type are documented exactly as the code pins them', () => {
  assert.ok(DOCS['references/tool-contract.md'].includes(srv.ENDPOINTS.push));
  assert.ok(DOCS['references/tool-contract.md'].includes(srv.ENDPOINTS.digest));
  assert.ok(SKILL_MD.includes(srv.ENDPOINTS.push));
  assert.ok(DOCS['references/tool-contract.md'].includes(`\`${srv.SOURCE_TYPE}\``));
  // And the contract must say out loud that javis-server owns the shape, or a
  // reader takes this bundle's expectation for the endpoint's definition.
  assert.match(DOCS['references/tool-contract.md'], /THIS BUNDLE'S EXPECTATION OF AN ENDPOINT JAVIS-SERVER[\s>]+OWNS/);
});

test('the trigger contract documents the flag rules the constructor enforces', () => {
  const trigger = DOCS['references/trigger-contract.md'];
  assert.match(trigger, /Flags, not positionals/);
  assert.match(trigger, /2026\.5\.12-beta\.1/);
  for (const flag of ['--name', '--cron', '--message', '--agent main', '--session isolated', '--no-deliver', '--tz']) {
    assert.ok(trigger.includes(flag), `trigger-contract should document ${flag}`);
  }
  for (const flag of cronMod.INVALID_FLAGS) assert.ok(trigger.includes(flag), `should warn about ${flag}`);
  assert.ok(trigger.includes(cronMod.JOB_NAME), 'the job name must be documented');
  assert.match(trigger, /remove <id>/, 'removal is positional by id');
});

test('the cli contract documents the jar location and the never-print rule', () => {
  const doc = DOCS['references/cli-contract.md'];
  assert.match(doc, /\$NOTEBOOKLM_HOME\/profiles\/<profile>\/storage_state\.json/);
  assert.match(doc, /Path, presence, size, mtime and a sha256 digest/);
  assert.match(doc, /No command in this bundle prints a cookie/);
  assert.match(doc, /600-second/);
  assert.match(doc, /UNVERIFIED IN THE CONTAINER/, 'the honest status of the command surface');
});

test('the credential contract says what the jar actually grants (R8)', () => {
  const doc = DOCS['references/credential-contract.md'];
  assert.match(doc, /Google account.{0,40}cookie jar/s);
  assert.match(doc, /LSID/);
  assert.match(doc, /Javis never types a Google credential/);
  assert.match(doc, /Sec-Session-/, 'the canary must be documented where the credential is');
  assert.match(doc, /password change or reset/i);
});

test('every reference file SKILL.md lists exists, and every reference file is listed', () => {
  const listed = [...SKILL_MD.matchAll(/`references\/([a-z-]+\.md)`/g)].map((m) => m[1]);
  const onDisk = fs.readdirSync(path.join(DIR, 'references')).filter((f) => f.endsWith('.md'));
  assert.deepEqual([...new Set(listed)].sort(), onDisk.sort());
});

// ---------------------------------------------------------------------------
// README
// ---------------------------------------------------------------------------

test('README opens with the HiJavis-app-required banner the other READMEs open with', () => {
  const readme = DOCS['README.md'];
  assert.match(readme, /Requires the HiJavis iPhone app/);
  assert.match(readme, /apps\.apple\.com\/us\/app\/hijavis\/id6745134765/);
});

test('README tells the user the two honest limitations rather than only the upside', () => {
  const readme = DOCS['README.md'];
  assert.match(readme, /unofficial access/);
  assert.match(readme, /it will\s+break at some point/, 'the expiry date has to be in the user-facing page too');
  assert.match(readme, /History lives on your container/);
  assert.match(readme, /never asks for your password/i);
});
