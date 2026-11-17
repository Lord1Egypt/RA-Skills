/**
 * English tokenizer + text helpers (en-side).
 *
 * Migrated verbatim from avoid-ai-writing's patterns.js helpers. The zh/
 * tokenizer will mirror this interface with CJK-aware splitting in stage 2.
 */
'use strict';

function tokenize(text) {
  return text.toLowerCase().match(/[\w'-]+/g) || [];
}

function countWords(text) {
  return (text.match(/\S+/g) || []).length;
}

function getParagraphs(text) {
  return text.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
}

function getSentences(text) {
  return text.split(/[.!?]+/).filter((s) => s.trim().length > 5);
}

// Run an array of regex patterns over text, emitting one issue per match.
// Mirrors aaw's matchPatterns exactly — same field shape, so the downstream
// dedup + scoring logic is unchanged.
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
  tokenize,
  countWords,
  getParagraphs,
  getSentences,
  matchPatterns,
};
