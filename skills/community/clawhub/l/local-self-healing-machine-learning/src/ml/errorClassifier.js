// errorClassifier.js — Semantic error clustering using Ollama embeddings.
// Replaces pure regex matching with embedding-based similarity detection.
// Falls back to regex when Ollama is unavailable.

const { embedText, cosineSimilarity, clusterErrors, isOllamaAvailable } = require('./embeddings');
const fs = require('fs');
const path = require('path');
const MEMORY_DIR = path.resolve(__dirname, '..', '..', 'memory');
const CLUSTER_REGISTRY_PATH = path.join(MEMORY_DIR, 'cluster-registry.json');

function loadClusterRegistry() {
  try {
    if (fs.existsSync(CLUSTER_REGISTRY_PATH)) {
      return JSON.parse(fs.readFileSync(CLUSTER_REGISTRY_PATH, 'utf8'));
    }
  } catch {}
  return [];
}

function saveClusterRegistry(registry) {
  try {
    if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
    const tmp = CLUSTER_REGISTRY_PATH + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(registry, null, 2), 'utf8');
    fs.renameSync(tmp, CLUSTER_REGISTRY_PATH);
  } catch {}
}

let _clusterRegistry = loadClusterRegistry();

// Classify a set of error lines into semantic clusters.
// Returns cluster assignments: [{clusterId, label, members}]
async function classifyErrors(errorLines) {
  if (!Array.isArray(errorLines) || errorLines.length === 0) return [];

  const available = await isOllamaAvailable();
  if (!available) return []; // Caller falls back to regex

  const clusters = await clusterErrors(errorLines, 0.85);

  // Assign stable cluster IDs based on label hash
  const result = clusters.map((c, idx) => {
    const id = 'cluster_' + require('crypto')
      .createHash('sha256')
      .update(c.label)
      .digest('hex')
      .slice(0, 12);

    // Register cluster for future lookups
    const existing = _clusterRegistry.find(r => r.id === id);
    if (existing) {
      existing.error_count = (existing.error_count || 0) + c.members.length;
      existing.last_seen = new Date().toISOString();
    } else {
      _clusterRegistry.push({
        id,
        label: c.label,
        error_count: c.members.length,
        first_seen: new Date().toISOString(),
        last_seen: new Date().toISOString(),
      });
    }

    return { clusterId: id, label: c.label, members: c.members };
  });

  saveClusterRegistry(_clusterRegistry);
  return result;
}

// Find the best matching cluster for a single error line.
async function findCluster(errorLine) {
  if (!errorLine) return null;
  const available = await isOllamaAvailable();
  if (!available) return null;

  const vec = await embedText(errorLine);
  if (!vec) return null;

  // Compare against known cluster centroids
  let bestMatch = null;
  let bestSim = 0;

  for (const cluster of _clusterRegistry) {
    if (cluster.centroidVec) {
      const sim = cosineSimilarity(vec, new Float64Array(cluster.centroidVec));
      if (sim > bestSim && sim >= 0.85) {
        bestSim = sim;
        bestMatch = cluster;
      }
    }
  }

  return bestMatch ? { clusterId: bestMatch.id, label: bestMatch.label, similarity: bestSim } : null;
}

// Convert signals to cluster-enhanced signals.
// Merges regex-based signals with embedding-based cluster IDs.
async function enhanceSignalsWithClusters(signals) {
  if (!Array.isArray(signals) || signals.length === 0) return signals;

  const available = await isOllamaAvailable();
  if (!available) return signals; // Return unchanged

  // Extract error lines from signals
  const errorSigs = signals.filter(s => String(s).startsWith('errsig:'));
  if (errorSigs.length === 0) return signals;

  const errorTexts = errorSigs.map(s => String(s).replace(/^errsig:/, ''));
  const clusters = await classifyErrors(errorTexts);

  if (clusters.length === 0) return signals;

  // Build enhanced signal list: keep non-error signals, add cluster signals
  const nonErrorSignals = signals.filter(s => !String(s).startsWith('errsig:'));
  const clusterSignals = clusters.map(c => `error_cluster:${c.clusterId}:${c.label.slice(0, 100)}`);

  // Also keep original errsigs for backward compatibility
  return [...nonErrorSignals, ...errorSigs, ...clusterSignals];
}

function getClusterRegistry() {
  return [..._clusterRegistry];
}

function resetClusterRegistry() {
  _clusterRegistry = [];
  saveClusterRegistry(_clusterRegistry);
}

module.exports = {
  classifyErrors,
  findCluster,
  enhanceSignalsWithClusters,
  getClusterRegistry,
  resetClusterRegistry,
};
