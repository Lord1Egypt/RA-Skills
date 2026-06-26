// LLM Review — safe stub.
// The shell-based eval pattern has been removed. Auto-approves by default.
// To wire a real review, replace this with your own LLM API call.

function isLlmReviewEnabled() { return false; }

function buildReviewPrompt({ diff, gene, signals, mutation }) {
  var geneId = gene && gene.id ? gene.id : '(unknown)';
  var category = (mutation && mutation.category) || (gene && gene.category) || 'unknown';
  return 'Review gene ' + geneId + ' (' + category + ')';
}

function runLlmReview() { return null; }

module.exports = { isLlmReviewEnabled, runLlmReview, buildReviewPrompt };
