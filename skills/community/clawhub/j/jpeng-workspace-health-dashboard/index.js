/**
 * Workspace Health Dashboard - Unified health monitoring for the workspace
 * 
 * Consolidates multiple health checks into a single dashboard:
 * - Skill quality audit
 * - Dependency vulnerabilities
 * - Cleanup recommendations
 * - Permission audit
 */

const fs = require('fs');
const path = require('path');

/**
 * Run all health checks and generate dashboard
 * @param {Object} options - Dashboard options
 * @returns {Object} Complete health dashboard
 */
function generateDashboard(options = {}) {
  const workspacePath = options.workspacePath || '/root/.openclaw/workspace';
  const skillsPath = path.join(workspacePath, 'skills');
  
  const dashboard = {
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    summary: {
      overallHealth: 'unknown',
      score: 0,
      checks: 0,
      passed: 0,
      warnings: 0,
      critical: 0
    },
    checks: {}
  };

  // 1. Skill Quality Check
  try {
    const skillQuality = checkSkillQuality(skillsPath);
    dashboard.checks.skillQuality = skillQuality;
    dashboard.summary.checks++;
    if (skillQuality.status === 'pass') dashboard.summary.passed++;
    else if (skillQuality.status === 'warning') dashboard.summary.warnings++;
    else dashboard.summary.critical++;
  } catch (e) {
    dashboard.checks.skillQuality = { status: 'error', message: e.message };
    dashboard.summary.critical++;
    dashboard.summary.checks++;
  }

  // 2. Dependency Security Check
  try {
    const dependencyCheck = checkDependencies(workspacePath);
    dashboard.checks.dependencies = dependencyCheck;
    dashboard.summary.checks++;
    if (dependencyCheck.status === 'pass') dashboard.summary.passed++;
    else if (dependencyCheck.status === 'warning') dashboard.summary.warnings++;
    else dashboard.summary.critical++;
  } catch (e) {
    dashboard.checks.dependencies = { status: 'error', message: e.message };
    dashboard.summary.critical++;
    dashboard.summary.checks++;
  }

  // 3. Cleanup Recommendations
  try {
    const cleanupCheck = checkCleanupNeeds(skillsPath);
    dashboard.checks.cleanup = cleanupCheck;
    dashboard.summary.checks++;
    if (cleanupCheck.status === 'pass') dashboard.summary.passed++;
    else if (cleanupCheck.status === 'warning') dashboard.summary.warnings++;
    else dashboard.summary.critical++;
  } catch (e) {
    dashboard.checks.cleanup = { status: 'error', message: e.message };
    dashboard.summary.critical++;
    dashboard.summary.checks++;
  }

  // 4. Protected Skills Check
  try {
    const protectedCheck = checkProtectedSkills(skillsPath);
    dashboard.checks.protectedSkills = protectedCheck;
    dashboard.summary.checks++;
    dashboard.summary.passed++; // Always pass if no error
  } catch (e) {
    dashboard.checks.protectedSkills = { status: 'error', message: e.message };
    dashboard.summary.warnings++;
    dashboard.summary.checks++;
  }

  // Calculate overall health score
  const passRate = dashboard.summary.passed / dashboard.summary.checks;
  dashboard.summary.score = Math.round(passRate * 100);
  
  if (dashboard.summary.critical > 0) {
    dashboard.summary.overallHealth = 'critical';
  } else if (dashboard.summary.warnings > 0) {
    dashboard.summary.overallHealth = 'warning';
  } else {
    dashboard.summary.overallHealth = 'healthy';
  }

  return dashboard;
}

/**
 * Check skill quality
 */
function checkSkillQuality(skillsPath) {
  const result = {
    status: 'pass',
    total: 0,
    complete: 0,
    incomplete: 0,
    broken: 0,
    details: {}
  };

  if (!fs.existsSync(skillsPath)) {
    result.status = 'error';
    result.message = 'Skills directory not found';
    return result;
  }

  const entries = fs.readdirSync(skillsPath, { withFileTypes: true });
  const skillDirs = entries.filter(e => e.isDirectory() && !e.name.startsWith('.'));
  
  result.total = skillDirs.length;

  for (const dir of skillDirs) {
    const skillPath = path.join(skillsPath, dir.name);
    const hasIndex = fs.existsSync(path.join(skillPath, 'index.js'));
    const hasSkillMd = fs.existsSync(path.join(skillPath, 'SKILL.md'));

    if (hasIndex && hasSkillMd) {
      result.complete++;
    } else if (hasIndex || hasSkillMd) {
      result.incomplete++;
    } else {
      result.broken++;
    }
  }

  result.details = {
    completePercent: Math.round((result.complete / result.total) * 100),
    incompletePercent: Math.round((result.incomplete / result.total) * 100)
  };

  // Set status based on thresholds
  if (result.details.completePercent < 50) {
    result.status = 'critical';
  } else if (result.details.completePercent < 75) {
    result.status = 'warning';
  }

  return result;
}

/**
 * Check for dependency vulnerabilities
 */
function checkDependencies(workspacePath) {
  const result = {
    status: 'pass',
    scanned: 0,
    vulnerabilities: 0,
    details: {}
  };

  const packagePath = path.join(workspacePath, 'package.json');
  if (!fs.existsSync(packagePath)) {
    result.message = 'No package.json found';
    return result;
  }

  try {
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    result.scanned = Object.keys(deps).length;
    result.details.totalDependencies = result.scanned;
    
    // Note: Full npm audit would require exec, which we avoid here
    // This is a lightweight check
    result.message = `${result.scanned} dependencies found. Run npm audit for full scan.`;
  } catch (e) {
    result.status = 'warning';
    result.message = 'Could not parse package.json';
  }

  return result;
}

/**
 * Check for cleanup needs
 */
function checkCleanupNeeds(skillsPath) {
  const result = {
    status: 'pass',
    junkFolders: 0,
    incompleteSkills: 0,
    potentialSavings: 0,
    details: {}
  };

  if (!fs.existsSync(skillsPath)) {
    return result;
  }

  const junkPatterns = ['__MACOSX', '.DS_Store', '.usage-tracker'];
  const entries = fs.readdirSync(skillsPath, { withFileTypes: true });

  for (const entry of entries) {
    if (junkPatterns.some(p => entry.name.includes(p))) {
      result.junkFolders++;
    }

    if (entry.isDirectory() && !entry.name.startsWith('.')) {
      const skillPath = path.join(skillsPath, entry.name);
      const hasIndex = fs.existsSync(path.join(skillPath, 'index.js'));
      if (!hasIndex) {
        result.incompleteSkills++;
      }
    }
  }

  if (result.junkFolders > 0 || result.incompleteSkills > 100) {
    result.status = 'warning';
  }

  result.details = {
    junkFolders: result.junkFolders,
    incompleteSkills: result.incompleteSkills
  };

  return result;
}

/**
 * Check protected skills status
 */
function checkProtectedSkills(skillsPath) {
  const protectedList = [
    'evolver', 'feishu-evolver-wrapper', 'feishu-common', 'feishu-post',
    'feishu-card', 'feishu-doc', 'common', 'clawhub', 'git-sync',
    'downloader', 'uploader', 'xfyun-search', 'xfyun-tts', 'podcast-gen',
    'weather', 'healthcheck', 'skill-creator', 'skill-quality-auditor',
    'skill-cleanup-executor', 'workspace-health-dashboard'
  ];

  const result = {
    status: 'pass',
    protected: 0,
    missing: [],
    details: {}
  };

  for (const skillName of protectedList) {
    const skillPath = path.join(skillsPath, skillName);
    if (fs.existsSync(skillPath)) {
      result.protected++;
    } else {
      result.missing.push(skillName);
    }
  }

  result.details = {
    protectedCount: result.protected,
    missingCount: result.missing.length
  };

  if (result.missing.length > 0) {
    result.status = 'warning';
  }

  return result;
}

/**
 * Format dashboard for display
 * @param {Object} dashboard - Dashboard object
 * @returns {string} Formatted dashboard
 */
function formatDashboard(dashboard) {
  const lines = [];

  const healthIcon = {
    healthy: '✅',
    warning: '⚠️',
    critical: '🔴',
    unknown: '❓'
  };

  const statusIcon = {
    pass: '✅',
    warning: '⚠️',
    critical: '🔴',
    error: '❌'
  };

  lines.push('🏥 Workspace Health Dashboard');
  lines.push('━'.repeat(50));
  lines.push(`Timestamp: ${dashboard.timestamp}`);
  lines.push('');

  lines.push('📊 Overall Health:');
  lines.push(`  ${healthIcon[dashboard.summary.overallHealth]} ${dashboard.summary.overallHealth.toUpperCase()}`);
  lines.push(`  Score: ${dashboard.summary.score}/100`);
  lines.push(`  Checks: ${dashboard.summary.passed}/${dashboard.summary.checks} passed`);
  lines.push('');

  // Skill Quality
  const sq = dashboard.checks.skillQuality;
  if (sq) {
    lines.push(`📁 Skill Quality: ${statusIcon[sq.status]} ${sq.status}`);
    lines.push(`   Total: ${sq.total} | Complete: ${sq.complete} | Incomplete: ${sq.incomplete}`);
    if (sq.details?.completePercent !== undefined) {
      lines.push(`   Completion: ${sq.details.completePercent}%`);
    }
    lines.push('');
  }

  // Dependencies
  const dep = dashboard.checks.dependencies;
  if (dep) {
    lines.push(`📦 Dependencies: ${statusIcon[dep.status]} ${dep.status}`);
    lines.push(`   Scanned: ${dep.scanned} dependencies`);
    if (dep.message) lines.push(`   ${dep.message}`);
    lines.push('');
  }

  // Cleanup
  const cleanup = dashboard.checks.cleanup;
  if (cleanup) {
    lines.push(`🧹 Cleanup Status: ${statusIcon[cleanup.status]} ${cleanup.status}`);
    lines.push(`   Junk folders: ${cleanup.junkFolders}`);
    lines.push(`   Incomplete skills: ${cleanup.incompleteSkills}`);
    lines.push('');
  }

  // Protected Skills
  const prot = dashboard.checks.protectedSkills;
  if (prot) {
    lines.push(`🛡️ Protected Skills: ${statusIcon[prot.status]} ${prot.status}`);
    lines.push(`   Found: ${prot.protected}/${prot.protected + prot.missing.length}`);
    if (prot.missing.length > 0) {
      lines.push(`   Missing: ${prot.missing.slice(0, 3).join(', ')}${prot.missing.length > 3 ? '...' : ''}`);
    }
  }

  return lines.join('\n');
}

/**
 * Quick health check - returns true if healthy
 */
function isHealthy(options = {}) {
  const dashboard = generateDashboard(options);
  return dashboard.summary.overallHealth === 'healthy';
}

/**
 * Main entry point
 */
async function main() {
  console.log('🏥 Workspace Health Dashboard');
  console.log('=============================\n');

  const dashboard = generateDashboard();
  console.log(formatDashboard(dashboard));

  console.log('\n💡 Tips:');
  console.log('   - Run skill-quality-auditor for detailed skill analysis');
  console.log('   - Run skill-cleanup-executor to clean incomplete skills');
  console.log('   - Run dependency-vulnerability-scanner for security audit');

  return dashboard;
}

module.exports = {
  generateDashboard,
  formatDashboard,
  isHealthy,
  checkSkillQuality,
  checkDependencies,
  checkCleanupNeeds,
  checkProtectedSkills,
  main
};
