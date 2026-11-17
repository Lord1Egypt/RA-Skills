/**
 * Chinese tokenizer + text helpers (zh-side).
 *
 * Zero-dependency Chinese segmentation: NO external word-segmentation library.
 * Pattern matching in Chinese doesn't need precise word boundaries — it needs
 * substring/n-gram hits + punctuation-based sentence splitting. This keeps the
 * "runs anywhere" property (Node + browser, no install) that is aaw's signature.
 *
 * Approach:
 *   - sentences: split on CJK + ASCII terminal punctuation
 *   - paragraphs: blank-line separated (same as en)
 *   - tokens: for vocabulary/cluster counting, CJK chars + ASCII word-runs;
 *     Chinese phrases are matched as raw substrings/n-grams, not as tokens
 *   - countWords: for Chinese, counts CJK chars + ASCII word tokens (the
 *     length-normalization gate uses the same notion as en so thresholds
 *     carry over)
 */
'use strict';

// CJK Unified Ideographs (+ compatibility for safety). Used to detect Chinese
// spans and to count Chinese "words" as characters (Chinese has no whitespace).
const CJK_RE = /[\u3400-\u9fff\uf900-\ufaff]/;

function isChineseText(text) {
  // A span is Chinese if CJK chars make up >=30% of its non-space chars.
  const chars = text.replace(/\s/g, '');
  if (chars.length === 0) return false;
  const cjk = (text.match(/[\u3400-\u9fff\uf900-\ufaff]/g) || []).length;
  return cjk / chars.length >= 0.3;
}

function countCjkChars(text) {
  return (text.match(/[\u3400-\u9fff\uf900-\ufaff]/g) || []).length;
}

function countWords(text) {
  // Count CJK chars individually + ASCII word-runs. Keeps the en-style
  // length-normalization gate meaningful for mixed zh/en text.
  const cjk = countCjkChars(text);
  const ascii = (text.match(/[A-Za-z0-9][A-Za-z0-9'-]*/g) || []).length;
  return cjk + ascii;
}

function tokenize(text) {
  // Lowercase ASCII word-runs + individual CJK chars. Used for tier cluster
  // counting and function-word analysis on the ASCII portions; Chinese tier
  // matching uses substring/n-gram hits directly (see vocabulary.js consumers).
  const ascii = text.toLowerCase().match(/[a-z0-9][a-z0-9'-]*/g) || [];
  const cjk = text.match(/[\u3400-\u9fff\uf900-\ufaff]/g) || [];
  return [...ascii, ...cjk];
}

function getParagraphs(text) {
  return text.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
}

function getSentences(text) {
  // Split on CJK terminal punctuation (。！？) and ASCII (.!?).
  return text.split(/[。！？.!?]+/).filter((s) => s.trim().length > 1);
}

// Run an array of regex/string patterns over text, emitting one issue per match.
// Same field shape as en matchPatterns so downstream dedup + scoring is shared.
// `patterns` may be RegExp[] (regex match) or {literal:string, ...}[] handled
// by the caller via substring scan — this fn only does regex.
function matchPatterns(text, patterns, category, severity) {
  const issues = [];
  for (const pat of patterns) {
    const regex = new RegExp(pat.source, pat.flags);
    let match;
    while ((match = regex.exec(text)) !== null) {
      issues.push({
        type: category,
        text: match[0],
        index: match.index,
        severity,
        suggestion: null,
      });
    }
  }
  return issues;
}

module.exports = {
  CJK_RE,
  isChineseText,
  countCjkChars,
  countWords,
  tokenize,
  getParagraphs,
  getSentences,
  matchPatterns,
};
