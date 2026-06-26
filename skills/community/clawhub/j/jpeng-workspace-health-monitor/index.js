/**
 * Workspace Health Monitor
 * Performs comprehensive workspace health checks and generates recommendations
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Get directory size recursively
 * @param {string} dir - Directory path
 * @param {Set<string>} excludeDirs - Directories to exclude
 * @returns {Object} Size info
 */
function getDirectorySize(dir, excludeDirs = new Set(['.git', 'node_modules'])) {
  let totalSize = 0;
  let fileCount = 0;
  let dirCount = 0;
  
  function walk(currentDir) {
    try {
      const entries = fs.readdirSync(currentDir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        
        if (entry.isDirectory()) {
          if (!excludeDirs.has(entry.name)) {
            dirCount++;
            walk(fullPath);
          }
        } else if (entry.isFile()) {
          try {
            const stats = fs.statSync(fullPath);
            totalSize += stats.size;
            fileCount++;
          } catch (e) {
            // Skip inaccessible files
          }
        }
      }
    } catch (e) {
      // Skip inaccessible directories
    }
  }
  
  walk(dir);
  
  return { totalSize, fileCount, dirCount };
}

/**
 * Format bytes to human readable
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size
 */
function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let unitIndex = 0;
  let size = bytes;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

/**
 * Check skill health
 * @param {string} skillsDir - Path to skills directory
 * @returns {Object} Skill health report
 */
function checkSkillHealth(skillsDir) {
  const report = {
    total: 0,
    healthy: 0,
    broken: 0,
    missingIndex: [],
    missingSkillMd: [],
    missingPackage: []
  };
  
  if (!fs.existsSync(skillsDir)) {
    return report;
  }
  
  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    
    report.total++;
    const skillPath = path.join(skillsDir, entry.name);
    let isHealthy = true;
    
    if (!fs.existsSync(path.join(skillPath, 'index.js'))) {
      report.missingIndex.push(entry.name);
      isHealthy = false;
    }
    
    if (!fs.existsSync(path.join(skillPath, 'SKILL.md'))) {
      report.missingSkillMd.push(entry.name);
      isHealthy = false;
    }
    
    if (!fs.existsSync(path.join(skillPath, 'package.json'))) {
      report.missingPackage.push(entry.name);
      // Not critical for health
    }
    
    if (isHealthy) {
      report.healthy++;
    } else {
      report.broken++;
    }
  }
  
  return report;
}

/**
 * Check for large files
 * @param {string} workspacePath - Workspace root
 * @param {number} thresholdMB - Size threshold in MB
 * @returns {Array<Object>} Large files
 */
function findLargeFiles(workspacePath, thresholdMB = 10) {
  const largeFiles = [];
  const threshold = thresholdMB * 1024 * 1024;
  const excludeDirs = new Set(['.git', 'node_modules']);
  
  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          if (!excludeDirs.has(entry.name)) {
            walk(fullPath);
          }
        } else if (entry.isFile()) {
          try {
            const stats = fs.statSync(fullPath);
            if (stats.size >= threshold) {
              largeFiles.push({
                path: path.relative(workspacePath, fullPath),
                size: stats.size,
                sizeFormatted: formatBytes(stats.size)
              });
            }
          } catch (e) {
            // Skip
          }
        }
      }
    } catch (e) {
      // Skip
    }
  }
  
  walk(workspacePath);
  
  return largeFiles.sort((a, b) => b.size - a.size);
}

/**
 * Check for empty directories
 * @param {string} workspacePath - Workspace root
 * @returns {Array<string>} Empty directories
 */
function findEmptyDirectories(workspacePath) {
  const emptyDirs = [];
  const excludeDirs = new Set(['.git', 'node_modules']);
  
  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      if (entries.length === 0) {
        emptyDirs.push(path.relative(workspacePath, dir));
        return;
      }
      
      for (const entry of entries) {
        if (entry.isDirectory() && !excludeDirs.has(entry.name)) {
          walk(path.join(dir, entry.name));
        }
      }
    } catch (e) {
      // Skip
    }
  }
  
  walk(workspacePath);
  
  return emptyDirs;
}

/**
 * Get file type distribution
 * @param {string} workspacePath - Workspace root
 * @returns {Object} File type counts
 */
function getFileTypeDistribution(workspacePath) {
  const distribution = {};
  const excludeDirs = new Set(['.git', 'node_modules']);
  
  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        if (entry.isDirectory()) {
          if (!excludeDirs.has(entry.name)) {
            walk(path.join(dir, entry.name));
          }
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name).toLowerCase() || 'no-extension';
          distribution[ext] = (distribution[ext] || 0) + 1;
        }
      }
    } catch (e) {
      // Skip
    }
  }
  
  walk(workspacePath);
  
  // Sort by count
  const sorted = Object.entries(distribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20);
  
  return Object.fromEntries(sorted);
}

/**
 * Calculate health score
 * @param {Object} metrics - Collected metrics
 * @returns {number} Health score (0-100)
 */
function calculateHealthScore(metrics) {
  let score = 100;
  
  // Deduct for broken skills
  if (metrics.skills.total > 0) {
    const brokenRatio = metrics.skills.broken / metrics.skills.total;
    score -= brokenRatio * 30;
  }
  
  // Deduct for large files
  if (metrics.largeFiles.length > 10) {
    score -= 10;
  } else if (metrics.largeFiles.length > 5) {
    score -= 5;
  }
  
  // Deduct for empty directories
  if (metrics.emptyDirs.length > 20) {
    score -= 10;
  } else if (metrics.emptyDirs.length > 10) {
    score -= 5;
  }
  
  // Deduct for very large workspace
  if (metrics.diskUsage.totalSizeMB > 1000) {
    score -= 10;
  }
  
  return Math.max(0, Math.min(100, Math.round(score)));
}

/**
 * Generate recommendations
 * @param {Object} metrics - Collected metrics
 * @returns {Array<Object>} Recommendations
 */
function generateRecommendations(metrics) {
  const recommendations = [];
  
  // Skill recommendations
  if (metrics.skills.broken > 0) {
    recommendations.push({
      severity: 'high',
      category: 'skills',
      message: `${metrics.skills.broken} broken skill(s) found`,
      details: metrics.skills.missingIndex.length > 0 
        ? `Missing index.js: ${metrics.skills.missingIndex.slice(0, 5).join(', ')}`
        : undefined,
      action: 'Fix or remove broken skills'
    });
  }
  
  // Large files recommendations
  if (metrics.largeFiles.length > 0) {
    recommendations.push({
      severity: 'medium',
      category: 'storage',
      message: `${metrics.largeFiles.length} large file(s) found (>10MB)`,
      details: metrics.largeFiles.slice(0, 3).map(f => `${f.path} (${f.sizeFormatted})`).join(', '),
      action: 'Consider archiving or removing large files'
    });
  }
  
  // Empty directories
  if (metrics.emptyDirs.length > 0) {
    recommendations.push({
      severity: 'low',
      category: 'cleanup',
      message: `${metrics.emptyDirs.length} empty director(y/ies) found`,
      action: 'Remove empty directories to clean up workspace'
    });
  }
  
  // Disk usage
  if (metrics.diskUsage.totalSizeMB > 500) {
    recommendations.push({
      severity: 'info',
      category: 'storage',
      message: `Workspace size: ${formatBytes(metrics.diskUsage.totalSize)}`,
      action: 'Monitor disk usage growth'
    });
  }
  
  return recommendations;
}

/**
 * Perform comprehensive health check
 * @param {string} workspacePath - Workspace root path
 * @param {Object} options - Check options
 * @returns {Object} Health report
 */
function check(workspacePath, options = {}) {
  const {
    largeFileThresholdMB = 10,
    includeEmptyDirs = true,
    includeLargeFiles = true
  } = options;
  
  const metrics = {
    timestamp: new Date().toISOString(),
    workspace: workspacePath,
    diskUsage: {},
    files: {},
    skills: {},
    largeFiles: [],
    emptyDirs: [],
    fileTypes: {}
  };
  
  // Disk usage
  const sizeInfo = getDirectorySize(workspacePath);
  metrics.diskUsage = {
    totalSize: sizeInfo.totalSize,
    totalSizeMB: sizeInfo.totalSize / (1024 * 1024),
    totalSizeFormatted: formatBytes(sizeInfo.totalSize)
  };
  
  // File counts
  metrics.files = {
    total: sizeInfo.fileCount,
    directories: sizeInfo.dirCount
  };
  
  // Skill health
  const skillsDir = path.join(workspacePath, 'skills');
  metrics.skills = checkSkillHealth(skillsDir);
  
  // Large files
  if (includeLargeFiles) {
    metrics.largeFiles = findLargeFiles(workspacePath, largeFileThresholdMB);
  }
  
  // Empty directories
  if (includeEmptyDirs) {
    metrics.emptyDirs = findEmptyDirectories(workspacePath);
  }
  
  // File type distribution
  metrics.fileTypes = getFileTypeDistribution(workspacePath);
  
  // Calculate health score
  const healthScore = calculateHealthScore(metrics);
  
  // Generate recommendations
  const recommendations = generateRecommendations(metrics);
  
  return {
    healthScore,
    status: healthScore >= 80 ? 'healthy' : healthScore >= 60 ? 'warning' : 'critical',
    metrics,
    recommendations
  };
}

/**
 * Generate health report
 * @param {Object} report - Health check report
 * @returns {string} Markdown report
 */
function generateReport(report) {
  const lines = [];
  const { healthScore, status, metrics, recommendations } = report;
  
  const statusEmoji = status === 'healthy' ? '✅' : status === 'warning' ? '⚠️' : '❌';
  
  lines.push('# Workspace Health Report');
  lines.push('');
  lines.push(`**Status:** ${statusEmoji} ${status.toUpperCase()} (Score: ${healthScore}/100)`);
  lines.push(`**Timestamp:** ${metrics.timestamp}`);
  lines.push('');
  
  lines.push('## Disk Usage');
  lines.push('');
  lines.push(`- **Total Size:** ${metrics.diskUsage.totalSizeFormatted}`);
  lines.push(`- **Files:** ${metrics.files.total.toLocaleString()}`);
  lines.push(`- **Directories:** ${metrics.files.directories.toLocaleString()}`);
  lines.push('');
  
  lines.push('## Skills Health');
  lines.push('');
  lines.push(`- **Total Skills:** ${metrics.skills.total}`);
  lines.push(`- **Healthy:** ${metrics.skills.healthy}`);
  lines.push(`- **Broken:** ${metrics.skills.broken}`);
  
  if (metrics.skills.missingIndex.length > 0) {
    lines.push(`- **Missing index.js:** ${metrics.skills.missingIndex.slice(0, 5).join(', ')}${metrics.skills.missingIndex.length > 5 ? '...' : ''}`);
  }
  lines.push('');
  
  if (metrics.largeFiles.length > 0) {
    lines.push('## Large Files (>10MB)');
    lines.push('');
    for (const file of metrics.largeFiles.slice(0, 10)) {
      lines.push(`- \`${file.path}\` (${file.sizeFormatted})`);
    }
    lines.push('');
  }
  
  if (metrics.emptyDirs.length > 0) {
    lines.push(`## Empty Directories (${metrics.emptyDirs.length})`);
    lines.push('');
    for (const dir of metrics.emptyDirs.slice(0, 10)) {
      lines.push(`- \`${dir}\``);
    }
    lines.push('');
  }
  
  if (recommendations.length > 0) {
    lines.push('## Recommendations');
    lines.push('');
    for (const rec of recommendations) {
      const severityIcon = rec.severity === 'high' ? '🔴' : rec.severity === 'medium' ? '🟡' : '🔵';
      lines.push(`${severityIcon} **${rec.category}**: ${rec.message}`);
      if (rec.details) {
        lines.push(`  - ${rec.details}`);
      }
      if (rec.action) {
        lines.push(`  - Action: ${rec.action}`);
      }
    }
  }
  
  return lines.join('\n');
}

/**
 * Main entry point
 */
async function main() {
  const workspacePath = process.cwd();
  console.log(`Checking workspace health: ${workspacePath}`);
  
  const report = check(workspacePath);
  console.log(generateReport(report));
  
  return report;
}

module.exports = {
  check,
  checkSkillHealth,
  findLargeFiles,
  findEmptyDirectories,
  getFileTypeDistribution,
  getDirectorySize,
  calculateHealthScore,
  generateRecommendations,
  generateReport,
  formatBytes,
  main
};
