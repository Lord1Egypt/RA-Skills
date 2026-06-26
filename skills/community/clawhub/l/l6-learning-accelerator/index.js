/**
 * l6-learning-accelerator
 * Learning Accelerator Skill - Main Entry Point
 * 
 * Provides 2-signal fusion retrieval (Vector + Time),
 * temporal routing, and progress tracking.
 */

const retrieval = require('./src/retrieval');
const temporal = require('./src/temporal');
const progress = require('./src/progress');

module.exports = {
  // Retrieval
  retrieve: retrieval.retrieve,
  batchRetrieve: retrieval.batchRetrieve,
  calculateTemporalScore: retrieval.calculateTemporalScore,
  cosineSimilarity: retrieval.cosineSimilarity,
  fuseScores: retrieval.fuseScores,
  getRetrievalStats: retrieval.getRetrievalStats,
  
  // Temporal
  detect_temporal: temporal.detect_temporal,
  get_date_range: temporal.get_date_range,
  getRelativeTime: temporal.getRelativeTime,
  TEMPORAL_PATTERNS: temporal.TEMPORAL_PATTERNS,
  
  // Progress
  track_progress: progress.track_progress,
  get_report: progress.get_report,
  set_milestone: progress.set_milestone,
  checkMilestone: progress.checkMilestone,
  calculateStreak: progress.calculateStreak,
  clear_sessions: progress.clear_sessions,
  get_all_sessions: progress.get_all_sessions,
  export_to_file: progress.export_to_file,
  import_from_file: progress.import_from_file
};
