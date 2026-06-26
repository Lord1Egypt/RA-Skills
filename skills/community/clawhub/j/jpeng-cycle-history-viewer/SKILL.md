---
name: cycle-history-viewer
description: Views and searches evolution cycle history with filtering capabilities for tracking progress and analyzing patterns. Use when reviewing past cycles, searching for specific outcomes, or generating history reports.
---

# Cycle History Viewer

Views and searches evolution cycle history with filtering capabilities.

## Usage

```javascript
const viewer = require('./skills/cycle-history-viewer');

// Get a specific cycle
const status = viewer.get('/path/to/workspace', 486);

// Search with filters
const results = viewer.search('/path/to/workspace', {
  intent: 'innovation',
  result: 'success',
  keyword: 'skill',
  limit: 20
});

// Get summary statistics
const stats = viewer.summary('/path/to/workspace', 100);

// Generate report
console.log(viewer.generateReport('/path/to/workspace', 20));
```

## API

### `listFiles(workspacePath)`

Lists all cycle status files with metadata.

### `get(workspacePath, cycle)`

Gets a specific cycle's status data.

### `search(workspacePath, filters)`

Searches cycle history with filters.

**Filters:**
- `intent` - Filter by intent (innovation|repair|optimize)
- `result` - Filter by result (success|failed)
- `keyword` - Search keyword in status text
- `limit` - Max results (default: 50)

**Returns:**
```javascript
[{
  cycle: number,
  result: string,
  en: string,
  zh: string
}]
```

### `summary(workspacePath, count)`

Gets summary statistics for recent cycles.

**Returns:**
```javascript
{
  total: number,
  success: number,
  failed: number,
  successRate: number,
  byIntent: { innovation, repair, optimize },
  recentCycles: [{ cycle, result, intent }]
}
```

### `generateReport(workspacePath, count)`

Generates markdown report of recent cycles.

### `exportJson(workspacePath, count)`

Exports history to JSON format.

## Status Files

Reads from `logs/status_XXXX.json` files created by each evolution cycle.

## Example Output

```
# 📜 Evolution Cycle History

## Summary

| Metric | Value |
|--------|-------|
| Cycles Shown | 20 |
| Success Rate | 95.0% |
| Innovation | 15 |
| Repair | 3 |
| Optimize | 2 |

## Last 20 Cycles

| Cycle | Result | Intent | Description |
|-------|--------|--------|-------------|
| 0486 | ✅ | innovation | Created evolution-metrics-tracker skill |
| 0485 | ✅ | innovation | Created skill-deprecation-scanner skill |
| 0484 | ✅ | innovation | Created tool-call-logger skill |
```
