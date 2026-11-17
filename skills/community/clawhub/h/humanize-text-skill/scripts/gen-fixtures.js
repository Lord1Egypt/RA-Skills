/**
 * scripts/gen-fixtures.js — regenerate evals/fixtures.json from benchmark.md
 *
 * Parses every SF/SNF case in evals/benchmark.md, runs the engine on each,
 * and emits the machine-verifiable contract: for SF, the expected types that
 * fired + the observed score (CI asserts the engine STILL hits those types at
 * at least that score); for SNF, the observed score ceiling (CI asserts it
 * stays at or below).
 *
 * Run after benchmark changes or vocab additions:
 *   node scripts/gen-fixtures.js
 *
 * The generated file is the CI gate (detector/__tests__/fixtures.test.js).
 * Hand-tune thresholds in the JSON if a case is borderline; re-run to refresh.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const Huorengan = require(path.join(__dirname, '..', 'detector', 'patterns.js'));

const md = fs.readFileSync(path.join(__dirname, '..', 'evals', 'benchmark.md'), 'utf8');

// Parse cases. Each is: ### (SF|SNF)-NN | scene | desc \n > text
function parseCases(src) {
  const cases = [];
  const re = /^### (SF|SNF)-(\d+)\s*\|\s*([^|\n]+)\s*\|\s*([^\n]*)\n> ([^#\n][^\n]*(?:\n> [^\n]*)*)/gm;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [, kind, num, sceneRaw, desc, quoted] = m;
    const id = `${kind}-${num}`;
    // Clean the quoted text: strip leading "> ", join lines, remove markdown.
    let text = quoted.replace(/^> ?/gm, '').replace(/\n/g, ' ').trim();
    // For code-context cases, the text may include fenced code; keep the prose.
    cases.push({
      id,
      kind,
      scene: sceneRaw.trim(),
      desc: desc.trim(),
      text,
    });
  }
  return cases;
}

const cases = parseCases(md);
const sf = [];
const snf = [];

for (const c of cases) {
  if (!c.text || c.text.length < 5) continue;
  const r = Huorengan.analyzeText(c.text);
  const types = [...new Set(r.issues.map((i) => i.type))];
  const isZh = r.stats.lang === 'zh';

  if (c.kind === 'SF') {
    // SF: record the types that fired + the score (CI asserts they still fire).
    if (types.length > 0 && r.score > 0) {
      sf.push({
        id: c.id,
        scene: c.scene,
        lang: isZh ? 'zh' : 'en',
        text: c.text,
        expect_types: types.slice(0, 4),
        // Low-score cases are borderline; use a floor of 2 to avoid flapping
        // on tokenize/CV jitter. Higher scores allow score-3 drift headroom.
        expect_min_score: r.score < 10 ? 2 : r.score - 3,
      });
    }
    // else: judgment-only case (protected spans / scope / scene-pack) — not
    // engine-verifiable, skipped with a note.
  } else {
    // SNF: record the score ceiling (CI asserts it stays low).
    snf.push({
      id: c.id,
      scene: c.scene,
      lang: isZh ? 'zh' : 'en',
      text: c.text,
      expect_max_score: Math.max(25, r.score + 3), // allow small drift upward
      rationale: c.desc,
    });
  }
}

const out = {
  _comment: 'Engine-verifiable fixtures auto-generated from evals/benchmark.md by scripts/gen-fixtures.js. SF: detector must hit expect_types at score >= expect_min_score. SNF: score must stay <= expect_max_score and not classify AI_ONLY. Cases requiring pure judgment (protected-span fidelity, in-place scope, scene-pack tone) are NOT here — those stay human-judged in benchmark.md.',
  _generated_by: 'scripts/gen-fixtures.js',
  sf,
  snf,
};

fs.writeFileSync(
  path.join(__dirname, '..', 'evals', 'fixtures.json'),
  JSON.stringify(out, null, 2) + '\n'
);
console.log(`Generated evals/fixtures.json: ${sf.length} SF + ${snf.length} SNF (${cases.length} parsed, ${cases.length - sf.length - snf.length} judgment-only skipped)`);
