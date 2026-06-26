const { describe, it, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

// Override memory dir before requiring the module
const MEMORY_DIR = path.resolve(__dirname, '..', 'memory');
const FEEDBACK_PATH = path.join(MEMORY_DIR, 'feedback.jsonl');

const {
  recordApplication,
  checkOutcomes,
  getFeedbackStats,
  getProvenGenes,
  getTrainingData,
  loadFeedback,
  hashError,
  extractErrorSignatures,
  CYCLES_TO_PROVE,
  CYCLES_TO_FAIL,
} = require('../src/ml/feedbackLoop');

function cleanup() {
  try { if (fs.existsSync(FEEDBACK_PATH)) fs.unlinkSync(FEEDBACK_PATH); } catch {}
}

describe('feedbackLoop', () => {
  beforeEach(() => cleanup());

  it('records application with error signals', () => {
    const entry = recordApplication({
      geneId: 'gene_repair_1',
      signals: ['log_error', 'errsig:TypeError: Cannot read property x'],
      environment: 'darwin/arm64/v20',
    });
    assert.ok(entry);
    assert.equal(entry.gene_id, 'gene_repair_1');
    assert.equal(entry.status, 'pending');
    assert.ok(entry.error_hash);
  });

  it('returns null when no error signals present', () => {
    const entry = recordApplication({
      geneId: 'gene_repair_1',
      signals: ['stable_success_plateau'],
      environment: 'darwin/arm64/v20',
    });
    assert.equal(entry, null);
  });

  it('marks gene as proven after clean cycles', () => {
    recordApplication({
      geneId: 'gene_repair_1',
      signals: ['errsig:ECONNREFUSED'],
      environment: 'test',
    });

    // Simulate cycles without the error recurring
    for (let i = 0; i < CYCLES_TO_PROVE; i++) {
      checkOutcomes(['stable_success_plateau']);
    }

    const stats = getFeedbackStats();
    assert.equal(stats.proven, 1);
    assert.equal(stats.pending, 0);
  });

  it('marks gene as failed when error recurs', () => {
    recordApplication({
      geneId: 'gene_repair_1',
      signals: ['errsig:ECONNREFUSED'],
      environment: 'test',
    });

    const errorHash = hashError('errsig:ECONNREFUSED');
    // Simulate cycles WITH the error recurring
    for (let i = 0; i < CYCLES_TO_FAIL; i++) {
      checkOutcomes(['errsig:ECONNREFUSED']);
    }

    const stats = getFeedbackStats();
    assert.equal(stats.failed, 1);
  });

  it('extracts error signatures from signals', () => {
    const sigs = extractErrorSignatures([
      'log_error',
      'errsig:TypeError: x is not a function',
      'recurring_errsig(3x):some error',
      'stable_success_plateau',
    ]);
    assert.equal(sigs.length, 2);
    assert.ok(sigs[0].startsWith('errsig:'));
    assert.ok(sigs[1].startsWith('recurring_errsig'));
  });

  it('hashError produces consistent hashes', () => {
    const h1 = hashError('TypeError: x');
    const h2 = hashError('TypeError: x');
    const h3 = hashError('ReferenceError: y');
    assert.equal(h1, h2);
    assert.notEqual(h1, h3);
  });

  it('getTrainingData returns only resolved entries', () => {
    recordApplication({ geneId: 'g1', signals: ['errsig:err1'], environment: 'test' });
    recordApplication({ geneId: 'g2', signals: ['errsig:err2'], environment: 'test' });

    // Prove g1
    for (let i = 0; i < CYCLES_TO_PROVE; i++) {
      checkOutcomes(['stable_success_plateau']);
    }

    const training = getTrainingData();
    assert.ok(training.length >= 1);
    assert.ok(training.some(e => e.status === 'proven'));
  });

  it('getFeedbackStats reports correct counts', () => {
    const stats = getFeedbackStats();
    assert.equal(stats.total, 0);
    assert.equal(stats.pending, 0);
    assert.equal(stats.proven, 0);
    assert.equal(stats.failed, 0);
  });
});
