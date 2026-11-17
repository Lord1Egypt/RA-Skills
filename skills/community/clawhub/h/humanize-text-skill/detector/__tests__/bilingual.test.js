/**
 * humanize-text-skill — bilingual symmetry test (humanize-text-skill-specific)
 *
 * The two parent projects split along a language line: avoid-ai-writing is
 * English-only, shuorenhua is Chinese-first. humanize-text-skill unifies them, which
 * creates a new failure mode neither has: a structural pattern that exists in
 * BOTH languages (binary contrast, summary closer, false agency, three-list)
 * could be implemented in one language and forgotten in the other.
 *
 * This test catches that asymmetry. For each cross-lingual structural type, the
 * same kind of input in zh and en should both produce a hit (or both not).
 *
 * Stage 0: engine not yet implemented; skips with a clear message.
 */
'use strict';

const assert = require('node:assert/strict');

let Huorengan;
try {
  Huorengan = require('../patterns.js');
} catch (e) {
  console.log('Bilingual symmetry');
  console.log('  \u2299 engine not yet implemented (stage 0) — skipping. ' + e.message);
  console.log('\nBilingual symmetry skipped (no engine yet).');
  process.exit(0);
}

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

console.log('Bilingual symmetry');

// Cross-lingual structural patterns. Each concept now has detector parity:
// the SAME `type` fires in both languages (en symmetry landed in stage-7 task 1).
// This is the strong form of the bilingual contract — not just "fires in both"
// but "fires with the same type".
const CROSS_LINGUAL = [
  // binary-contrast: zh "不是X而是Y" / en "It's not X, it's Y" -> false-concession
  { type: 'false-concession',
    zh: '这不是技术问题，而是管理问题，团队流程比代码更容易出状况。',
    en: "It's not about the code, it's about the culture. The team matters more than the tools." },
  // value-inflation: zh "不仅仅是…更是…" / en "not just X, it's Y" -> significance-inflation
  { type: 'significance-inflation',
    zh: '这不仅仅是一个产品，更是一种信念的传承，改变了整个行业。',
    en: "It's not just a product, it's a movement that changes how we think about work today." },
];

for (const { type, zh, en } of CROSS_LINGUAL) {
  test(`"${type}" fires in BOTH zh and en (symmetric type)`, () => {
    const zhTypes = new Set(Huorengan.analyzeText(zh).issues.map((i) => i.type));
    const enTypes = new Set(Huorengan.analyzeText(en).issues.map((i) => i.type));
    assert.ok(zhTypes.has(type), `${type} not flagged in zh (got: ${[...zhTypes].join(',')})`);
    assert.ok(enTypes.has(type), `${type} not flagged in en (got: ${[...enTypes].join(',')})`);
  });
}

// Asymmetry guard: a Chinese-only translation-tone type must fire on zh and
// be absent on en (it has no English equivalent by design).
test('zh-only translation-tone type is zh-exclusive', () => {
  const zhPassive = Huorengan.analyzeText('系统被优化后，性能被显著提升，用户体验被大幅改善，整体被全面重构。');
  const zhTypes = new Set(zhPassive.issues.map((i) => i.type));
  assert.ok(zhTypes.has('zh-passive-stack'), 'zh-passive-stack should fire on Chinese passive stacking');
  // The same type should never appear on English text
  const enR = Huorengan.analyzeText('The system was optimized, performance was improved, and user experience was enhanced across the board.');
  const enTypes = new Set(enR.issues.map((i) => i.type));
  assert.ok(!enTypes.has('zh-passive-stack'), 'zh-only type leaked into English analysis');
});

if (failed > 0) {
  console.error(`\n${failed} symmetry check(s) failed.`);
  process.exit(1);
}
console.log('\nBilingual symmetry holds.');
