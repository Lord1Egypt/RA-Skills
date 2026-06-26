// knowledgeBase.js — Persistent, compounding knowledge store.
// Replaces the 90-day epigenetic decay with permanent lessons.
// Knowledge only grows — confidence adjusts but entries never delete.

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.resolve(__dirname, '..', '..', 'memory');
const KB_PATH = path.join(MEMORY_DIR, 'knowledge.json');

function ensureMemoryDir() {
  try {
    if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
  } catch {}
}

function loadKnowledge() {
  ensureMemoryDir();
  try {
    if (fs.existsSync(KB_PATH)) {
      return JSON.parse(fs.readFileSync(KB_PATH, 'utf8'));
    }
  } catch {}
  return { lessons: [], version: 1 };
}

function saveKnowledge(kb) {
  ensureMemoryDir();
  const tmp = KB_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(kb, null, 2), 'utf8');
  fs.renameSync(tmp, KB_PATH);
}

// Record an outcome for a gene applied to an error cluster + environment.
function recordOutcome({ errorHash, geneId, success, environment }) {
  if (!geneId || !errorHash) return null;

  const kb = loadKnowledge();
  const key = `${errorHash}|${geneId}|${environment || 'unknown'}`;

  let lesson = kb.lessons.find(l => l.key === key);
  if (lesson) {
    if (success) {
      lesson.times_succeeded++;
      lesson.confidence = Math.min(1.0, lesson.confidence + 0.05);
    } else {
      lesson.times_failed = (lesson.times_failed || 0) + 1;
      lesson.confidence = Math.max(0.01, lesson.confidence - 0.1);
    }
    lesson.times_applied++;
    lesson.last_applied = new Date().toISOString();
  } else {
    lesson = {
      key,
      error_hash: String(errorHash),
      gene_id: String(geneId),
      environment: String(environment || 'unknown'),
      confidence: success ? 0.6 : 0.1,
      times_applied: 1,
      times_succeeded: success ? 1 : 0,
      times_failed: success ? 0 : 1,
      created_at: new Date().toISOString(),
      last_applied: new Date().toISOString(),
    };
    kb.lessons.push(lesson);
  }

  saveKnowledge(kb);
  return lesson;
}

// Get ranked lessons for a given error hash and environment.
function getLessons(errorHash, environment) {
  if (!errorHash) return [];
  const kb = loadKnowledge();
  const env = environment || 'unknown';

  return kb.lessons
    .filter(l => l.error_hash === errorHash)
    .sort((a, b) => {
      // Prefer same environment, then by confidence
      const envMatchA = a.environment === env ? 1 : 0;
      const envMatchB = b.environment === env ? 1 : 0;
      if (envMatchA !== envMatchB) return envMatchB - envMatchA;
      return b.confidence - a.confidence;
    });
}

// Get knowledge base stats for reporting.
function getKnowledgeStats() {
  const kb = loadKnowledge();
  const lessons = kb.lessons;

  if (lessons.length === 0) {
    return { total_lessons: 0, top_genes: [], avg_confidence: 0, improvement_trend: 'none' };
  }

  // Top 5 most reliable genes
  const geneScores = {};
  for (const l of lessons) {
    if (!geneScores[l.gene_id]) geneScores[l.gene_id] = { total_conf: 0, count: 0, successes: 0 };
    geneScores[l.gene_id].total_conf += l.confidence;
    geneScores[l.gene_id].count++;
    geneScores[l.gene_id].successes += l.times_succeeded;
  }

  const topGenes = Object.entries(geneScores)
    .map(([id, s]) => ({ gene_id: id, avg_confidence: s.total_conf / s.count, applications: s.count, successes: s.successes }))
    .sort((a, b) => b.avg_confidence - a.avg_confidence)
    .slice(0, 5);

  const avgConf = lessons.reduce((s, l) => s + l.confidence, 0) / lessons.length;

  // Improvement trend: compare recent vs older lessons
  const sorted = [...lessons].sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  const mid = Math.floor(sorted.length / 2);
  const olderAvg = mid > 0 ? sorted.slice(0, mid).reduce((s, l) => s + l.confidence, 0) / mid : 0;
  const newerAvg = mid > 0 ? sorted.slice(mid).reduce((s, l) => s + l.confidence, 0) / (sorted.length - mid) : 0;
  const trend = newerAvg > olderAvg + 0.05 ? 'improving' : newerAvg < olderAvg - 0.05 ? 'declining' : 'stable';

  return {
    total_lessons: lessons.length,
    top_genes: topGenes,
    avg_confidence: avgConf,
    improvement_trend: trend,
  };
}

// Get the best gene recommendation for a given error.
function recommend(errorHash, environment) {
  const lessons = getLessons(errorHash, environment);
  if (lessons.length === 0) return null;
  const best = lessons[0];
  return best.confidence >= 0.3 ? { gene_id: best.gene_id, confidence: best.confidence } : null;
}

module.exports = {
  recordOutcome,
  getLessons,
  getKnowledgeStats,
  recommend,
  loadKnowledge,
  saveKnowledge,
};
