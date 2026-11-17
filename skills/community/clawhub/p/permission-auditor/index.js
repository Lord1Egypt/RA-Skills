/**
 * Permission Auditor Skill
 * Reviews tool usage patterns and permission configurations
 */

const fs = require('fs');
const path = require('path');

/**
 * Audit tool usage patterns from session transcripts
 * @param {string} workspaceDir - Workspace directory to audit
 * @param {object} options - Audit options
 * @returns {object} Audit results
 */
function auditPermissions(workspaceDir = process.cwd(), options = {}) {
  const results = {
    timestamp: new Date().toISOString(),
    workspace: workspaceDir,
    summary: {
      total_tools_used: 0,
      risky_patterns: 0,
      bypass_attempts: 0,
      policy_violations: 0
    },
    tool_usage: {},
    patterns: [],
    recommendations: []
  };

  // Check for tool policy configuration
  const configPath = path.join(workspaceDir, '.env');
  if (fs.existsSync(configPath)) {
    try {
      const envContent = fs.readFileSync(configPath, 'utf8');
      if (envContent.includes('ALLOW_UNSAFE')) {
        results.patterns.push({
          type: 'unsafe_flag',
          severity: 'high',
          description: 'ALLOW_UNSAFE flag detected in environment'
        });
        results.summary.risky_patterns++;
      }
    } catch (e) {
      // Ignore read errors
    }
  }

  // Analyze recent session logs for tool usage
  const memoryDir = path.join(workspaceDir, 'memory');
  if (fs.existsSync(memoryDir)) {
    try {
      const files = fs.readdirSync(memoryDir);
      const sessionFiles = files.filter(f => f.endsWith('.jsonl') || f.includes('session'));
      
      for (const file of sessionFiles.slice(0, 10)) { // Limit to recent 10 sessions
        try {
          const content = fs.readFileSync(path.join(memoryDir, file), 'utf8');
          const lines = content.split('\n').filter(l => l.trim());
          
          for (const line of lines) {
            // Look for tool usage patterns
            if (line.includes('[TOOL:') || line.includes('tool:') || line.includes('exec')) {
              const toolMatch = line.match(/tool[:\s]+(\w+)/i) || line.match(/\[TOOL[:\s]+(\w+)/i);
              if (toolMatch) {
                const toolName = toolMatch[1].toLowerCase();
                results.tool_usage[toolName] = (results.tool_usage[toolName] || 0) + 1;
                results.summary.total_tools_used++;
              }
              
              // Check for risky patterns
              if (line.includes('elevated') || line.includes('sudo') || line.includes('admin')) {
                results.patterns.push({
                  type: 'elevated_execution',
                  severity: 'medium',
                  description: 'Elevated execution detected in session',
                  file: file
                });
                results.summary.risky_patterns++;
              }
              
              // Check for tool bypass attempts
              if (line.includes('bypass') || line.includes('--force') || line.includes('unsafe')) {
                results.patterns.push({
                  type: 'bypass_attempt',
                  severity: 'high',
                  description: 'Tool bypass attempt detected',
                  file: file
                });
                results.summary.bypass_attempts++;
              }
            }
          }
        } catch (e) {
          // Skip unreadable files
        }
      }
    } catch (e) {
      // Ignore directory read errors
    }
  }

  // Check evolution state for tool policy
  const evolutionStatePath = path.join(workspaceDir, 'memory', 'evolution', 'evolution_state.json');
  if (fs.existsSync(evolutionStatePath)) {
    try {
      const state = JSON.parse(fs.readFileSync(evolutionStatePath, 'utf8'));
      if (state.tool_policy) {
        results.patterns.push({
          type: 'tool_policy_configured',
          severity: 'info',
          description: 'Tool policy is configured in evolution state'
        });
      }
    } catch (e) {
      // Ignore parse errors
    }
  }

  // Generate recommendations
  if (results.summary.bypass_attempts > 0) {
    results.recommendations.push('CRITICAL: Tool bypass attempts detected - review security policy');
  }
  if (results.summary.risky_patterns > 0) {
    results.recommendations.push('WARNING: Elevated executions found - ensure proper authorization');
  }
  if (results.tool_usage['exec'] && results.tool_usage['exec'] > 10) {
    results.recommendations.push('INFO: Heavy exec usage detected - consider registering as tool');
  }
  if (results.summary.total_tools_used === 0) {
    results.recommendations.push('INFO: No tool usage patterns detected in recent sessions');
  }
  if (results.recommendations.length === 0) {
    results.recommendations.push('OK: Tool usage patterns appear normal');
  }

  return results;
}

/**
 * Format audit results for display
 * @param {object} results - Audit results
 * @returns {string} Formatted output
 */
function formatResults(results) {
  const lines = [];

  lines.push('=== Permission Audit Report ===');
  lines.push(`Workspace: ${results.workspace}`);
  lines.push(`Time: ${results.timestamp}`);
  lines.push('');

  lines.push('Summary:');
  lines.push(`  Total tools used: ${results.summary.total_tools_used}`);
  lines.push(`  Risky patterns: ${results.summary.risky_patterns}`);
  lines.push(`  Bypass attempts: ${results.summary.bypass_attempts}`);
  lines.push(`  Policy violations: ${results.summary.policy_violations}`);
  lines.push('');

  if (Object.keys(results.tool_usage).length > 0) {
    lines.push('Tool Usage Frequency:');
    const sorted = Object.entries(results.tool_usage).sort((a, b) => b[1] - a[1]);
    for (const [tool, count] of sorted.slice(0, 5)) {
      lines.push(`  ${tool}: ${count} uses`);
    }
    lines.push('');
  }

  if (results.patterns.length > 0) {
    lines.push('Detected Patterns:');
    for (const pattern of results.patterns) {
      const icon = pattern.severity === 'high' ? '[!]' : 
                   pattern.severity === 'medium' ? '[?]' : '[i]';
      lines.push(`  ${icon} ${pattern.type}: ${pattern.description}`);
      if (pattern.file) {
        lines.push(`      File: ${pattern.file}`);
      }
    }
    lines.push('');
  }

  if (results.recommendations.length > 0) {
    lines.push('Recommendations:');
    for (const rec of results.recommendations) {
      lines.push(`  - ${rec}`);
    }
  }

  return lines.join('\n');
}

/**
 * Main entry point
 */
function main() {
  const workspaceDir = process.argv[2] || process.cwd();
  const results = auditPermissions(workspaceDir);
  console.log(formatResults(results));

  // Exit with error if critical issues found
  if (results.summary.bypass_attempts > 0) {
    process.exit(1);
  }
}

module.exports = {
  auditPermissions,
  formatResults,
  main
};

// Run main if executed directly
if (require.main === module) {
  main();
}