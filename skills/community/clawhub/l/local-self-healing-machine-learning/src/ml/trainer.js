// trainer.js — Scheduled retraining logic for the success predictor.
// Rebuilds model after every N new feedback entries.

const { loadFeedback } = require('./feedbackLoop');
const { train, loadModel, MIN_SAMPLES } = require('./predictor');

const RETRAIN_INTERVAL = 10; // Retrain after every 10 new feedback entries

// Check if retraining is needed based on feedback count vs model sample count.
function shouldRetrain() {
  const feedback = loadFeedback();
  const resolved = feedback.filter(e => e.status === 'proven' || e.status === 'failed');
  const model = loadModel();
  const modelCount = model.sample_count || 0;

  if (resolved.length < MIN_SAMPLES) return false;
  if (modelCount === 0) return true; // First training
  return (resolved.length - modelCount) >= RETRAIN_INTERVAL;
}

// Run training if needed. Returns training result or skip reason.
async function retrainIfNeeded() {
  if (!shouldRetrain()) {
    return { retrained: false, reason: 'not_needed' };
  }
  const result = await train();
  return { retrained: result.ok, ...result };
}

// Force retrain regardless of interval.
async function forceRetrain() {
  return await train();
}

module.exports = {
  shouldRetrain,
  retrainIfNeeded,
  forceRetrain,
  RETRAIN_INTERVAL,
};
