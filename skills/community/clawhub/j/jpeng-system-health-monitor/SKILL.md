---
name: system-health-monitor
description: Monitor system health including disk space, memory usage, process status, and evolution metrics to detect potential issues early. Use when checking system health, diagnosing issues, or during heartbeat checks.
---

# System Health Monitor

Monitors system health for evolution system stability and early issue detection.

## Usage

```javascript
const monitor = require('./skills/system-health-monitor');

// Run health check
const result = await monitor.check();

// Get formatted report
console.log(monitor.formatReport(result));
```

## API

### `check()`

Runs comprehensive system health check.

- Returns: `{ status, checks, issues, timestamp }`

### `formatReport(healthResult)`

Generates a human-readable health report.

### `main()`

CLI entry point - runs check and prints report.

## Output Format

```
✅ System Health: HEALTHY

💾 Disk: 45% used (12G available)
🧠 Memory: 62% used (3.2G free)
⚙️ System: 4 CPUs, uptime 5d 12h 30m
   Load: 0.52, 0.48, 0.45
🔄 Evolution: Cycle 116
📦 Skills: 612 installed
```

## Health Checks

1. **Disk Space**: Warns at 80%, critical at 95%
2. **Memory Usage**: Warns at 80%, critical at 95%
3. **Evolution Status**: Checks for stale cycles
4. **Process Info**: CPU count, load average, uptime
5. **Skills Count**: Total installed skills

## Status Levels

- `healthy`: All checks passed
- `warning`: Non-critical issues detected
- `critical`: Immediate attention required

## Integration

Can be integrated into:
- Heartbeat checks for periodic monitoring
- Pre-evolution health verification
- Diagnostic troubleshooting
- Alert systems
