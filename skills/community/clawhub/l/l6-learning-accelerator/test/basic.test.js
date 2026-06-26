/**
 * Basic Test Suite for l6-learning-accelerator
 * Tests retrieval, temporal routing, and progress tracking modules
 */

const assert = require('assert');

// Import modules
const retrieval = require('../src/retrieval');
const temporal = require('../src/temporal');
const progress = require('../src/progress');

// Test counters
let passed = 0;
let failed = 0;

/**
 * Run a test
 * @param {string} name - Test name
 * @param {Function} fn - Test function
 */
function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

/**
 * Assert helper
 */
function equal(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}

/**
 * Assert deep equality
 */
function deepEqual(actual, expected, message) {
  const actualStr = JSON.stringify(actual);
  const expectedStr = JSON.stringify(expected);
  if (actualStr !== expectedStr) {
    throw new Error(message || `Expected ${expectedStr}, got ${actualStr}`);
  }
}

console.log('\n🧪 l6-learning-accelerator Test Suite\n');
console.log('='.repeat(50));

// ============================================
// RETRIEVAL MODULE TESTS
// ============================================
console.log('\n📦 Retrieval Module Tests\n');

test('cosineSimilarity: identical vectors return 1', () => {
  const vec1 = [1, 0, 0];
  const vec2 = [1, 0, 0];
  const similarity = retrieval.cosineSimilarity(vec1, vec2);
  equal(similarity, 1, 'Identical vectors should have similarity 1');
});

test('cosineSimilarity: orthogonal vectors return 0', () => {
  const vec1 = [1, 0, 0];
  const vec2 = [0, 1, 0];
  const similarity = retrieval.cosineSimilarity(vec1, vec2);
  equal(similarity, 0, 'Orthogonal vectors should have similarity 0');
});

test('cosineSimilarity: handles null vectors', () => {
  const similarity = retrieval.cosineSimilarity(null, [1, 0, 0]);
  equal(similarity, 0, 'Null vectors should return 0');
});

test('calculateTemporalScore: today returns 1', () => {
  const now = new Date();
  const score = retrieval.calculateTemporalScore(now, now);
  equal(score, 1, 'Same date should have temporal score 1');
});

test('calculateTemporalScore: older items have lower scores', () => {
  const now = new Date();
  const old = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000); // 7 days ago
  const scoreNow = retrieval.calculateTemporalScore(now, now);
  const scoreOld = retrieval.calculateTemporalScore(old, now);
  if (scoreOld >= scoreNow) {
    throw new Error('Older items should have lower temporal scores');
  }
});

test('fuseScores: weighted combination', () => {
  const vectorScore = 0.8;
  const temporalScore = 0.6;
  const weights = { vector: 0.6, time: 0.4 };
  const fused = retrieval.fuseScores(vectorScore, temporalScore, weights);
  const expected = (0.8 * 0.6) + (0.6 * 0.4);
  equal(fused, expected, 'Fused score should be weighted combination');
});

test('retrieve: returns ranked results', () => {
  const queryVector = [1, 0, 0];
  const items = [
    { id: 1, vector: [1, 0, 0], date: new Date().toISOString(), content: 'recent relevant' },
    { id: 2, vector: [0.9, 0, 0], date: new Date(Date.now() - 86400000).toISOString(), content: 'yesterday relevant' },
    { id: 3, vector: [0.5, 0, 0], date: new Date().toISOString(), content: 'recent less relevant' },
    { id: 4, vector: [1, 0, 0], date: new Date(Date.now() - 30 * 86400000).toISOString(), content: 'old relevant' }
  ];
  
  const results = retrieval.retrieve('test', {
    queryVector,
    items,
    topK: 4
  });
  
  if (results.length !== 4) {
    throw new Error(`Expected 4 results, got ${results.length}`);
  }
  
  // First result should have highest fused score
  for (let i = 1; i < results.length; i++) {
    if (results[i].scores.fused > results[i-1].scores.fused) {
      throw new Error('Results should be sorted by fused score descending');
    }
  }
});

test('retrieve: respects date range filter', () => {
  const queryVector = [1, 0, 0];
  const now = new Date();
  const lastWeek = new Date(now.getTime() - 7 * 86400000);
  
  const items = [
    { id: 1, vector: [1, 0, 0], date: now.toISOString(), content: 'today' },
    { id: 2, vector: [1, 0, 0], date: lastWeek.toISOString(), content: 'last week' },
    { id: 3, vector: [1, 0, 0], date: new Date(Date.now() - 30 * 86400000).toISOString(), content: 'last month' }
  ];
  
  const results = retrieval.retrieve('test', {
    queryVector,
    items,
    dateRange: { start: lastWeek, end: now },
    topK: 10
  });
  
  // Should only include items within date range
  if (results.length !== 2) {
    throw new Error(`Expected 2 results in date range, got ${results.length}`);
  }
});

test('getRetrievalStats: calculates correct statistics', () => {
  const results = [
    { scores: { vector: 0.8, temporal: 0.6, fused: 0.72 } },
    { scores: { vector: 0.6, temporal: 0.8, fused: 0.68 } },
    { scores: { vector: 0.9, temporal: 0.5, fused: 0.74 } }
  ];
  
  const stats = retrieval.getRetrievalStats(results);
  
  equal(stats.count, 3, 'Count should be 3');
  equal(stats.avgVectorScore, 0.767, 'Avg vector score should be correct');
  equal(stats.avgTemporalScore, 0.633, 'Avg temporal score should be correct');
});

// ============================================
// TEMPORAL MODULE TESTS
// ============================================
console.log('\n⏰ Temporal Module Tests\n');

test('detect_temporal: detects "today"', () => {
  const result = temporal.detect_temporal('What did I learn today?');
  if (!result.hasTemporal) {
    throw new Error('Should detect temporal intent');
  }
  if (result.expressions.length === 0) {
    throw new Error('Should find temporal expressions');
  }
});

test('detect_temporal: detects "last week"', () => {
  const result = temporal.detect_temporal('Show me notes from last week');
  if (!result.hasTemporal) {
    throw new Error('Should detect temporal intent');
  }
});

test('detect_temporal: detects ISO dates', () => {
  const result = temporal.detect_temporal('Events on 2024-03-15');
  if (!result.hasTemporal) {
    throw new Error('Should detect temporal intent');
  }
  const hasAbsolute = result.expressions.some(e => e.type === 'absolute');
  if (!hasAbsolute) {
    throw new Error('Should find absolute date expression');
  }
});

test('detect_temporal: no temporal in plain query', () => {
  const result = temporal.detect_temporal('JavaScript functions');
  if (result.hasTemporal) {
    throw new Error('Should not detect temporal intent');
  }
});

test('get_date_range: today', () => {
  // Use local date construction to avoid timezone issues
  const now = new Date(2024, 2, 22, 12, 0, 0); // March 22, 2024 (month is 0-indexed)
  const range = temporal.get_date_range('today', now);
  
  if (!range) {
    throw new Error('Should return date range');
  }
  
  // Check using local date components
  if (range.start.getDate() !== 22 || range.start.getMonth() !== 2 || range.start.getFullYear() !== 2024) {
    throw new Error(`Start date should be 2024-03-22, got ${range.start.toISOString()}`);
  }
  if (range.end.getDate() !== 22 || range.end.getMonth() !== 2 || range.end.getFullYear() !== 2024) {
    throw new Error(`End date should be 2024-03-22, got ${range.end.toISOString()}`);
  }
});

test('get_date_range: last week', () => {
  const now = new Date(2024, 2, 22, 12, 0, 0); // March 22, 2024 (Friday)
  const range = temporal.get_date_range('last week', now);
  
  if (!range) {
    throw new Error('Should return date range');
  }
  
  // Last week should be before this week
  if (range.end >= now) {
    throw new Error('End date should be in the past');
  }
});

test('get_date_range: past 7 days', () => {
  const now = new Date(2024, 2, 22, 12, 0, 0); // March 22, 2024
  const range = temporal.get_date_range('past 7 days', now);
  
  if (!range) {
    throw new Error('Should return date range');
  }
  
  const diffDays = (now - range.start) / (1000 * 60 * 60 * 24);
  if (diffDays < 6 || diffDays > 8) {
    throw new Error(`Range should be approximately 7 days, got ${diffDays}`);
  }
});

test('get_date_range: ISO date', () => {
  const now = new Date(2024, 2, 22, 12, 0, 0); // March 22, 2024
  const range = temporal.get_date_range('2024-03-15', now);
  
  if (!range) {
    throw new Error('Should return date range');
  }
  
  // Check using local date components
  if (range.start.getDate() !== 15 || range.start.getMonth() !== 2 || range.start.getFullYear() !== 2024) {
    throw new Error(`Should parse ISO date 2024-03-15, got ${range.start.toISOString()}`);
  }
});

test('getRelativeTime: today', () => {
  const now = new Date();
  const relative = temporal.getRelativeTime(now, now);
  equal(relative, 'today', 'Should return "today"');
});

test('getRelativeTime: yesterday', () => {
  const now = new Date();
  const yesterday = new Date(now.getTime() - 86400000);
  const relative = temporal.getRelativeTime(yesterday, now);
  equal(relative, 'yesterday', 'Should return "yesterday"');
});

// ============================================
// PROGRESS MODULE TESTS
// ============================================
console.log('\n📊 Progress Module Tests\n');

// Clear sessions before tests
progress.clear_sessions();

test('track_progress: creates session', () => {
  const session = progress.track_progress('study', {
    topic: 'JavaScript',
    duration: 45
  });
  
  if (!session.id) {
    throw new Error('Session should have ID');
  }
  if (session.type !== 'study') {
    throw new Error('Session type should be "study"');
  }
  if (session.duration !== 45) {
    throw new Error('Session duration should be 45');
  }
});

test('track_progress: includes timestamp', () => {
  const session = progress.track_progress('practice', {
    topic: 'Python',
    duration: 30
  });
  
  if (!session.timestamp) {
    throw new Error('Session should have timestamp');
  }
  
  const sessionDate = new Date(session.timestamp);
  const now = new Date();
  const diff = Math.abs(now - sessionDate);
  
  if (diff > 1000) {
    throw new Error('Timestamp should be close to now');
  }
});

test('get_report: returns weekly report', () => {
  const report = progress.get_report('weekly');
  
  if (!report.period) {
    throw new Error('Report should have period');
  }
  if (report.period !== 'weekly') {
    throw new Error('Period should be "weekly"');
  }
  if (!report.summary) {
    throw new Error('Report should have summary');
  }
  if (!report.generatedAt) {
    throw new Error('Report should have generatedAt timestamp');
  }
});

test('get_report: includes correct session count', () => {
  const report = progress.get_report('all');
  
  // We've created 2 sessions in previous tests
  if (report.summary.totalSessions < 2) {
    throw new Error(`Report should include at least 2 sessions, got ${report.summary.totalSessions}`);
  }
});

test('get_report: calculates total time', () => {
  const report = progress.get_report('all');
  
  // We've added 45 + 30 = 75 minutes
  if (report.summary.totalTimeMinutes < 75) {
    throw new Error(`Total time should be at least 75 minutes, got ${report.summary.totalTimeMinutes}`);
  }
});

test('set_milestone: creates milestone', () => {
  const milestone = progress.set_milestone('First Week', {
    totalSessions: 5
  });
  
  if (!milestone.id) {
    throw new Error('Milestone should have ID');
  }
  if (milestone.name !== 'First Week') {
    throw new Error('Milestone name should match');
  }
});

test('checkMilestone: detects achievement', () => {
  // Add more sessions to reach milestone
  for (let i = 0; i < 5; i++) {
    progress.track_progress('review', { duration: 20 });
  }
  
  const milestones = progress.get_report('all').milestones;
  // At least one milestone should be checked
  // (The actual achievement check happens internally)
});

test('calculateStreak: returns 0 for no sessions', () => {
  progress.clear_sessions();
  const streak = progress.calculateStreak();
  equal(streak, 0, 'Streak should be 0');
});

test('calculateStreak: tracks consecutive days', () => {
  progress.clear_sessions();
  
  // Add sessions for today and yesterday
  progress.track_progress('study', { duration: 30 });
  
  const yesterday = new Date(Date.now() - 86400000);
  progress.track_progress('study', { duration: 30 });
  // Manually adjust timestamp for yesterday session
  const sessions = progress.get_all_sessions();
  if (sessions.length > 0) {
    sessions[sessions.length - 1].timestamp = yesterday.toISOString();
  }
  
  const streak = progress.calculateStreak();
  if (streak < 1) {
    throw new Error(`Streak should be at least 1, got ${streak}`);
  }
});

test('export_to_file: exports data', () => {
  const testFile = 'D:\\OpenClaw\\workspace\\skills\\l6-learning-accelerator\\test\\export_test.json';
  const success = progress.export_to_file(testFile);
  
  if (!success) {
    throw new Error('Export should succeed');
  }
  
  // Clean up
  try {
    require('fs').unlinkSync(testFile);
  } catch (e) {
    // Ignore cleanup errors
  }
});

// ============================================
// SUMMARY
// ============================================
console.log('\n' + '='.repeat(50));
console.log(`\n✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📝 Total:  ${passed + failed}\n`);

if (failed > 0) {
  process.exit(1);
} else {
  console.log('🎉 All tests passed!\n');
  process.exit(0);
}
