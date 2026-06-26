const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  isModelReady,
  getModelStats,
  MIN_SAMPLES,
  K_NEIGHBORS,
} = require('../src/ml/predictor');

describe('predictor', () => {
  it('model is not ready with no training data', () => {
    assert.equal(isModelReady(), false);
  });

  it('getModelStats returns valid structure', () => {
    const stats = getModelStats();
    assert.ok('ready' in stats);
    assert.ok('sample_count' in stats);
    assert.ok('trained_at' in stats);
    assert.ok('min_required' in stats);
    assert.equal(stats.min_required, MIN_SAMPLES);
  });

  it('MIN_SAMPLES is 20', () => {
    assert.equal(MIN_SAMPLES, 20);
  });

  it('K_NEIGHBORS is 5', () => {
    assert.equal(K_NEIGHBORS, 5);
  });
});
