/**
 * System Health Monitor Skill
 * Monitors system health for evolution system stability
 */

const os = require('os');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Health thresholds
const THRESHOLDS = {
  diskWarning: 80,    // % disk usage warning
  diskCritical: 95,   // % disk usage critical
  memoryWarning: 80,  // % memory usage warning
  memoryCritical: 95  // % memory usage critical
};

/**
 * Check system health
 * @returns {Promise<{status: string, checks: object, issues: Array}>}
 */
async function check() {
  const result = {
    status: 'healthy',
    checks: {},
    issues: [],
    timestamp: new Date().toISOString()
  };

  // Disk space check
  try {
    const diskUsage = checkDiskSpace();
    result.checks.disk = diskUsage;
    if (diskUsage.usedPercent >= THRESHOLDS.diskCritical) {
      result.status = 'critical';
      result.issues.push({
        type: 'disk',
        level: 'critical',
        message: `Disk usage at ${diskUsage.usedPercent}% - critical level`
      });
    } else if (diskUsage.usedPercent >= THRESHOLDS.diskWarning) {
      if (result.status === 'healthy') result.status = 'warning';
      result.issues.push({
        type: 'disk',
        level: 'warning',
        message: `Disk usage at ${diskUsage.usedPercent}% - approaching limit`
      });
    }
  } catch (e) {
    result.checks.disk = { error: e.message };
  }

  // Memory check
  try {
    const memoryUsage = checkMemory();
    result.checks.memory = memoryUsage;
    if (memoryUsage.usedPercent >= THRESHOLDS.memoryCritical) {
      result.status = 'critical';
      result.issues.push({
        type: 'memory',
        level: 'critical',
        message: `Memory usage at ${memoryUsage.usedPercent}% - critical level`
      });
    } else if (memoryUsage.usedPercent >= THRESHOLDS.memoryWarning) {
      if (result.status === 'healthy') result.status = 'warning';
      result.issues.push({
        type: 'memory',
        level: 'warning',
        message: `Memory usage at ${memoryUsage.usedPercent}% - high`
      });
    }
  } catch (e) {
    result.checks.memory = { error: e.message };
  }

  // Evolution status check
  try {
    const evolutionStatus = checkEvolutionStatus();
    result.checks.evolution = evolutionStatus;
    if (evolutionStatus.stale) {
      if (result.status === 'healthy') result.status = 'warning';
      result.issues.push({
        type: 'evolution',
        level: 'warning',
        message: `Evolution may be stale (last cycle: ${evolutionStatus.lastCycle})`
      });
    }
  } catch (e) {
    result.checks.evolution = { error: e.message };
  }

  // Process check
  try {
    const processInfo = checkProcesses();
    result.checks.processes = processInfo;
  } catch (e) {
    result.checks.processes = { error: e.message };
  }

  // Skills count check
  try {
    const skillsInfo = checkSkillsCount();
    result.checks.skills = skillsInfo;
  } catch (e) {
    result.checks.skills = { error: e.message };
  }

  return result;
}

/**
 * Check disk space
 */
function checkDiskSpace() {
  try {
    const output = execSync('df -h / | tail -1', { encoding: 'utf-8' });
    const parts = output.trim().split(/\s+/);
    const used = parseInt(parts[4]);
    const available = parts[3];
    const total = parts[1];
    
    return {
      total,
      used: parts[2],
      available,
      usedPercent: used
    };
  } catch (e) {
    // Fallback for systems without df
    return {
      usedPercent: 0,
      error: 'Unable to check disk space'
    };
  }
}

/**
 * Check memory usage
 */
function checkMemory() {
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const usedPercent = Math.round((usedMem / totalMem) * 100);
  
  return {
    total: formatBytes(totalMem),
    used: formatBytes(usedMem),
    free: formatBytes(freeMem),
    usedPercent
  };
}

/**
 * Check evolution status
 */
function checkEvolutionStatus() {
  const logsPath = path.join(process.cwd(), 'logs');
  const cycleCountFile = path.join(logsPath, 'cycle_count.txt');
  
  let lastCycle = 0;
  let stale = false;
  
  if (fs.existsSync(cycleCountFile)) {
    lastCycle = parseInt(fs.readFileSync(cycleCountFile, 'utf-8').trim()) || 0;
  }
  
  // Check if any recent status files exist
  const statusFiles = fs.readdirSync(logsPath)
    .filter(f => f.startsWith('status_') && f.endsWith('.json'))
    .slice(-5);
  
  if (statusFiles.length > 0) {
    const latestStatus = statusFiles[statusFiles.length - 1];
    const statusPath = path.join(logsPath, latestStatus);
    try {
      const stat = fs.statSync(statusPath);
      const ageMs = Date.now() - stat.mtimeMs;
      stale = ageMs > 30 * 60 * 1000; // 30 minutes
    } catch (e) {
      // Ignore
    }
  }
  
  return {
    lastCycle,
    stale,
    recentStatusFiles: statusFiles.length
  };
}

/**
 * Check running processes
 */
function checkProcesses() {
  const uptime = os.uptime();
  const loadAvg = os.loadavg();
  const cpus = os.cpus().length;
  
  return {
    uptime: formatUptime(uptime),
    loadAverage: loadAvg.map(l => l.toFixed(2)),
    cpuCount: cpus,
    platform: os.platform(),
    nodeVersion: process.version
  };
}

/**
 * Check skills count
 */
function checkSkillsCount() {
  const skillsPath = path.join(process.cwd(), 'skills');
  if (!fs.existsSync(skillsPath)) {
    return { count: 0 };
  }
  
  const count = fs.readdirSync(skillsPath, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory() && !dirent.name.startsWith('.'))
    .length;
  
  return { count };
}

/**
 * Format bytes to human readable
 */
function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let unitIndex = 0;
  let value = bytes;
  
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex++;
  }
  
  return `${value.toFixed(1)} ${units[unitIndex]}`;
}

/**
 * Format uptime
 */
function formatUptime(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  
  if (days > 0) {
    return `${days}d ${hours}h ${mins}m`;
  } else if (hours > 0) {
    return `${hours}h ${mins}m`;
  } else {
    return `${mins}m`;
  }
}

/**
 * Generate health report
 */
function formatReport(healthResult) {
  const { status, checks, issues } = healthResult;
  
  const statusIcon = status === 'healthy' ? '✅' : status === 'warning' ? '⚠️' : '🚨';
  
  let report = `${statusIcon} System Health: ${status.toUpperCase()}\n\n`;
  
  // Disk
  if (checks.disk && !checks.disk.error) {
    report += `💾 Disk: ${checks.disk.usedPercent}% used (${checks.disk.available} available)\n`;
  }
  
  // Memory
  if (checks.memory && !checks.memory.error) {
    report += `🧠 Memory: ${checks.memory.usedPercent}% used (${checks.memory.free} free)\n`;
  }
  
  // Processes
  if (checks.processes && !checks.processes.error) {
    report += `⚙️ System: ${checks.processes.cpuCount} CPUs, uptime ${checks.processes.uptime}\n`;
    report += `   Load: ${checks.processes.loadAverage.join(', ')}\n`;
  }
  
  // Evolution
  if (checks.evolution && !checks.evolution.error) {
    report += `🔄 Evolution: Cycle ${checks.evolution.lastCycle}`;
    if (checks.evolution.stale) {
      report += ' (may be stale)';
    }
    report += '\n';
  }
  
  // Skills
  if (checks.skills && !checks.skills.error) {
    report += `📦 Skills: ${checks.skills.count} installed\n`;
  }
  
  // Issues
  if (issues.length > 0) {
    report += `\n⚠️ Issues (${issues.length}):\n`;
    issues.forEach(issue => {
      const icon = issue.level === 'critical' ? '🚨' : '⚠️';
      report += `   ${icon} ${issue.message}\n`;
    });
  }
  
  return report;
}

/**
 * Main entry point
 */
async function main() {
  const result = await check();
  console.log(formatReport(result));
  return result;
}

module.exports = {
  check,
  formatReport,
  main
};
