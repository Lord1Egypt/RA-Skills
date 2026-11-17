/**
 * humanize-text-skill — evals/fixtures.json gate test
 *
 * Binds the human-judged benchmark (evals/benchmark.md, prose) to the
 * deterministic engine: every SF (should-fix) case must be hit by the detector
 * with score >= its threshold; every SNF (should-not-fix) case must score below.
 *
 * This is the CI gate that prevents "the prose says it's fixed but the engine
 * can't see it" drift — the failure mode both parent projects are vulnerable to
 * because their benchmarks and engines live in separate worlds.
 *
 * Dependency-free; runs on node >= 18.
 */
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Huorengan = require('../patterns.js');

let failed = 0;
function test(name, fn) {
  try {
    fn();
    console.log(`  \u2713 ${name}`);
  } catch (err) {
    failed++;
    console.error(`  \u2717 ${name}`);
    console.error(`    ${err.message}`);
  }
}

const fixtures = JSON.parse(
  fs.readFileSync(path.join(__dirname, '..', '..', 'evals', 'fixtures.json'), 'utf8')
);

console.log('evals/fixtures.json gate');
console.log(`  (${fixtures.sf.length} SF, ${fixtures.snf.length} SNF)`);

for (const c of fixtures.sf) {
  test(`SF ${c.id}: detector hits expected types at score >= ${c.expect_min_score}`, () => {
    const r = Huorengan.analyzeText(c.text);
    const types = new Set(r.issues.map((i) => i.type));
    const missing = c.expect_types.filter((t) => !types.has(t));
    assert.deepEqual(missing, [], `${c.id}: expected types ${c.expect_types.join(',')} not all present (got ${[...types].join(',')})`);
    assert.ok(r.score >= c.expect_min_score, `${c.id}: score ${r.score} < expected ${c.expect_min_score}`);
  });
}

for (const c of fixtures.snf) {
  test(`SNF ${c.id}: score <= ${c.expect_max_score} (${c.rationale})`, () => {
    const r = Huorengan.analyzeText(c.text);
    assert.ok(r.score <= c.expect_max_score, `${c.id}: score ${r.score} > max ${c.expect_max_score} — ${c.rationale}`);
    assert.notEqual(r.document_classification, 'AI_ONLY', `${c.id}: should not classify AI_ONLY — ${c.rationale}`);
  });
}

if (failed > 0) {
  console.error(`\n${failed} fixture gate check(s) failed.`);
  process.exit(1);
}
console.log('\nfixtures.json gate holds.');
