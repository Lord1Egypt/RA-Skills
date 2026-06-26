// predictor.js — Local trained classifier that predicts which gene
// will fix a given error. Uses feedback data as training set.
// Implements k-NN with embedding vectors — no external ML libraries needed.

const fs = require('fs');
const path = require('path');
const { getTrainingData } = require('./feedbackLoop');
const { embedText, cosineSimilarity } = require('./embeddings');

const MEMORY_DIR = path.resolve(__dirname, '..', '..', 'memory');
const MODEL_PATH = path.join(MEMORY_DIR, 'predictor.json');
const MIN_SAMPLES = 20; // Cold start protection
const K_NEIGHBORS = 5;

function ensureMemoryDir() {
  try {
    if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
  } catch {}
}

function loadModel() {
  ensureMemoryDir();
  try {
    if (fs.existsSync(MODEL_PATH)) {
      return JSON.parse(fs.readFileSync(MODEL_PATH, 'utf8'));
    }
  } catch {}
  return { samples: [], trained_at: null, sample_count: 0, version: 1 };
}

function saveModel(model) {
  ensureMemoryDir();
  const tmp = MODEL_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(model), 'utf8');
  fs.renameSync(tmp, MODEL_PATH);
}

// Train (rebuild) the model from feedback data.
// Stores embedded samples for k-NN lookup.
async function train() {
  const data = getTrainingData();
  if (data.length < MIN_SAMPLES) {
    return { ok: false, reason: 'insufficient_data', count: data.length, needed: MIN_SAMPLES };
  }

  const samples = [];
  for (const entry of data) {
    const signalText = Array.isArray(entry.signals) ? entry.signals.join(' ') : '';
    if (!signalText) continue;

    const vec = await embedText(signalText);
    if (!vec) continue;

    samples.push({
      gene_id: entry.gene_id,
      outcome: entry.status, // 'proven' or 'failed'
      env: entry.env,
      vector: Array.from(vec),
    });
  }

  if (samples.length < MIN_SAMPLES) {
    return { ok: false, reason: 'insufficient_embeddings', count: samples.length, needed: MIN_SAMPLES };
  }

  const model = {
    samples,
    trained_at: new Date().toISOString(),
    sample_count: samples.length,
    version: 1,
  };
  saveModel(model);

  // Compute per-gene accuracy
  const geneStats = {};
  for (const s of samples) {
    if (!geneStats[s.gene_id]) geneStats[s.gene_id] = { proven: 0, failed: 0 };
    geneStats[s.gene_id][s.outcome]++;
  }

  return {
    ok: true,
    sample_count: samples.length,
    gene_count: Object.keys(geneStats).length,
    gene_stats: geneStats,
  };
}

// Predict which genes will work for a given error.
// Returns ranked list: [{gene_id, confidence, votes}]
async function predict(errorSignals, environment) {
  const model = loadModel();
  if (!model.samples || model.samples.length < MIN_SAMPLES) {
    return { ok: false, reason: 'model_not_trained', predictions: [] };
  }

  const signalText = Array.isArray(errorSignals) ? errorSignals.join(' ') : String(errorSignals);
  const vec = await embedText(signalText);
  if (!vec) return { ok: false, reason: 'embedding_failed', predictions: [] };

  // k-NN: find K most similar training samples
  const similarities = model.samples.map(s => ({
    gene_id: s.gene_id,
    outcome: s.outcome,
    env: s.env,
    similarity: cosineSimilarity(vec, new Float64Array(s.vector)),
  }));

  similarities.sort((a, b) => b.similarity - a.similarity);
  const neighbors = similarities.slice(0, K_NEIGHBORS);

  // Aggregate votes per gene (only "proven" neighbors vote positively)
  const votes = {};
  for (const n of neighbors) {
    if (!votes[n.gene_id]) votes[n.gene_id] = { positive: 0, negative: 0, total_sim: 0 };
    if (n.outcome === 'proven') {
      votes[n.gene_id].positive += n.similarity;
    } else {
      votes[n.gene_id].negative += n.similarity;
    }
    votes[n.gene_id].total_sim += n.similarity;
  }

  // Rank by net positive weighted votes
  const predictions = Object.entries(votes)
    .map(([gene_id, v]) => ({
      gene_id,
      confidence: v.total_sim > 0 ? v.positive / v.total_sim : 0,
      positive_votes: v.positive,
      negative_votes: v.negative,
    }))
    .filter(p => p.confidence > 0.3) // Minimum confidence threshold
    .sort((a, b) => b.confidence - a.confidence);

  return { ok: true, predictions, method: 'knn', k: K_NEIGHBORS };
}

// Check if the model has enough data to be active.
function isModelReady() {
  const model = loadModel();
  return model.samples && model.samples.length >= MIN_SAMPLES;
}

// Get model stats.
function getModelStats() {
  const model = loadModel();
  return {
    ready: model.samples && model.samples.length >= MIN_SAMPLES,
    sample_count: model.sample_count || 0,
    trained_at: model.trained_at,
    min_required: MIN_SAMPLES,
  };
}

module.exports = {
  train,
  predict,
  isModelReady,
  getModelStats,
  loadModel,
  MIN_SAMPLES,
  K_NEIGHBORS,
};
