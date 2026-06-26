/**
 * Permission Auditor - Review tool usage and permissions
 * Identifies security risks and excessive access
 */

/**
 * Tool risk levels
 */
const TOOL_RISK_LEVELS = {
  // Critical risk - can modify system or exfiltrate data
  exec: 'critical',
  write: 'high',
  edit: 'high',
  gateway: 'critical',

  // Medium risk - can access sensitive data
  read: 'medium',
  browser: 'medium',
  nodes: 'medium',
  cron: 'medium',

  // Low risk - read-only or controlled access
  web_fetch: 'low',
  sessions_list: 'low',
  session_status: 'low',
  message: 'medium',

  // Feishu tools
  feishu_doc: 'medium',
  feishu_drive: 'medium',
  feishu_wiki: 'low',
  feishu_bitable_create_record: 'medium',
  feishu_bitable_update_record: 'medium',
  feishu_bitable_list_records: 'low',

  // TTS
  tts: 'low'
};

/**
 * Risk categories
 */
const RISK_CATEGORIES = {
  critical: {
    score: 100,
    description: 'Can execute arbitrary commands or modify system configuration',
    examples: ['exec', 'gateway config.apply']
  },
  high: {
    score: 75,
    description: 'Can modify files or access sensitive resources',
    examples: ['write', 'edit', 'nodes run']
  },
  medium: {
    score: 50,
    description: 'Can access user data or external services',
    examples: ['read', 'browser', 'message']
  },
  low: {
    score: 25,
    description: 'Read-only or controlled access',
    examples: ['web_fetch', 'session_status', 'tts']
  }
};

/**
 * Analyze tool usage from logs
 * @param {object[]} toolLogs - Array of tool usage records
 * @returns {object}
 */
function auditToolUsage(toolLogs) {
  const stats = {
    totalCalls: 0,
    byTool: {},
    byRisk: {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
      unknown: 0
    },
    patterns: [],
    anomalies: []
  };

  for (const log of toolLogs) {
    stats.totalCalls++;

    const tool = log.tool || log.name || 'unknown';
    const risk = TOOL_RISK_LEVELS[tool] || 'unknown';

    // Count by tool
    if (!stats.byTool[tool]) {
      stats.byTool[tool] = { count: 0, risk };
    }
    stats.byTool[tool].count++;

    // Count by risk
    stats.byRisk[risk]++;

    // Detect patterns
    if (log.success === false) {
      stats.anomalies.push({
        type: 'failed_call',
        tool,
        timestamp: log.timestamp
      });
    }
  }

  // Detect suspicious patterns
  const execCount = stats.byTool.exec?.count || 0;
  if (execCount > 10) {
    stats.patterns.push({
      type: 'high_exec_usage',
      severity: 'high',
      description: `High exec usage detected: ${execCount} calls`,
      recommendation: 'Review exec calls for necessity and safety'
    });
  }

  const writeCount = stats.byTool.write?.count || 0;
  const readCount = stats.byTool.read?.count || 0;
  if (writeCount > readCount * 2) {
    stats.patterns.push({
      type: 'write_heavy',
      severity: 'medium',
      description: `More writes than reads: ${writeCount} writes vs ${readCount} reads`,
      recommendation: 'Verify write operations are intentional'
    });
  }

  // Check for critical tool usage
  if (stats.byRisk.critical > 0) {
    stats.patterns.push({
      type: 'critical_tools_used',
      severity: 'critical',
      description: `Critical risk tools used ${stats.byRisk.critical} times`,
      recommendation: 'Review all critical tool usage for security compliance'
    });
  }

  return stats;
}

/**
 * Check if permissions are excessive
 * @param {string[]} required - Required permissions
 * @param {string[]} granted - Granted permissions
 * @returns {object}
 */
function checkPermissions(required, granted) {
  const issues = [];

  // Check for missing required permissions
  const missing = required.filter(p => !granted.includes(p));
  if (missing.length > 0) {
    issues.push({
      type: 'missing_permissions',
      severity: 'high',
      permissions: missing,
      description: `Missing required permissions: ${missing.join(', ')}`
    });
  }

  // Check for excessive permissions
  const excessive = granted.filter(p => !required.includes(p));
  if (excessive.length > 0) {
    issues.push({
      type: 'excessive_permissions',
      severity: 'medium',
      permissions: excessive,
      description: `Excessive permissions granted: ${excessive.join(', ')}`
    });
  }

  // Check for wildcard permissions
  const wildcards = granted.filter(p => p.includes('*'));
  if (wildcards.length > 0) {
    issues.push({
      type: 'wildcard_permissions',
      severity: 'high',
      permissions: wildcards,
      description: `Wildcard permissions detected: ${wildcards.join(', ')}`
    });
  }

  return {
    required,
    granted,
    missing,
    excessive,
    issues,
    score: calculatePermissionScore(issues)
  };
}

/**
 * Calculate permission security score
 * @param {object[]} issues
 * @returns {number} 0-100 (100 = most secure)
 */
function calculatePermissionScore(issues) {
  let score = 100;

  for (const issue of issues) {
    switch (issue.severity) {
      case 'critical':
        score -= 30;
        break;
      case 'high':
        score -= 20;
        break;
      case 'medium':
        score -= 10;
        break;
      case 'low':
        score -= 5;
        break;
    }
  }

  return Math.max(0, score);
}

/**
 * Generate security audit report
 * @param {object} auditResult
 * @returns {object}
 */
function generateReport(auditResult) {
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      totalCalls: auditResult.totalCalls,
      riskDistribution: auditResult.byRisk,
      patternsFound: auditResult.patterns.length,
      anomaliesFound: auditResult.anomalies.length
    },
    riskAssessment: assessRisk(auditResult),
    patterns: auditResult.patterns,
    anomalies: auditResult.anomalies,
    recommendations: generateRecommendations(auditResult)
  };

  return report;
}

/**
 * Assess overall risk level
 * @param {object} stats
 * @returns {object}
 */
function assessRisk(stats) {
  const criticalRatio = stats.byRisk.critical / (stats.totalCalls || 1);
  const highRatio = stats.byRisk.high / (stats.totalCalls || 1);

  let level = 'low';
  let score = 100;

  if (criticalRatio > 0.1) {
    level = 'critical';
    score = 20;
  } else if (criticalRatio > 0.05) {
    level = 'high';
    score = 40;
  } else if (highRatio > 0.2) {
    level = 'high';
    score = 50;
  } else if (highRatio > 0.1) {
    level = 'medium';
    score = 70;
  }

  return {
    level,
    score,
    description: RISK_CATEGORIES[level]?.description || 'Unknown risk level'
  };
}

/**
 * Generate security recommendations
 * @param {object} stats
 * @returns {string[]}
 */
function generateRecommendations(stats) {
  const recommendations = [];

  if (stats.byRisk.critical > 0) {
    recommendations.push('Review all critical tool usage and ensure proper authorization');
  }

  if (stats.byRisk.high > stats.totalCalls * 0.3) {
    recommendations.push('High-risk tool usage is elevated - consider access controls');
  }

  if (stats.anomalies.length > stats.totalCalls * 0.1) {
    recommendations.push('High failure rate detected - investigate tool errors');
  }

  for (const pattern of stats.patterns) {
    if (pattern.recommendation) {
      recommendations.push(pattern.recommendation);
    }
  }

  if (recommendations.length === 0) {
    recommendations.push('No immediate security concerns detected');
  }

  return recommendations;
}

/**
 * Format report for display
 * @param {object} report
 * @returns {string}
 */
function formatReport(report) {
  const lines = [];

  lines.push('Permission Audit Report');
  lines.push('='.repeat(50));
  lines.push(`Generated: ${report.timestamp}`);
  lines.push('');

  lines.push('Summary:');
  lines.push(`  Total tool calls: ${report.summary.totalCalls}`);
  lines.push(`  Critical: ${report.summary.riskDistribution.critical}`);
  lines.push(`  High: ${report.summary.riskDistribution.high}`);
  lines.push(`  Medium: ${report.summary.riskDistribution.medium}`);
  lines.push(`  Low: ${report.summary.riskDistribution.low}`);
  lines.push('');

  lines.push('Risk Assessment:');
  lines.push(`  Level: ${report.riskAssessment.level.toUpperCase()}`);
  lines.push(`  Score: ${report.riskAssessment.score}/100`);
  lines.push('');

  if (report.patterns.length > 0) {
    lines.push('Patterns Detected:');
    for (const p of report.patterns) {
      lines.push(`  [${p.severity.toUpperCase()}] ${p.description}`);
    }
    lines.push('');
  }

  lines.push('Recommendations:');
  for (const r of report.recommendations) {
    lines.push(`  • ${r}`);
  }

  return lines.join('\n');
}

/**
 * Demo function
 */
async function demo() {
  console.log('Permission Auditor Demo');
  console.log('=======================\n');

  // Demo tool usage audit
  console.log('1. Tool Usage Audit:');
  const sampleLogs = [
    { tool: 'read', success: true },
    { tool: 'read', success: true },
    { tool: 'write', success: true },
    { tool: 'exec', success: true },
    { tool: 'exec', success: true },
    { tool: 'exec', success: false },
    { tool: 'browser', success: true },
    { tool: 'message', success: true },
    { tool: 'read', success: true },
    { tool: 'write', success: true },
    { tool: 'write', success: true },
    { tool: 'write', success: true },
    { tool: 'exec', success: true },
    { tool: 'exec', success: true },
    { tool: 'exec', success: true }
  ];

  const audit = auditToolUsage(sampleLogs);
  console.log(`   Total calls: ${audit.totalCalls}`);
  console.log(`   Critical: ${audit.byRisk.critical}, High: ${audit.byRisk.high}`);
  console.log(`   Medium: ${audit.byRisk.medium}, Low: ${audit.byRisk.low}`);
  console.log();

  // Demo permission check
  console.log('2. Permission Check:');
  const permCheck = checkPermissions(
    ['read', 'write'],
    ['read', 'write', 'exec', 'admin:*']
  );
  console.log(`   Score: ${permCheck.score}/100`);
  console.log(`   Issues: ${permCheck.issues.length}`);
  for (const issue of permCheck.issues) {
    console.log(`   - [${issue.severity.toUpperCase()}] ${issue.description}`);
  }
  console.log();

  // Demo full report
  console.log('3. Full Audit Report:');
  const report = generateReport(audit);
  console.log(formatReport(report));
}

/**
 * CLI entry point
 */
async function main() {
  const args = process.argv.slice(2);

  if (args[0] === 'demo') {
    await demo();
    return;
  }

  console.log('Permission Auditor');
  console.log('==================\n');
  console.log('Exports:', Object.keys(module.exports));
  console.log('\nUsage: node skills/permission-auditor/index.js demo');
}

module.exports = {
  auditToolUsage,
  checkPermissions,
  generateReport,
  assessRisk,
  generateRecommendations,
  formatReport,
  TOOL_RISK_LEVELS,
  RISK_CATEGORIES,
  main
};

// Run main if called directly
if (require.main === module) {
  main().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}
