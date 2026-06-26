---
name: workspace-health-dashboard
description: Unified health monitoring dashboard that consolidates skill quality, dependency security, cleanup needs, and protected skills status into a single health check report. Use when checking overall workspace health or running system diagnostics.
---

# Workspace Health Dashboard

Unified health monitoring for the entire workspace.

## Usage

```javascript
const { generateDashboard, formatDashboard, isHealthy } = require('./skills/workspace-health-dashboard');

// Generate full dashboard
const dashboard = generateDashboard();
console.log(formatDashboard(dashboard));

// Quick check
if (!isHealthy()) {
  console.log('Workspace needs attention!');
}
```

## Functions

### generateDashboard(options?)
Runs all health checks and returns:
- Overall health score (0-100)
- Skill quality metrics
- Dependency status
- Cleanup recommendations
- Protected skills status

### formatDashboard(dashboard)
Generates human-readable dashboard with icons.

### isHealthy(options?)
Quick boolean check - returns true if all checks pass.

## Health Checks

1. **Skill Quality** - % of skills with complete structure
2. **Dependencies** - Scan for known vulnerabilities
3. **Cleanup** - Junk folders and incomplete skills
4. **Protected Skills** - Critical skills present

## Health Status

- ✅ **Healthy** - All checks pass
- ⚠️ **Warning** - Some issues found
- 🔴 **Critical** - Immediate attention needed

## Integration

Works with:
- `skill-quality-auditor` - Detailed skill analysis
- `skill-cleanup-executor` - Execute cleanup
- `dependency-vulnerability-scanner` - Security audit
