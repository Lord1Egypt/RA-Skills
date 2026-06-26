/**
 * Progress Tracking Module
 * Tracks learning sessions and generates progress reports
 */

const fs = require('fs');
const path = require('path');

// In-memory store (in production, use persistent storage)
let sessions = [];
let milestones = [];

/**
 * Track a learning session
 * @param {string} type - Session type (study, practice, review, etc.)
 * @param {object} data - Session data
 * @returns {object} Created session
 */
function track_progress(type, data = {}) {
  const session = {
    id: generateId(),
    type,
    timestamp: new Date().toISOString(),
    date: new Date(),
    ...data
  };
  
  sessions.push(session);
  return session;
}

/**
 * Get progress report
 * @param {string} period - Report period (daily, weekly, monthly, all)
 * @param {object} options - Report options
 * @returns {object} Progress report
 */
function get_report(period = 'weekly', options = {}) {
  const now = new Date();
  let startDate = new Date(now);
  
  // Calculate date range based on period
  switch (period) {
    case 'daily':
      startDate.setDate(startDate.getDate() - 1);
      break;
    case 'weekly':
      startDate.setDate(startDate.getDate() - 7);
      break;
    case 'monthly':
      startDate.setMonth(startDate.getMonth() - 1);
      break;
    case 'all':
      startDate = new Date(0);
      break;
    default:
      startDate.setDate(startDate.getDate() - 7);
  }
  
  // Filter sessions in range
  const filteredSessions = sessions.filter(s => new Date(s.timestamp) >= startDate);
  
  // Calculate statistics
  const stats = calculateStats(filteredSessions);
  
  // Group by type
  const byType = groupByType(filteredSessions);
  
  // Group by date
  const byDate = groupByDate(filteredSessions);
  
  // Get milestones achieved
  const achievedMilestones = milestones.filter(m => new Date(m.achievedAt) >= startDate);
  
  return {
    period,
    generatedAt: now.toISOString(),
    dateRange: {
      start: startDate.toISOString(),
      end: now.toISOString()
    },
    summary: {
      totalSessions: filteredSessions.length,
      totalTimeMinutes: stats.totalTime,
      avgSessionTime: stats.avgTime,
      typesCompleted: Object.keys(byType).length
    },
    byType,
    byDate,
    milestones: achievedMilestones,
    trends: calculateTrends(filteredSessions)
  };
}

/**
 * Set a milestone
 * @param {string} name - Milestone name
 * @param {object} criteria - Achievement criteria
 * @returns {object} Milestone
 */
function set_milestone(name, criteria = {}) {
  const milestone = {
    id: generateId(),
    name,
    criteria,
    createdAt: new Date().toISOString(),
    achieved: false,
    achievedAt: null
  };
  
  milestones.push(milestone);
  checkMilestone(milestone);
  return milestone;
}

/**
 * Check if a milestone is achieved
 * @param {object} milestone - Milestone to check
 * @returns {boolean} Whether milestone is achieved
 */
function checkMilestone(milestone) {
  if (milestone.achieved) return true;
  
  const { criteria } = milestone;
  let achieved = false;
  
  if (criteria.totalSessions) {
    const count = sessions.filter(s => {
      if (criteria.type && s.type !== criteria.type) return false;
      return true;
    }).length;
    
    if (count >= criteria.totalSessions) {
      achieved = true;
    }
  }
  
  if (criteria.totalMinutes) {
    const total = sessions.reduce((sum, s) => sum + (s.duration || 0), 0);
    if (total >= criteria.totalMinutes) {
      achieved = true;
    }
  }
  
  if (criteria.streak) {
    const streak = calculateStreak();
    if (streak >= criteria.streak) {
      achieved = true;
    }
  }
  
  if (achieved && !milestone.achieved) {
    milestone.achieved = true;
    milestone.achievedAt = new Date().toISOString();
  }
  
  return achieved;
}

/**
 * Calculate statistics from sessions
 * @param {object[]} sessions - Sessions to analyze
 * @returns {object} Statistics
 */
function calculateStats(sessionList) {
  if (!sessionList || sessionList.length === 0) {
    return { totalTime: 0, avgTime: 0, sessions: 0 };
  }
  
  const totalTime = sessionList.reduce((sum, s) => sum + (s.duration || 0), 0);
  const avgTime = totalTime / sessionList.length;
  
  return {
    totalTime: Math.round(totalTime),
    avgTime: Math.round(avgTime),
    sessions: sessionList.length
  };
}

/**
 * Group sessions by type
 * @param {object[]} sessionList - Sessions to group
 * @returns {object} Grouped sessions
 */
function groupByType(sessionList) {
  return sessionList.reduce((acc, session) => {
    const type = session.type || 'unknown';
    if (!acc[type]) {
      acc[type] = {
        count: 0,
        totalTime: 0,
        sessions: []
      };
    }
    acc[type].count++;
    acc[type].totalTime += (session.duration || 0);
    acc[type].sessions.push(session);
    return acc;
  }, {});
}

/**
 * Group sessions by date
 * @param {object[]} sessionList - Sessions to group
 * @returns {object} Grouped sessions
 */
function groupByDate(sessionList) {
  return sessionList.reduce((acc, session) => {
    const date = new Date(session.timestamp).toISOString().split('T')[0];
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(session);
    return acc;
  }, {});
}

/**
 * Calculate trends
 * @param {object[]} sessionList - Sessions to analyze
 * @returns {object} Trend data
 */
function calculateTrends(sessionList) {
  if (sessionList.length < 2) {
    return { direction: 'stable', change: 0 };
  }
  
  // Split into first half and second half
  const mid = Math.floor(sessionList.length / 2);
  const firstHalf = sessionList.slice(0, mid);
  const secondHalf = sessionList.slice(mid);
  
  const firstAvg = firstHalf.reduce((sum, s) => sum + (s.duration || 0), 0) / firstHalf.length;
  const secondAvg = secondHalf.reduce((sum, s) => sum + (s.duration || 0), 0) / secondHalf.length;
  
  const change = secondAvg - firstAvg;
  const percentChange = firstAvg > 0 ? (change / firstAvg) * 100 : 0;
  
  let direction = 'stable';
  if (percentChange > 10) direction = 'increasing';
  if (percentChange < -10) direction = 'decreasing';
  
  return {
    direction,
    change: Math.round(change),
    percentChange: Math.round(percentChange * 10) / 10
  };
}

/**
 * Calculate current streak
 * @returns {number} Streak in days
 */
function calculateStreak() {
  if (sessions.length === 0) return 0;
  
  const now = new Date();
  const today = now.toISOString().split('T')[0];
  let streak = 0;
  let currentDate = new Date(now);
  
  // Get unique dates with sessions
  const datesWithSessions = new Set(
    sessions.map(s => new Date(s.timestamp).toISOString().split('T')[0])
  );
  
  // Count backwards from today
  while (true) {
    const dateStr = currentDate.toISOString().split('T')[0];
    if (datesWithSessions.has(dateStr)) {
      streak++;
      currentDate.setDate(currentDate.getDate() - 1);
    } else if (dateStr === today) {
      // Today doesn't count if no session yet
      currentDate.setDate(currentDate.getDate() - 1);
    } else {
      break;
    }
  }
  
  return streak;
}

/**
 * Generate unique ID
 * @returns {string} Unique ID
 */
function generateId() {
  return `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Clear all sessions (for testing)
 */
function clear_sessions() {
  sessions = [];
  milestones = [];
}

/**
 * Get all sessions
 * @returns {object[]} All sessions
 */
function get_all_sessions() {
  return [...sessions];
}

/**
 * Export sessions to JSON
 * @param {string} filePath - File path to export to
 * @returns {boolean} Success
 */
function export_to_file(filePath) {
  try {
    const data = {
      sessions,
      milestones,
      exportedAt: new Date().toISOString()
    };
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    return true;
  } catch (error) {
    console.error('Export failed:', error);
    return false;
  }
}

/**
 * Import sessions from JSON file
 * @param {string} filePath - File path to import from
 * @returns {boolean} Success
 */
function import_from_file(filePath) {
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (data.sessions) sessions = data.sessions;
    if (data.milestones) milestones = data.milestones;
    return true;
  } catch (error) {
    console.error('Import failed:', error);
    return false;
  }
}

module.exports = {
  track_progress,
  get_report,
  set_milestone,
  checkMilestone,
  calculateStreak,
  clear_sessions,
  get_all_sessions,
  export_to_file,
  import_from_file
};
