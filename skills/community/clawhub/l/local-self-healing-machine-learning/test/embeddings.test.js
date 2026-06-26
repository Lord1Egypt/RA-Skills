const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  cosineSimilarity,
  textHash,
  getCacheStats,
} = require('../src/ml/embeddings');

describe('embeddings', () => {
  it('cosineSimilarity returns 1 for identical vectors', () => {
    const v = new Float64Array([1, 2, 3, 4]);
    assert.ok(Math.abs(cosineSimilarity(v, v) - 1.0) < 0.001);
  });

  it('cosineSimilarity returns 0 for orthogonal vectors', () => {
    const a = new Float64Array([1, 0, 0]);
    const b = new Float64Array([0, 1, 0]);
    assert.ok(Math.abs(cosineSimilarity(a, b)) < 0.001);
  });

  it('cosineSimilarity returns -1 for opposite vectors', () => {
    const a = new Float64Array([1, 0]);
    const b = new Float64Array([-1, 0]);
    assert.ok(Math.abs(cosineSimilarity(a, b) + 1.0) < 0.001);
  });

  it('cosineSimilarity handles zero vectors', () => {
    const a = new Float64Array([0, 0, 0]);
    const b = new Float64Array([1, 2, 3]);
    assert.equal(cosineSimilarity(a, b), 0);
  });

  it('cosineSimilarity handles mismatched lengths', () => {
    const a = new Float64Array([1, 2]);
    const b = new Float64Array([1, 2, 3]);
    assert.equal(cosineSimilarity(a, b), 0);
  });

  it('cosineSimilarity handles null/empty inputs', () => {
    assert.equal(cosineSimilarity(null, null), 0);
    assert.equal(cosineSimilarity(new Float64Array([]), new Float64Array([])), 0);
  });

  it('textHash produces consistent hashes', () => {
    const h1 = textHash('hello world');
    const h2 = textHash('hello world');
    const h3 = textHash('different text');
    assert.equal(h1, h2);
    assert.notEqual(h1, h3);
    assert.equal(h1.length, 24);
  });

  it('getCacheStats returns valid structure', () => {
    const stats = getCacheStats();
    assert.ok('entries' in stats);
    assert.ok('model' in stats);
    assert.ok('url' in stats);
  });
});
