/**
 * core/scoring — the ONE scorer (language-agnostic).
 *
 * This module is the single source of truth for the `score` field. By contract
 * (AGENTS.md, CONTRIBUTING.md): `score` (AI density) lives ONLY here. `fidelity`
 * is a gate, `voice.drift` is an independent dimension — never mixed.
 *
 * Migrated verbatim from avoid-ai-writing's ISSUE_WEIGHTS + dedup + getLabel +
 * length normalization. Behavioral parity is the regression contract.
 *
 * Scoring model:
 *   Each category has a weight in ISSUE_WEIGHTS. rawScore is the sum of
 *   category weights across the DEDUPED issue list. rawScore is then normalized
 *   to 0-100 via log2(wordCount/50) so longer texts don't accumulate
 *   unboundedly on the same density of patterns.
 */
'use strict';

// Per-category score weights. Applied to distinct (deduplicated) issues.
// Non-uniform: critical rules like cutoff disclaimers (×10) and chatbot
// artifacts (×8) weigh more than vague attributions (×5), even though all
// three are tagged `critical`.
const ISSUE_WEIGHTS = {
  tier1: 5,
  tier2: 3,
  tier3: 2,
  transition: 2,
  chatbot: 8,
  sycophantic: 8,
  filler: 2,
  'generic-conclusion': 3,
  'lets-construction': 2,
  'reasoning-artifact': 6,
  'acknowledgment-loop': 3,
  'significance-inflation': 4,
  'vague-attribution': 5,
  'hollow-intensifier': 2,
  'emotional-flatline': 2,
  'novelty-inflation': 3,
  'cutoff-disclaimer': 10,
  'template-phrase': 3,
  'false-concession': 2,
  'rhetorical-question': 2,
  'confidence-calibration': 2,
  'em-dash': 4,
  uniformity: 5,
  formatting: 3,
  'tier3-phrase': 3,
  'tier3-phrase-cluster': 12,
  'hashtag-stuff': 12,
  'bullet-np-list': 10,
  'hedge-stack': 6,
  'future-narrative': 12,
  'real-actual-inflation': 5,
  'social-cta-closer': 8,
  'formulaic-opener': 8,
  'title-case-header': 4,
  'parenthetical-hedge': 3,
  'smart-punct-signature': 6,
  'punct-distribution': 6,
  'fnword-trigram-entropy': 5,
  'cross-para-burstiness': 5,
  'normalization-flag': 9,
  'low-ttr': 3,
  'ai-placeholder': 10,
  'ai-citation-markup': 15,
  'ai-utm-source': 12,
  // zh-only translation-tone weights (modest — these are Chinese-specific
  // structural tells, individually weaker than vocabulary hits)
  'zh-passive-stack': 3,
  'zh-long-attributive': 2,
  'zh-translation-opener': 2,
  'zh-via-to': 2,
  'zh-for-x-regard': 2,
  'zh-in-x-aspect': 2,
};

function deduplicateIssues(issues) {
  const seen = new Set();
  return issues.filter((issue) => {
    const key = `${issue.type}:${issue.text.toLowerCase()}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

// Scale raw score by text length: longer text gets more chances to trigger.
function normalizeScore(rawScore, wordCount) {
  const lengthFactor = Math.max(1, Math.log2(wordCount / 50));
  return Math.min(100, Math.round(rawScore / lengthFactor));
}

function getLabel(score) {
  if (score === 0) return 'Clean';
  if (score <= 15) return 'Minimal AI signals';
  if (score <= 35) return 'Some AI patterns';
  if (score <= 60) return 'Moderate AI signals';
  if (score <= 80) return 'Strong AI signals';
  return 'Heavy AI patterns';
}

function getColor(score) {
  if (score <= 15) return '#44bb66';
  if (score <= 35) return '#88bb44';
  if (score <= 60) return '#ddaa00';
  if (score <= 80) return '#ff8833';
  return '#ff4444';
}

module.exports = {
  ISSUE_WEIGHTS,
  deduplicateIssues,
  normalizeScore,
  getLabel,
  getColor,
};
