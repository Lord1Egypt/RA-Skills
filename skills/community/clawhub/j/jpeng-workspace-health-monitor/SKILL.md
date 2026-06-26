---
name: workspace-health-monitor
description: Performs comprehensive workspace health checks including disk usage, file counts, skill health, large files, and empty directories with actionable recommendations. Use when checking workspace health, diagnosing issues, or performing maintenance.
---

# Workspace Health Monitor

Performs comprehensive workspace health checks and generates actionable recommendations.

## Usage

```javascript
const monitor = require('./skills/workspace-health-monitor');

// Perform health check
const report = monitor.check('/path/to/workspace');

// Generate markdown report
console.log(monitor.generateReport(report));
```

## API

### `check(workspacePath, options)`

Performs comprehensive workspace health check.

**Options:**
- `largeFileThresholdMB` (number): Size threshold for large files. Default: `10`
- `includeEmptyDirs` (boolean): Check for empty directories. Default: `true`
- `includeLargeFiles` (boolean): Check for large files. Default: `true`

**Returns:**
```javascript
{
  healthScore: number,      // 0-100
  status: 'healthy' | 'warning' | 'critical',
  metrics: {
    timestamp: string,
    workspace: string,
    diskUsage: {
      totalSize: number,
      totalSizeMB: number,
      totalSizeFormatted: string
    },
    files: {
      total: number,
      directories: number
    },
    skills: {
      total: number,
      healthy: number,
      broken: number,
      missingIndex: string[],
      missingSkillMd: string[],
      missingPackage: string[]
    },
    largeFiles: [{ path, size, sizeFormatted }],
    emptyDirs: string[],
    fileTypes: { [extension]: count }
  },
  recommendations: [{
    severity: 'high' | 'medium' | 'low' | 'info',
    category: string,
    message: string,
    details?: string,
    action: string
  }]
}
```

### `checkSkillHealth(skillsDir)`

Checks health of all skills in a directory.

### `findLargeFiles(workspacePath, thresholdMB)`

Finds files larger than the threshold.

### `findEmptyDirectories(workspacePath)`

Finds empty directories in the workspace.

### `generateReport(report)`

Generates a markdown-formatted health report.

### `formatBytes(bytes)`

Formats bytes to human-readable size.

## Example Output

```
# Workspace Health Report

**Status:** ✅ HEALTHY (Score: 92/100)
**Timestamp:** 2026-03-27T04:30:00.000Z

## Disk Usage

- **Total Size:** 256.78 MB
- **Files:** 3,456
- **Directories:** 234

## Skills Health

- **Total Skills:** 150
- **Healthy:** 145
- **Broken:** 5
- **Missing index.js:** skill-a, skill-b, skill-c

## Large Files (>10MB)

- `logs/evolution.log` (45.23 MB)
- `data/cache.json` (23.45 MB)

## Recommendations

🔴 **skills**: 5 broken skill(s) found
  - Missing index.js: skill-a, skill-b, skill-c
  - Action: Fix or remove broken skills

🟡 **storage**: 2 large file(s) found (>10MB)
  - logs/evolution.log (45.23 MB), data/cache.json (23.45 MB)
  - Action: Consider archiving or removing large files
```

## Health Score Calculation

The health score (0-100) is calculated based on:

- **Broken skills**: -30 points max for broken skill ratio
- **Large files**: -10 points for >10 large files
- **Empty directories**: -10 points for >20 empty directories
- **Workspace size**: -10 points for >1GB total size

## Status Levels

- **Healthy** (80-100): Workspace is in good condition
- **Warning** (60-79): Some issues need attention
- **Critical** (0-59): Immediate action required
