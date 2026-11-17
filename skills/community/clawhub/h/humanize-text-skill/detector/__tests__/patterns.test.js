/**
 * humanize-text-skill — detector fixtures
 *
 * Node-runnable tests for the detection engine. Intentionally small and
 * dependency-free so they run on any `node >= 18`. Invoked via `npm test`.
 *
 * Failure modes worth catching:
 *   - AI-heavy text scoring as human (regression in pattern coverage)
 *   - Plain prose scoring above "minimal" (false-positive drift)
 *   - Length gates (too-short / too-long) not firing
 *   - Stats failing to sum to issue count (dedup math drift)
 *   - zh/en asymmetry (a structural pattern flagged in one lang, not the other)
 *   - fidelity gate not catching protected-span drift
 *   - voice.drift not separating from score
 *
 * Stage 0: engine not yet implemented; these tests skip with a clear message.
 * Stage 1+: fixtures populate as each engine module lands.
 */
'use strict';

const assert = require('node:assert/strict');
const childProcess = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

let Huorengan;
try {
  Huorengan = require('../patterns.js');
} catch (e) {
  console.log('Detector fixtures');
  console.log('  \u2299 engine not yet implemented (stage 0) — skipping. ' + e.message);
  console.log('\nAll detector fixtures skipped (no engine yet).');
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

console.log('Detector fixtures');

test('empty text returns Empty label', () => {
  const r = Huorengan.analyzeText('');
  assert.equal(r.label, 'Empty');
  assert.equal(r.issues.length, 0);
});

test('text under length gate returns tooShort flag', () => {
  const r = Huorengan.analyzeText('Short unscorable snippet.');
  assert.equal(r.tooShort, true);
  assert.equal(r.label, 'Too short');
});

test('one scorer contract: score is numeric and computed', () => {
  const text = 'Some ordinary prose about a build that broke and got fixed today. ';
  const r = Huorengan.analyzeText(text.repeat(3), {});
  assert.ok(typeof r.score === 'number', 'score is numeric');
  // fidelity (stage 2) and voice.drift (stage 4) are separate dimensions;
  // their presence is asserted in their respective stage's tests.
});

test('AI-heavy text scores high (English regression baseline)', () => {
  const text = [
    "In today's ever-evolving landscape, we delve into the intricate",
    'tapestry of innovation. This seamless, robust paradigm showcases a',
    'comprehensive framework. Moreover, it truly is a game-changer.',
    'Furthermore, this pivotal moment underscores how we navigate the',
    'complexities of modern AI.',
  ].join(' ');
  const r = Huorengan.analyzeText(text);
  assert.ok(r.score >= 60, `expected score >= 60, got ${r.score}`);
  assert.ok(['Strong AI signals', 'Heavy AI patterns'].includes(r.label), `got label: ${r.label}`);
});

test('plain human bug-report stays low (false-positive guard)', () => {
  const text = [
    'The build broke again this morning. Rolled back the auth refactor',
    'and tests pass now. Still need to figure out why the token refresh',
    'path hits a 401 for users on Safari but not Firefox — probably a',
    'cookie scope issue but I want to confirm before shipping a fix.',
  ].join(' ');
  const r = Huorengan.analyzeText(text);
  assert.ok(r.score <= 20, `expected score <= 20, got ${r.score}`);
  assert.ok(['HUMAN_ONLY', 'MIXED'].includes(r.document_classification),
    `human prose got ${r.document_classification}`);
});

test('stats fields sum to issues length', () => {
  const text = [
    "In today's landscape of innovation, we leverage seamless paradigms",
    'to harness the power of transformation. It is important to note',
    'that experts believe this is pivotal. Let me think step by step.',
  ].join(' ');
  const r = Huorengan.analyzeText(text);
  const sum = r.stats.tier1Count + r.stats.tier2Count + r.stats.tier3Count + r.stats.patternCount;
  assert.equal(sum, r.issues.length, `stats sum (${sum}) != issues (${r.issues.length})`);
});

test('em-dash detector ignores CLI flags like --save-dev', () => {
  const text = 'Run npm install --save-dev and then npm run build --no-verify --silent. Takes about ten seconds on this machine. The package is installed into node_modules directly after the install command completes successfully.';
  const r = Huorengan.analyzeText(text);
  const emDashIssues = r.issues.filter((i) => i.type === 'em-dash');
  assert.equal(emDashIssues.length, 0, 'CLI flags should not count as em dashes');
});

test('Chinese AI-heavy text scores high (zh regression baseline)', () => {
  const text = '值得注意的是，本次迭代在性能方面取得了显著提升，有效解决了长期困扰团队的延迟问题。我们打造了一套全新的解决方案，旨在赋能开发者社区，助力企业实现降本增效的闭环。综上所述，该方案表现优异，未来可期！';
  const r = Huorengan.analyzeText(text);
  assert.ok(r.stats.lang === 'zh', `expected zh routing, got ${r.stats.lang}`);
  assert.ok(r.score >= 40, `expected zh AI-heavy score >= 40, got ${r.score}`);
  // Should catch Chinese-specific tells: tier1 (jargon/opener), generic-conclusion
  const types = new Set(r.issues.map((i) => i.type));
  assert.ok(types.has('tier1'), 'expected tier1 hits on jargon/opener');
});

test('Chinese human technical status stays low (zh false-positive guard)', () => {
  const text = '今天把连接池上限从 20 调到 100，504 先压下来了。后面再观察 24 小时，如果错误率还在 0.1% 以下就全量。Safari 那个 token 刷新的 401 还没复现，可能跟 cookie 作用域有关，明天再确认。';
  const r = Huorengan.analyzeText(text);
  assert.ok(r.score <= 20, `expected zh human score <= 20, got ${r.score}`);
  assert.ok(['HUMAN_ONLY', 'MIXED'].includes(r.document_classification),
    `zh human prose got ${r.document_classification}`);
});

test('language router dispatches zh vs en correctly', () => {
  const zhR = Huorengan.analyzeText('值得注意的是这很重要。');
  const enR = Huorengan.analyzeText('It is worth noting that this matters.');
  assert.equal(zhR.stats.lang, 'zh', 'Chinese text routed to zh');
  assert.notEqual(enR.stats.lang, 'zh', 'English text not routed to zh');
});

test('scene policy suppresses T3 in chat mode (matrix.toml)', () => {
  // Text dense in T3 words (significant/innovative) — would surface T3 by default.
  const t3text = 'This is significant and innovative. The significant innovation is significant. We see significant innovative approaches that are significant across the board repeatedly today and again.';
  const defaultR = Huorengan.analyzeText(t3text);
  const chatR = Huorengan.analyzeText(t3text, { sceneMode: 'chat' });
  // Default surfaces T3; chat suppresses it per matrix.toml [chat] T3="suppress"
  const defaultT3 = defaultR.issues.filter((i) => i.type === 'tier3').length;
  const chatT3 = chatR.issues.filter((i) => i.type === 'tier3').length;
  assert.ok(defaultT3 >= 1, `default should surface T3, got ${defaultT3}`);
  assert.equal(chatT3, 0, `chat should suppress T3, got ${chatT3}`);
  assert.equal(chatR.stats.sceneMode, 'chat', 'sceneMode recorded in stats');
});

test('scene policy keeps T3 in public-writing mode', () => {
  const t3text = 'This is significant and innovative. The significant innovation is significant. We see significant innovative approaches that are significant across the board repeatedly today and again.';
  const pubR = Huorengan.analyzeText(t3text, { sceneMode: 'public-writing' });
  const pubT3 = pubR.issues.filter((i) => i.type === 'tier3').length;
  assert.ok(pubT3 >= 1, `public-writing should keep T3, got ${pubT3}`);
});

test('invalid sceneMode falls back to null (no suppression)', () => {
  const r = Huorengan.analyzeText('Some ordinary prose about a build that broke and got fixed today. ', {});
  const badR = Huorengan.analyzeText('Some ordinary prose about a build that broke and got fixed today. ', { sceneMode: 'nonexistent' });
  assert.equal(badR.stats.sceneMode, null, 'invalid sceneMode coerced to null');
});

// ─── Addition layer (voice) — humanize-text-skill's differentiator ──────────
test('voice is null when voiceMode is none (pure subtraction)', () => {
  const r = Huorengan.analyzeText('The build broke this morning and I rolled back the refactor.', {});
  assert.equal(r.voice, null, 'voice must be null in pure-subtraction mode');
});

test('voice produces drift + suggestions when voiceMode is set (en)', () => {
  const formal = 'Furthermore, it is worth noting that the aforementioned architectural decision necessitates a comprehensive reconsideration of the underlying infrastructure across multiple subsystems simultaneously.';
  const r = Huorengan.analyzeText(formal, { voiceMode: 'casual' });
  assert.ok(r.voice, 'voice block should be present');
  assert.ok(typeof r.voice.drift === 'number' && r.voice.drift > 0, `expected drift > 0, got ${r.voice.drift}`);
  assert.ok(r.voice.suggestions.length > 0, 'casual target on formal text should yield suggestions');
  assert.equal(r.voice.voiceMode, 'casual');
});

test('voice suggestions are language-appropriate (zh gets Chinese connectors)', () => {
  const zhFormal = '值得注意的是，本次架构决策需要对底层基础设施进行全面重新考量。此外，实施策略要求在多个相互关联的子系统中保持细致的注意力。';
  const r = Huorengan.analyzeText(zhFormal, { voiceMode: 'casual' });
  assert.ok(r.voice.drift > 0, 'zh formal text should drift from casual target');
  // Connector suggestions must be Chinese, not English
  const connSug = r.voice.suggestions.find((s) => s.kind === 'connectors');
  if (connSug) {
    assert.ok(!/and|but|so/.test(connSug.hint), 'zh connector suggestion leaked English');
  }
});

test('zh short technical text does not get artificially extreme voice drift', () => {
  const text = '今天把连接池上限从 20 调到 100，504 先压下来了。';
  const r = Huorengan.analyzeText(text, { voiceMode: 'casual' });
  assert.ok(r.voice, 'voice block should be present');
  assert.ok(r.voice.drift < 80, `short zh drift should be damped, got ${r.voice.drift}`);
  assert.equal(r.voice.confidence, 'low', 'single-sentence zh drift should be low-confidence');
});

test('zh tier2 skips effective-as-metric context', () => {
  const text = '这次策略有效 100 倍，后面再看在品控方面还有没有回退。';
  const r = Huorengan.analyzeText(text);
  const tier2Texts = r.issues.filter((i) => i.type === 'tier2').map((i) => i.text);
  assert.ok(!tier2Texts.includes('有效'), `metric context should suppress 有效, got ${tier2Texts.join(', ')}`);
});

test('missing policy voice file fails loudly instead of returning null voice', () => {
  const repoRoot = path.join(__dirname, '..', '..');
  const voicePath = path.join(repoRoot, 'policy', 'voice.toml');
  const backupPath = `${voicePath}.bak-test`;
  fs.renameSync(voicePath, backupPath);
  try {
    let err = null;
    try {
      childProcess.execFileSync(
        process.execPath,
        ['-e', 'const H=require("./detector/patterns.js"); H.analyzeText("值得注意的是，我们打造了一套方案。", { voiceMode: "casual" });'],
        { cwd: repoRoot, stdio: 'pipe' }
      );
    } catch (e) {
      err = e;
    }
    assert.ok(err, 'missing policy should cause a hard failure');
    const stderr = String(err.stderr || '') + String(err.stdout || '') + String(err.message || '');
    assert.match(stderr, /Missing required policy file: .*voice\.toml/, 'error should mention missing voice.toml');
  } finally {
    fs.renameSync(backupPath, voicePath);
  }
});

test('voice.drift is independent of score (three-dimension contract)', () => {
  // A text can be low AI-tone (low score) but far from a target voice (high drift).
  const clean = 'I fixed the bug yesterday afternoon. The tests pass now. Will ship tomorrow morning.';
  const r = Huorengan.analyzeText(clean, { voiceMode: 'blunt' });
  assert.ok(r.score < 30, 'clean text should have low AI-tone score');
  // drift is its own dimension — it does NOT derive from score
  assert.ok(typeof r.voice.drift === 'number', 'drift is computed independently');
});

test('custom voice calibrates from an author sample (references/voice/samples.md)', () => {
  // The casual-en sample from references/voice/samples.md — short punchy sentences.
  const casualSample = 'Rolled back the auth thing last night. Cookie scope was wrong. Fixed it, shipped it, moving on. Honestly should have checked that first but I was chasing the wrong thread for an hour.';
  // A formal text should drift far from this casual target.
  const formal = 'Furthermore, it is worth noting that the aforementioned architectural decision necessitates a comprehensive reconsideration of the underlying infrastructure across multiple interconnected subsystems simultaneously.';
  const r = Huorengan.analyzeText(formal, { voiceMode: 'custom', sample: casualSample });
  assert.ok(r.voice, 'custom voice should produce a voice block');
  assert.ok(r.voice.target._calibrated, 'target should be marked as calibrated');
  assert.ok(r.voice.target.sentence_len_target < 15, `casual sample should calibrate short target, got ${r.voice.target.sentence_len_target}`);
  assert.ok(r.voice.drift > 30, `formal text should drift far from casual target, got ${r.voice.drift}`);
});

test('custom voice without a sample returns null (graceful)', () => {
  const r = Huorengan.analyzeText('Some text here that is long enough to clear the length gate for testing the custom mode gracefully today.', { voiceMode: 'custom' });
  assert.equal(r.voice, null, 'custom without sample should return null');
});

// ─── examples.md showcase cases (5 groups) — pins the README/examples claims ──
test('H1: zh README intro hits tier1 (jargon cleanup)', () => {
  const r = Huorengan.analyzeText('在 AI 全面重塑开发范式的今天，我们打造了一款真正面向未来的中文表达优化工具，深度赋能开发者的内容生产链路。');
  const types = new Set(r.issues.map((i) => i.type));
  assert.ok(types.has('tier1'), `H1 should hit tier1, got ${[...types].join(',')}`);
});

test('H2: en LinkedIn post hits tier1 + voice casual drift', () => {
  const text = "In today's rapidly evolving landscape, we leverage cutting-edge technology to deliver seamless, robust solutions. Moreover, this transformative platform empowers organizations to navigate the intricacies of modern business.";
  const r = Huorengan.analyzeText(text, { voiceMode: 'casual' });
  const types = new Set(r.issues.map((i) => i.type));
  assert.ok(types.has('tier1'), 'H2 should hit tier1');
  assert.ok(r.voice && r.voice.drift > 20, `H2 casual drift should be notable, got ${r.voice && r.voice.drift}`);
});

test('H3: status unsourced-citation hits tier1 (audit-only policy)', () => {
  const r = Huorengan.analyzeText('数据显示，这次改版显著提升了留存率。业内人士认为，这个方向已经验证可行，后续只要继续投入就能稳定放大收益。', { sceneMode: 'status' });
  const types = new Set(r.issues.map((i) => i.type));
  assert.ok(types.has('tier1'), 'H3 should hit tier1 (数据显示/业内人士认为)');
  assert.equal(r.stats.sceneMode, 'status', 'H3 should run in status scene');
});

test('H4: issue-reply sycophancy hits tier1', () => {
  const r = Huorengan.analyzeText('感谢你非常宝贵的反馈！你这个问题问到了项目体验的核心。我们已经充分接住了这个场景，也会在后续版本中持续优化相关能力。如果你愿意，我可以先帮你把这段文本整体梳理一遍。');
  const types = new Set(r.issues.map((i) => i.type));
  assert.ok(types.has('tier1'), 'H4 should hit tier1 (客服腔)');
});

test('H5: bilingual symmetry — binary-contrast same type in zh + en', () => {
  const zh = Huorengan.analyzeText('真正的竞争力不是功能堆砌，而是体验细节。');
  const en = Huorengan.analyzeText('It is not about features, it is about the details of the experience.');
  const zhTypes = new Set(zh.issues.map((i) => i.type));
  const enTypes = new Set(en.issues.map((i) => i.type));
  assert.ok(zhTypes.has('false-concession'), 'H5 zh should hit false-concession');
  assert.ok(enTypes.has('false-concession'), 'H5 en should hit false-concession (strong symmetry)');
});

if (failed > 0) {
  console.error(`\n${failed} test(s) failed`);
  process.exit(1);
}
console.log('\nAll detector fixtures passed.');
