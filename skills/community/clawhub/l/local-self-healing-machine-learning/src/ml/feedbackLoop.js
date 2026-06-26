// feedbackLoop.js — Tracks whether applied fixes actually work.
// After a gene is solidified, records the application. On subsequent cycles,
// checks if the same error pattern recurs. After 3 clean cycles → "proven".
// If error recurs within 5 cycles → "failed". Append-only JSONL store.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const MEMORY_DIR = path.resolve(__dirname, '..', '..', 'memory');
const FEEDBACK_PATH = path.join(MEMORY_DIR, 'feedback.jsonl');

const CYCLES_TO_PROVE = 3;
const CYCLES_TO_FAIL = 5;

function ensureMemoryDir() {
  try {
    if (!fs.existsSync(MEMORY_DIR)) fs.mkdirSync(MEMORY_DIR, { recursive: true });
  } catch {}
}

function hashError(errorText) {
  return crypto.createHash('sha256').update(String(errorText || '')).digest('hex').slice(0, 16);
}

function extractErrorSignatures(signals) {
  if (!Array.isArray(signals)) return [];
  return signals
    .filter(s => String(s).startsWith('errsig:') || String(s).startsWith('recurring_errsig'))
    .map(s => String(s));
}

function loadFeedback() {
  ensureMemoryDir();
  if (!fs.existsSync(FEEDBACK_PATH)) return [];
  try {
    const lines = fs.readFileSync(FEEDBACK_PATH, 'utf8').split('\n').filter(Boolean);
    return lines.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  } catch { return []; }
}

function appendFeedback(entry) {
  ensureMemoryDir();
  fs.appendFileSync(FEEDBACK_PATH, JSON.stringify(entry) + '\n', 'utf8');
}

function updateFeedbackEntry(entries, idx, updates) {
  entries[idx] = { ...entries[idx], ...updates };
  writeFeedbackBulk(entries);
}

function writeFeedbackBulk(entries) {
  ensureMemoryDir();
  const data = entries.map(e => JSON.stringify(e)).join('\n') + '\n';
  const tmp = FEEDBACK_PATH + '.tmp';
  fs.writeFileSync(tmp, data, 'utf8');
  fs.renameSync(tmp, FEEDBACK_PATH);
}

// Record that a gene was applied to fix a specific error pattern.
function recordApplication({ geneId, signals, environment }) {
  if (!geneId) return null;
  const errorSigs = extractErrorSignatures(signals);
  if (errorSigs.length === 0) return null;

  const entry = {
    gene_id: String(geneId),
    signals: errorSigs,
    error_hash: hashError(errorSigs.join('|')),
    applied_at: new Date().toISOString(),
    env: String(environment || 'unknown'),
    status: 'pending',
    cycles_since: 0,
    resolved_at: null,
  };
  appendFeedback(entry);
  return entry;
}

// Check current signals against pending feedback entries.
// Closes the loop: did the fix work?
function checkOutcomes(currentSignals) {
  const entries = loadFeedback();
  if (entries.length === 0) return { proven: [], failed: [], pending: [] };

  const currentErrorSigs = extractErrorSignatures(currentSignals);
  const currentHashes = new Set(currentErrorSigs.map(s => hashError(s)));

  const proven = [];
  const failed = [];
  const pending = [];
  let changed = false;

  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    if (entry.status !== 'pending') continue;

    const errorRecurred = currentHashes.has(entry.error_hash);

    if (errorRecurred) {
      entry.cycles_since = (entry.cycles_since || 0) + 1;
      if (entry.cycles_since >= CYCLES_TO_FAIL) {
        entry.status = 'failed';
        entry.resolved_at = new Date().toISOString();
        failed.push(entry);
      } else {
        pending.push(entry);
      }
      changed = true;
    } else {
      entry.cycles_since = (entry.cycles_since || 0) + 1;
      if (entry.cycles_since >= CYCLES_TO_PROVE) {
        entry.status = 'proven';
        entry.resolved_at = new Date().toISOString();
        proven.push(entry);
      } else {
        pending.push(entry);
      }
      changed = true;
    }
  }

  if (changed) writeFeedbackBulk(entries);
  return { proven, failed, pending };
}

// Get stats for reporting.
function getFeedbackStats() {
  const entries = loadFeedback();
  const byStatus = { pending: 0, proven: 0, failed: 0 };
  for (const e of entries) {
    byStatus[e.status] = (byStatus[e.status] || 0) + 1;
  }
  return {
    total: entries.length,
    ...byStatus,
    success_rate: entries.length > 0
      ? (byStatus.proven / Math.max(1, byStatus.proven + byStatus.failed))
      : 0,
  };
}

// Get all proven gene IDs — useful for the predictor.
function getProvenGenes() {
  const entries = loadFeedback();
  return entries.filter(e => e.status === 'proven').map(e => e.gene_id);
}

// Get all feedback entries for training.
function getTrainingData() {
  return loadFeedback().filter(e => e.status === 'proven' || e.status === 'failed');
}

module.exports = {
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
};
