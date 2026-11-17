/**
 * core/trinary — FN-biased trinary classification + sentence regions.
 *
 * Migrated verbatim from avoid-ai-writing. Decouples confidence from
 * AI-proportion: maps the 0-100 score plus structural signals into
 * HUMAN_ONLY / MIXED / AI_ONLY with a confidence band. Thresholds are
 * FN-biased — ambiguity routes to MIXED, never AI_ONLY.
 *
 * Also builds sentence-region highlights (HMM-style without an HMM) so
 * integrators get "this paragraph is AI" rather than scattered hits.
 *
 * Shape mirrors GPTZero so integrators can swap in.
 */
'use strict';

const { ISSUE_WEIGHTS } = require('./scoring');

function buildSentenceRegions(text, issues) {
  const sentences = [];
  const sentenceRe = /[^.!?]+[.!?]+|\S[^.!?]*$/g;
  let m;
  while ((m = sentenceRe.exec(text)) !== null) {
    const trimmed = m[0].trim();
    if (trimmed.length < 4) continue;
    sentences.push({ start: m.index, end: m.index + m[0].length, text: trimmed });
  }
  if (sentences.length === 0) return [];

  const SUMMARY_ONLY_TYPES = new Set([
    'punct-distribution',
    'cross-para-burstiness',
    'fnword-trigram-entropy',
    'smart-punct-signature',
    'normalization-flag',
    'uniformity',
    'em-dash',
    'formatting',
    'tier3',
    'tier3-phrase',
    'tier3-phrase-cluster',
    'hashtag-stuff',
    'bullet-np-list',
  ]);
  const hits = sentences.map(() => ({ count: 0, weight: 0 }));
  const lowerText = text.toLowerCase();
  let unmappedHighlights = 0;
  for (const issue of issues) {
    if (!issue.text || issue.text.length > 200) continue;
    if (SUMMARY_ONLY_TYPES.has(issue.type)) continue;
    const needle = issue.text.toLowerCase();
    let idx = 0;
    let matched = false;
    while ((idx = lowerText.indexOf(needle, idx)) !== -1) {
      matched = true;
      for (let i = 0; i < sentences.length; i++) {
        if (idx >= sentences[i].start && idx < sentences[i].end) {
          hits[i].count++;
          hits[i].weight += ISSUE_WEIGHTS[issue.type] ?? 2;
          break;
        }
      }
      idx += needle.length;
    }
    if (!matched) unmappedHighlights++;
  }

  const regions = [];
  let cur = null;
  for (let i = 0; i < sentences.length; i++) {
    if (hits[i].count > 0) {
      if (cur === null) {
        cur = { startSentence: i, endSentence: i, start: sentences[i].start, end: sentences[i].end, hitCount: hits[i].count, weight: hits[i].weight };
      } else {
        cur.endSentence = i;
        cur.end = sentences[i].end;
        cur.hitCount += hits[i].count;
        cur.weight += hits[i].weight;
      }
    } else if (cur !== null) {
      const next = hits[i + 1];
      if (next && next.count > 0) {
        cur.endSentence = i;
        cur.end = sentences[i].end;
        continue;
      }
      regions.push(finalizeRegion(cur));
      cur = null;
    }
  }
  if (cur !== null) regions.push(finalizeRegion(cur));
  Object.defineProperty(regions, '_unmapped', { value: unmappedHighlights, enumerable: false });
  return regions;
}

function finalizeRegion(r) {
  const score = Math.min(1, r.weight / 20);
  return {
    startSentence: r.startSentence,
    endSentence: r.endSentence,
    start: r.start,
    end: r.end,
    hitCount: r.hitCount,
    score: Math.round(score * 100) / 100,
  };
}

function classifyTrinary({ score, issues, regions, normFlags, wordCount, denseAIVocab }) {
  const hasCutoff = issues.some((i) => i.type === 'cutoff-disclaimer');
  const hasNormFlag = normFlags.zeroWidth >= 2 || normFlags.homoglyph >= 2;
  const hasReasoning = issues.some((i) => i.type === 'reasoning-artifact');
  const hasChatbot = issues.some((i) => i.type === 'chatbot');
  const strongCorrob =
    (hasCutoff ? 1 : 0) +
    (hasNormFlag ? 1 : 0) +
    (hasReasoning && hasChatbot ? 1 : 0) +
    (denseAIVocab ? 1 : 0);

  const stylometricHits = ['punct-distribution', 'cross-para-burstiness', 'fnword-trigram-entropy']
    .filter((t) => issues.some((i) => i.type === t)).length;
  const hasSmartPunct = issues.some((i) => i.type === 'smart-punct-signature');
  const weakCorrob = (stylometricHits >= 2 ? 1 : 0) + (hasSmartPunct ? 1 : 0);

  const totalCorrob = strongCorrob + weakCorrob;
  let classification;
  if (score < 15 && strongCorrob === 0) classification = 'HUMAN_ONLY';
  else if (strongCorrob >= 1 || score >= 70) classification = 'AI_ONLY';
  else if (score >= 40 && totalCorrob >= 1) classification = 'AI_ONLY';
  else classification = 'MIXED';

  const aiSoft = Math.min(0.97, score / 100 + totalCorrob * 0.06 + strongCorrob * 0.08);
  let p;
  if (classification === 'HUMAN_ONLY') p = { human: Math.max(0.6, 1 - aiSoft), mixed: Math.min(0.35, aiSoft * 0.8), ai: Math.min(0.1, aiSoft * 0.3) };
  else if (classification === 'AI_ONLY') p = { human: Math.max(0.02, 1 - aiSoft - 0.05), mixed: 0.1, ai: aiSoft };
  else p = { human: Math.max(0.15, 0.6 - aiSoft * 0.5), mixed: 0.5, ai: aiSoft * 0.7 };
  const rawSum = p.human + p.mixed + p.ai;
  p.human = +(p.human / rawSum).toFixed(3);
  p.mixed = +(p.mixed / rawSum).toFixed(3);
  p.ai = Math.max(0, +(1 - p.human - p.mixed).toFixed(3));
  const probabilities = p;

  let confidence;
  if (strongCorrob >= 2 || hasCutoff || (score < 8 && wordCount >= 100)) confidence = 'high';
  else if (strongCorrob >= 1 || (score >= 45 && weakCorrob >= 1) || score < 20) confidence = 'medium';
  else confidence = 'low';

  return { classification, probabilities, confidence };
}

module.exports = {
  buildSentenceRegions,
  classifyTrinary,
};
