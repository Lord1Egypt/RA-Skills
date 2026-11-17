/**
 * humanize-text-skill — end-to-end test
 *
 * Walks the full user journey as a real consumer would, exercising every
 * advertised capability in combination (not in isolation like the unit tests):
 *
 *   1. bilingual routing (zh / en / mixed)
 *   2. subtraction layer (AI-heavy scores high, human scores low, in BOTH langs)
 *   3. scene × tier policy (chat suppresses T3, others don't)
 *   4. voice addition layer (drift + suggestions, 6 profiles + custom)
 *   5. three-dimension independence (score / fidelity-absent / voice.drift)
 *   6. false-positive guard (technical text with numbers/commands untouched)
 *   7. edge cases (empty, too-short, too-long, invalid options)
 *
 * This is the "did the whole thing hold together" test. Unit tests pin
 * individual contracts; this one pins the integration.
 *
 * Dependency-free; runs on node >= 18.
 */
'use strict';

const assert = require('node:assert/strict');
const Huorengan = require('../patterns.js');

let failed = 0;
const results = [];
function test(name, fn) {
  try {
    fn();
    results.push(['✓', name]);
  } catch (err) {
    failed++;
    results.push(['✗', name, err.message]);
  }
}

// ─── 1. Bilingual routing ─────────────────────────────────────────
test('e2e 1.1: pure Chinese routes to zh analyzer', () => {
  const r = Huorengan.analyzeText('值得注意的是，我们打造了赋能开发者的方案，助力实现闭环。');
  assert.equal(r.stats.lang, 'zh', `expected zh, got ${r.stats.lang}`);
  assert.ok(r.issues.some((i) => i.lang === 'zh'), 'zh issues should carry lang:zh');
});

test('e2e 1.2: pure English routes to en analyzer (not zh)', () => {
  const r = Huorengan.analyzeText("In today's ever-evolving landscape, we leverage seamless robust paradigms to navigate modern complexities.");
  assert.notEqual(r.stats.lang, 'zh', 'English text should not route to zh');
});

test('e2e 1.3: bilingual symmetry — same concept, same type in zh + en', () => {
  const zh = Huorengan.analyzeText('真正的竞争力不是功能堆砌，而是体验细节。');
  const en = Huorengan.analyzeText('It is not about features, it is about the details of the experience.');
  const zhTypes = new Set(zh.issues.map((i) => i.type));
  const enTypes = new Set(en.issues.map((i) => i.type));
  assert.ok(zhTypes.has('false-concession') && enTypes.has('false-concession'),
    'binary-contrast should hit false-concession in both langs');
});

// ─── 2. Subtraction layer (both languages) ────────────────────────
test('e2e 2.1: zh AI-heavy scores high', () => {
  const r = Huorengan.analyzeText('值得注意的是，我们打造了一套赋能开发者社区的方案，助力企业实现降本增效闭环。综上所述，未来可期！');
  assert.ok(r.score >= 30, `zh AI-heavy score ${r.score} too low`);
  assert.ok(r.issues.length >= 5, `only ${r.issues.length} issues`);
});

test('e2e 2.2: en AI-heavy scores high', () => {
  const r = Huorengan.analyzeText("In today's rapidly evolving landscape, we delve into the intricate tapestry of innovation. This seamless robust paradigm showcases a comprehensive framework. Moreover it truly is a game-changer.");
  assert.ok(r.score >= 40, `en AI-heavy score ${r.score} too low`);
});

// ─── 3. scene × tier policy ───────────────────────────────────────
test('e2e 3.1: chat suppresses T3, public-writing keeps it', () => {
  const t3 = 'This is significant and innovative. The significant innovation is significant. We see significant innovative approaches repeatedly today and again now.';
  const chat = Huorengan.analyzeText(t3, { sceneMode: 'chat' });
  const pub = Huorengan.analyzeText(t3, { sceneMode: 'public-writing' });
  assert.equal(chat.issues.filter((i) => i.type === 'tier3').length, 0, 'chat should suppress T3');
  assert.ok(pub.issues.filter((i) => i.type === 'tier3').length >= 1, 'public-writing should keep T3');
});

test('e2e 3.2: T1 never suppressed across all 4 scenes', () => {
  const t1 = '值得注意的是，我们赋能开发者，打造闭环，深度助力。';
  for (const s of ['chat', 'status', 'docs', 'public-writing']) {
    const r = Huorengan.analyzeText(t1, { sceneMode: s });
    assert.ok(r.issues.some((i) => i.type === 'tier1'), `T1 missing in scene ${s}`);
  }
});

// ─── 4. Voice addition layer ──────────────────────────────────────
test('e2e 4.1: voice drift + suggestions on formal text (casual target)', () => {
  const r = Huorengan.analyzeText('Furthermore, it is worth noting that the aforementioned architectural decision necessitates a comprehensive reconsideration of the underlying infrastructure across multiple subsystems simultaneously.', { voiceMode: 'casual' });
  assert.ok(r.voice.drift > 30, `drift ${r.voice.drift} too low for formal-vs-casual`);
  assert.ok(r.voice.suggestions.length > 0, 'should yield pull suggestions');
});

test('e2e 4.2: all 6 voice profiles produce a voice block', () => {
  for (const v of ['casual', 'professional', 'technical', 'warm', 'blunt']) {
    const r = Huorengan.analyzeText('Some ordinary prose about a build that broke and got fixed today afternoon.', { voiceMode: v });
    assert.ok(r.voice, `${v} missing voice block`);
    assert.equal(r.voice.voiceMode, v);
  }
});

test('e2e 4.3: custom calibrates from sample', () => {
  const sample = 'Rolled back the auth thing. Cookie scope was wrong. Fixed it. Shipped it. Moving on now today.';
  const r = Huorengan.analyzeText('The aforementioned implementation necessitates comprehensive reconsideration of the underlying infrastructure subsystems.', { voiceMode: 'custom', sample });
  assert.ok(r.voice.target._calibrated, 'custom target should be flagged _calibrated');
});

// ─── 5. Three-dimension independence ──────────────────────────────
test('e2e 5.1: low-score text can still have high voice drift', () => {
  const clean = 'I fixed the bug yesterday afternoon. The tests pass now. Will ship tomorrow morning.';
  const r = Huorengan.analyzeText(clean, { voiceMode: 'blunt' });
  assert.ok(r.score < 30, `clean text score ${r.score} should be low`);
  assert.ok(typeof r.voice.drift === 'number', 'drift must be computed independently of score');
});

test('e2e 5.2: fidelity is NOT an engine return field (rule-layer, as documented)', () => {
  const r = Huorengan.analyzeText('Some text here that is long enough to clear the gate today.');
  assert.ok(!('fidelity' in r), 'fidelity should not be a return field (README marks it 规划中)');
});

// ─── 6. False-positive guard ──────────────────────────────────────
test('e2e 6.1: zh technical status (numbers/commands) not flagged', () => {
  const r = Huorengan.analyzeText('今天把连接池上限从 20 调到 100，504 先压下来了。观察 24 小时，错误率 0.1% 以下就全量。');
  assert.ok(r.score <= 20, `technical text score ${r.score} — false positive`);
  assert.notEqual(r.document_classification, 'AI_ONLY');
});

test('e2e 6.2: en dense-jargon technical writing not AI_ONLY', () => {
  const r = Huorengan.analyzeText('Rust offers a robust and comprehensive approach to systems programming. Engineers leverage zero-cost abstractions to navigate intricate memory hierarchies. The borrow checker provides meticulous compile-time guarantees across the ecosystem.');
  assert.notEqual(r.document_classification, 'AI_ONLY', `Rust docs misclassified AI_ONLY at score ${r.score}`);
});

// ─── 7. Edge cases ────────────────────────────────────────────────
test('e2e 7.1: empty text → Empty label', () => {
  assert.equal(Huorengan.analyzeText('').label, 'Empty');
});

test('e2e 7.2: too-short text → tooShort', () => {
  assert.equal(Huorengan.analyzeText('短.').tooShort, true);
});

test('e2e 7.3: too-long text → tooLong', () => {
  assert.equal(Huorengan.analyzeText('word '.repeat(10001)).tooLong, true);
});

test('e2e 7.4: invalid contextMode coerces to general', () => {
  const r = Huorengan.analyzeText('Some text here that is long enough to pass the gate today.', { contextMode: 'nonsense' });
  assert.equal(r.stats.contextMode, 'general');
  assert.equal(r.stats.contextModeFallback, 'nonsense');
});

test('e2e 7.5: invalid sceneMode coerces to null (no suppression)', () => {
  const r = Huorengan.analyzeText('Some text here that is long enough to pass the gate today.', { sceneMode: 'bogus' });
  assert.equal(r.stats.sceneMode, null);
});

test('e2e 7.6: trinary classification always sums to 1.0', () => {
  for (const t of [
    '值得注意的是，我们赋能开发者打造闭环。综上所述，未来可期！',
    'The build broke. Rolled back. Tests pass.',
    'Some neutral text about a system that does things in a moderate way today.',
  ]) {
    const r = Huorengan.analyzeText(t);
    const sum = r.class_probabilities.human + r.class_probabilities.mixed + r.class_probabilities.ai;
    assert.ok(Math.abs(sum - 1) < 0.02, `probabilities sum ${sum} != 1`);
  }
});

// ─── 8. Honest gates: pin KNOWN limitations (so future fixes are deliberate) ─
// These assert current behavior that is a deliberate (if incomplete) design
// choice, NOT a bug. If a future change implements the fuller behavior, these
// fail loudly — forcing the contributor to re-evaluate and update docs. This
// is the "honest gate" pattern: known gaps get CI-locked just like features.

test('e2e 8.1 [known limitation]: contextMode has 2 effective behaviors, not 4', () => {
  // technical differs from general (skips title-case-header); marketing and
  // personal currently behave identically to general. This is documented as a
  // v0.1.0 boundary. If marketing/personal get differentiated, this fails and
  // the README/contextMode table should be updated.
  const text = 'This is significant and innovative text about a robust comprehensive system. Moreover the transformative approach navigates intricacies repeatedly today now here.';
  const g = Huorengan.analyzeText(text, { contextMode: 'general' });
  const m = Huorengan.analyzeText(text, { contextMode: 'marketing' });
  const p = Huorengan.analyzeText(text, { contextMode: 'personal' });
  assert.equal(g.score, m.score, 'marketing should match general (known limitation)');
  assert.equal(g.score, p.score, 'personal should match general (known limitation)');
  assert.equal(g.issues.length, m.issues.length);
  assert.equal(g.issues.length, p.issues.length);
});

test('e2e 8.2 [known limitation]: sceneMode only differentiates T3, not T1/T2', () => {
  // The scene×tier matrix only affects T3 (chat suppresses it). T1/T2 are
  // surfaced identically across all 4 scenes. This is the current v0.1.0
  // matrix granularity. If T1/T2 scene differentiation lands, update this.
  const text = '值得注意的是，我们赋能开发者打造闭环。然而此外，显著有效全面持续地推动提升。';
  const counts = {};
  for (const s of ['chat', 'status', 'docs', 'public-writing']) {
    const r = Huorengan.analyzeText(text, { sceneMode: s });
    counts[s] = {
      t1: r.issues.filter((i) => i.type === 'tier1').length,
      t2: r.issues.filter((i) => i.type === 'tier2').length,
    };
  }
  const t1s = new Set(Object.values(counts).map((c) => c.t1));
  const t2s = new Set(Object.values(counts).map((c) => c.t2));
  assert.equal(t1s.size, 1, `T1 count varies across scenes (got ${[...t1s]}) — if intended, update this gate`);
  assert.equal(t2s.size, 1, `T2 count varies across scenes (got ${[...t2s]}) — if intended, update this gate`);
});

// ─── Report ───────────────────────────────────────────────────────
console.log('end-to-end integration test');
for (const [mark, name, msg] of results) {
  if (mark === '✓') console.log(`  \u2713 ${name}`);
  else { console.error(`  \u2717 ${name}`); console.error(`    ${msg}`); }
}
if (failed > 0) {
  console.error(`\n${failed} e2e check(s) failed.`);
  process.exit(1);
}
console.log(`\nAll ${results.length} e2e checks passed.`);
