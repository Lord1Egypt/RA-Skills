/**
 * Cycle History Viewer
 * 
 * Views and searches evolution cycle history with filtering capabilities.
 * Helps track progress and analyze patterns.
 */

const fs = require('fs');
const path = require('path');

const HISTORY_DIR = 'logs';

/**
 * List all cycle status files
 * @param {string} workspacePath - Path to workspace root
 * @returns {array} List of status files with metadata
 */
function listFiles(workspacePath) {
  const logsDir = path.join(workspacePath, HISTORY_DIR);
  
  if (!fs.existsSync(logsDir)) {
    return [];
  }
  
  const files = fs.readdirSync(logsDir)
    .filter(f => f.startsWith('status_') && f.endsWith('.json'))
    .sort()
    .reverse();
  
  return files.map(f => {
    const match = f.match(/status_(\d+)\.json/);
    const cycle = match ? parseInt(match[1], 10) : 0;
    
    const filepath = path.join(logsDir, f);
    let data = null;
    try {
      data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    } catch (e) {
      // Ignore parse errors
    }
    
    return {
      filename: f,
      cycle,
      path: filepath,
      data
    };
  });
}

/**
 * Get a specific cycle's status
 * @param {string} workspacePath - Path to workspace root
 * @param {number} cycle - Cycle number
 * @returns {object|null} Cycle status data
 */
function get(workspacePath, cycle) {
  const filepath = path.join(workspacePath, HISTORY_DIR, `status_${String(cycle).padStart(4, '0')}.json`);
  
  if (!fs.existsSync(filepath)) {
    return null;
  }
  
  return JSON.parse(fs.readFileSync(filepath, 'utf8'));
}

/**
 * Search cycle history with filters
 * @param {string} workspacePath - Path to workspace root
 * @param {object} filters - Filter options
 * @returns {array} Matching cycles
 */
function search(workspacePath, filters = {}) {
  const { intent, result, keyword, limit = 50 } = filters;
  
  const files = listFiles(workspacePath);
  const results = [];
  
  for (const file of files) {
    if (results.length >= limit) break;
    
    if (!file.data) continue;
    
    // Filter by intent
    if (intent) {
      const intentLower = intent.toLowerCase();
      if (!file.data.en || !file.data.en.toLowerCase().includes(intentLower)) {
        continue;
      }
    }
    
    // Filter by result
    if (result && file.data.result !== result) {
      continue;
    }
    
    // Filter by keyword
    if (keyword) {
      const keywordLower = keyword.toLowerCase();
      const matchesEn = file.data.en && file.data.en.toLowerCase().includes(keywordLower);
      const matchesZh = file.data.zh && file.data.zh.toLowerCase().includes(keywordLower);
      if (!matchesEn && !matchesZh) {
        continue;
      }
    }
    
    results.push({
      cycle: file.cycle,
      result: file.data.result,
      en: file.data.en,
      zh: file.data.zh
    });
  }
  
  return results;
}

/**
 * Get summary statistics
 * @param {string} workspacePath - Path to workspace root
 * @param {number} count - Number of recent cycles to analyze
 * @returns {object} Summary statistics
 */
function summary(workspacePath, count = 100) {
  const files = listFiles(workspacePath).slice(0, count);
  
  const stats = {
    total: files.length,
    success: 0,
    failed: 0,
    byIntent: {
      innovation: 0,
      repair: 0,
      optimize: 0
    },
    recentCycles: []
  };
  
  files.forEach(f => {
    if (!f.data) return;
    
    if (f.data.result === 'success') stats.success++;
    if (f.data.result === 'failed') stats.failed++;
    
    // Detect intent from status text
    const text = (f.data.en || '').toLowerCase();
    if (text.includes('innovation') || text.includes('创新')) {
      stats.byIntent.innovation++;
    } else if (text.includes('repair') || text.includes('修复')) {
      stats.byIntent.repair++;
    } else if (text.includes('optimize') || text.includes('优化')) {
      stats.byIntent.optimize++;
    }
    
    stats.recentCycles.push({
      cycle: f.cycle,
      result: f.data.result,
      intent: detectIntent(f.data.en)
    });
  });
  
  stats.successRate = stats.total > 0 ? stats.success / stats.total : 0;
  
  return stats;
}

/**
 * Detect intent from status text
 */
function detectIntent(text) {
  if (!text) return 'unknown';
  const lower = text.toLowerCase();
  if (lower.includes('innovation') || lower.includes('创新')) return 'innovation';
  if (lower.includes('repair') || lower.includes('修复')) return 'repair';
  if (lower.includes('optimize') || lower.includes('优化')) return 'optimize';
  return 'unknown';
}

/**
 * Generate history report
 * @param {string} workspacePath - Path to workspace root
 * @param {number} count - Number of cycles to include
 * @returns {string} Markdown report
 */
function generateReport(workspacePath, count = 20) {
  const files = listFiles(workspacePath).slice(0, count);
  const stats = summary(workspacePath, count);
  
  const lines = [];
  lines.push('# 📜 Evolution Cycle History');
  lines.push('');
  
  // Summary
  lines.push('## Summary');
  lines.push('');
  lines.push(`| Metric | Value |`);
  lines.push(`|--------|-------|`);
  lines.push(`| Cycles Shown | ${stats.total} |`);
  lines.push(`| Success Rate | ${(stats.successRate * 100).toFixed(1)}% |`);
  lines.push(`| Innovation | ${stats.byIntent.innovation} |`);
  lines.push(`| Repair | ${stats.byIntent.repair} |`);
  lines.push(`| Optimize | ${stats.byIntent.optimize} |`);
  lines.push('');
  
  // Recent cycles
  lines.push(`## Last ${count} Cycles`);
  lines.push('');
  lines.push('| Cycle | Result | Intent | Description |');
  lines.push('|-------|--------|--------|-------------|');
  
  files.forEach(f => {
    if (!f.data) return;
    const intent = detectIntent(f.data.en);
    const emoji = f.data.result === 'success' ? '✅' : '❌';
    const desc = (f.data.en || '').replace(/Status:\s*\[[\w]+\]\s*/, '').substring(0, 50);
    lines.push(`| ${f.cycle} | ${emoji} | ${intent} | ${desc} |`);
  });
  
  lines.push('');
  
  return lines.join('\n');
}

/**
 * Export history to JSON
 * @param {string} workspacePath - Path to workspace root
 * @param {number} count - Number of cycles to export
 * @returns {object} Exported data
 */
function exportJson(workspacePath, count = 100) {
  const files = listFiles(workspacePath).slice(0, count);
  
  return {
    exported: new Date().toISOString(),
    count: files.length,
    cycles: files.filter(f => f.data).map(f => ({
      cycle: f.cycle,
      ...f.data
    }))
  };
}

module.exports = {
  listFiles,
  get,
  search,
  summary,
  generateReport,
  exportJson,
  main: () => {
    const workspacePath = process.cwd();
    console.log(generateReport(workspacePath, 20));
    return summary(workspacePath);
  }
};
