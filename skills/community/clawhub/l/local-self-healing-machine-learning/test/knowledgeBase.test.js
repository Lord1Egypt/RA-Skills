const { describe, it, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.resolve(__dirname, '..', 'memory');
const KB_PATH = path.join(MEMORY_DIR, 'knowledge.json');

const {
  recordOutcome,
  getLessons,
  getKnowledgeStats,
  recommend,
  loadKnowledge,
} = require('../src/ml/knowledgeBase');

function cleanup() {
  try { if (fs.existsSync(KB_PATH)) fs.unlinkSync(KB_PATH); } catch {}
}

describe('knowledgeBase', () => {
  beforeEach(() => cleanup());

  it('records a successful outcome', () => {
    const lesson = recordOutcome({
      errorHash: 'abc123',
      geneId: 'gene_repair_1',
      success: true,
      environment: 'darwin/arm64/v20',
    });
    assert.ok(lesson);
    assert.equal(lesson.gene_id, 'gene_repair_1');
    assert.equal(lesson.times_succeeded, 1);
    assert.equal(lesson.times_failed, 0);
    assert.ok(lesson.confidence > 0);
  });

  it('records a failed outcome', () => {
    const lesson = recordOutcome({
      errorHash: 'abc123',
      geneId: 'gene_repair_1',
      success: false,
      environment: 'test',
    });
    assert.equal(lesson.times_failed, 1);
    assert.equal(lesson.times_succeeded, 0);
    assert.ok(lesson.confidence < 0.5);
  });

  it('compounds confidence with repeated success', () => {
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });

    const lessons = getLessons('abc', 'test');
    assert.equal(lessons.length, 1);
    assert.equal(lessons[0].times_applied, 3);
    assert.equal(lessons[0].times_succeeded, 3);
    assert.ok(lessons[0].confidence > 0.6);
  });

  it('decreases confidence on failure but never deletes', () => {
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: false, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: false, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: false, environment: 'test' });

    const lessons = getLessons('abc', 'test');
    assert.equal(lessons.length, 1);
    assert.ok(lessons[0].confidence > 0); // Never reaches 0
    assert.ok(lessons[0].confidence < 0.5);
  });

  it('no decay — knowledge persists indefinitely', () => {
    recordOutcome({ errorHash: 'old', geneId: 'g1', success: true, environment: 'test' });
    const kb = loadKnowledge();
    // Manually backdate the lesson
    kb.lessons[0].created_at = '2020-01-01T00:00:00.000Z';
    const { saveKnowledge } = require('../src/ml/knowledgeBase');
    saveKnowledge(kb);

    const lessons = getLessons('old', 'test');
    assert.equal(lessons.length, 1); // Still there — no decay
  });

  it('getKnowledgeStats returns valid structure', () => {
    const stats = getKnowledgeStats();
    assert.ok('total_lessons' in stats);
    assert.ok('top_genes' in stats);
    assert.ok('avg_confidence' in stats);
    assert.ok('improvement_trend' in stats);
  });

  it('recommend returns best gene for known error', () => {
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });
    recordOutcome({ errorHash: 'abc', geneId: 'g1', success: true, environment: 'test' });

    const rec = recommend('abc', 'test');
    assert.ok(rec);
    assert.equal(rec.gene_id, 'g1');
    assert.ok(rec.confidence > 0);
  });

  it('recommend returns null for unknown error', () => {
    const rec = recommend('unknown_hash', 'test');
    assert.equal(rec, null);
  });

  it('prefers same-environment lessons', () => {
    recordOutcome({ errorHash: 'abc', geneId: 'g_darwin', success: true, environment: 'darwin' });
    recordOutcome({ errorHash: 'abc', geneId: 'g_darwin', success: true, environment: 'darwin' });
    recordOutcome({ errorHash: 'abc', geneId: 'g_linux', success: true, environment: 'linux' });

    const lessons = getLessons('abc', 'darwin');
    assert.equal(lessons[0].gene_id, 'g_darwin');
  });
});
