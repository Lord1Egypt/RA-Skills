/**
 * humanize-text-skill — README example numbers vs engine output
 *
 * Pins the concrete numbers cited in README.md so they can't silently drift
 * from the engine's actual output. When the engine's scoring/voice weights
 * change and a README example no longer matches, this fails loudly instead of
 * shipping a README that lies.
 *
 * Each entry: { find (a unique substring in README), text, options, assert }.
 * The test runs the engine on `text`+`options` and checks the README still
 * contains the asserted number near that example.
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

const readme = fs.readFileSync(path.join(__dirname, '..', '..', 'README.md'), 'utf8');

console.log('README example numbers vs engine');

// Case 1: zh AI-heavy example — README says score 55, 10 issues.
test('zh AI-heavy: score=55, issues=10 (README §真实证据)', () => {
  const text = '值得注意的是，我们打造了一套赋能开发者社区的方案，助力企业实现降本增效闭环。综上所述，未来可期！';
  const r = Huorengan.analyzeText(text);
  assert.equal(r.score, 55, `engine score drifted to ${r.score} — update README`);
  assert.equal(r.issues.length, 10, `issue count drifted to ${r.issues.length} — update README`);
  assert.ok(readme.includes('55'), 'README no longer cites score 55');
});

// Case 2: zh human (protected spans) — README says score 0.
test('zh human: score=0 (README §真实证据, false-positive guard)', () => {
  const text = '今天把连接池上限从 20 调到 100，504 先压下来了。观察 24 小时，错误率 0.1% 以下就全量。';
  const r = Huorengan.analyzeText(text);
  assert.equal(r.score, 0, `engine score drifted to ${r.score} — update README`);
});

// Case 3: voice casual drift — README says drift 71.
test('voice casual drift=71 (README §加法层)', () => {
  const text = '值得注意的是，本次架构决策需要全面重新考量。此外，实施策略要求细致的注意力。';
  const r = Huorengan.analyzeText(text, { voiceMode: 'casual' });
  assert.ok(r.voice, 'voice block missing');
  assert.equal(r.voice.drift, 71, `drift drifted to ${r.voice.drift} — update README`);
  assert.ok(readme.includes('voice.drift = 71'), 'README no longer cites drift 71');
});

// ─── Test-count lock: README's "N CI checks" must match the real total ────
// Counts test() calls across all __tests__/*.js + fixtures SF/SNF. Prevents
// the "99 vs 122" drift from recurring: adding/removing a test without bumping
// README's number fails CI. The number lives in README in several forms
// ("N 项 CI 实测" / "N CI checks" / "N 项检查"), so we extract whatever
// integer README claims and compare.
test('README test-count matches real test total (anti-drift lock)', () => {
  const testDir = path.join(__dirname);
  const files = fs.readdirSync(testDir).filter((f) => f.endsWith('.test.js'));
  let count = 0;
  for (const f of files) {
    const src = fs.readFileSync(path.join(testDir, f), 'utf8');
    // Count test(...) / test(`...`) calls in this file (each = 1 ✓ when passing)
    const matches = src.match(/\btest\s*\(/g);
    count += matches ? matches.length : 0;
  }
  // Add fixtures SF/SNF (each is one ✓ in fixtures.test.js's loop, not a test() call)
  const fixtures = JSON.parse(
    fs.readFileSync(path.join(__dirname, '..', '..', 'evals', 'fixtures.json'), 'utf8')
  );
  count += fixtures.sf.length + fixtures.snf.length;

  // Extract the number README claims (any of the known phrasings).
  const claimed = (readme.match(/(\d+)\s*(?:项 CI 实测|CI checks|项检查)/) || [])[1];
  assert.ok(claimed, 'README no longer cites a CI-check count');
  assert.equal(Number(claimed), count,
    `README claims ${claimed} CI checks but the suite actually has ${count} — sync README`);
});

if (failed > 0) {
  console.error(`\n${failed} README-example check(s) failed.`);
  process.exit(1);
}
console.log('\nREADME example numbers match engine output.');
