---
name: perfguard
description: Performance anti-pattern scanner — finds N+1 queries, sync I/O, missing pagination, and memory leaks before they hit production
homepage: https://perfguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "⚡",
      "primaryEnv": "PERFGUARD_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# PerfGuard -- Performance Anti-Pattern Scanner

PerfGuard scans your codebase for performance anti-patterns including N+1 queries, synchronous I/O in async code, missing pagination, unbounded loops, memory leaks, and inefficient serialization. It supports Python (Django, Flask, FastAPI, SQLAlchemy), JavaScript/TypeScript (Node.js, React, Express), Ruby (Rails), and Java (JPA/Hibernate). All scanning happens locally using regex-based pattern matching -- no code is sent to external servers.

## Commands

### Free Tier (No license required)

#### `perfguard scan [file|directory]`
One-shot performance anti-pattern scan.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects the project stack (Python, JavaScript/TypeScript, Ruby, Java)
3. Finds all relevant source files (excluding .git/, node_modules/, dist/, build/, vendor/, __pycache__)
4. Runs 40+ performance checks against each source file
5. Outputs findings with: file, line number, check ID, severity, description, recommendation
6. Calculates a performance score (0-100)
7. Free tier: limited to scanning up to 5 source files
8. Exit code 0 if score >= 70, exit code 1 if score < 70 or critical issues found

**Example usage scenarios:**
- "Scan my code for performance issues" -> runs `perfguard scan .`
- "Check for N+1 queries in my Django app" -> runs `perfguard scan .`
- "Find async anti-patterns in my Node.js project" -> runs `perfguard scan src/`
- "Are there performance problems in this file?" -> runs `perfguard scan path/to/file.py`
- "Look for slow database queries" -> runs `perfguard scan .`

### Pro Tier ($19/user/month -- requires PERFGUARD_LICENSE_KEY)

#### `perfguard scan [file|directory]` (unlimited)
Full performance scan with no file limit and all 40+ checks enabled.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" scan [target]
```

**What it does (beyond free):**
1. Unlimited source file scanning
2. Full 40+ performance checks including database, async, memory, and bundle patterns
3. Detailed remediation advice per finding

#### `perfguard hooks install`
Install git pre-commit hooks that scan staged files for performance anti-patterns before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans staged source files for performance anti-patterns, blocks commit if critical issues found

#### `perfguard hooks uninstall`
Remove PerfGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" hooks uninstall
```

#### `perfguard report [directory]`
Generate a markdown performance audit report.

```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report with severity breakdown
4. Includes per-file findings, performance score, and remediation steps
5. Output written to PERFGUARD-REPORT.md

#### `perfguard hotspots [directory]`
Identify the files with the most performance anti-patterns (hot paths).

```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" hotspots [directory]
```

**What it does:**
1. Validates Pro+ license
2. Scans all source files in the directory
3. Ranks files by total anti-pattern count and severity weight
4. Shows top 10 performance hotspot files with issue breakdown
5. Helps prioritize which files to optimize first

### Team Tier ($39/user/month -- requires PERFGUARD_LICENSE_KEY with team tier)

#### `perfguard budget [directory]`
Check code against performance budgets.

```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" budget [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full performance scan
3. Checks results against configurable thresholds: max critical issues, max total issues, minimum score
4. Returns exit code 1 if any budget is exceeded
5. Designed for CI/CD pipeline integration as a quality gate

#### `perfguard trend [directory]`
Show performance trend over recent git history.

```bash
bash "<SKILL_DIR>/scripts/perfguard.sh" trend [directory]
```

**What it does:**
1. Validates Team+ license
2. Checks out recent commits (up to 10) and runs performance scan on each
3. Shows a timeline of performance scores
4. Identifies whether code quality is improving or degrading
5. Helps track the impact of optimizations over time

## Detected Performance Anti-Patterns

PerfGuard checks for 40+ performance anti-patterns across 4 categories:

### Database / ORM Patterns

| Check | Description | Severity |
|-------|-------------|----------|
| N+1 Query | Query inside a loop / loop inside a query | Critical |
| SELECT * | Using SELECT * instead of specific columns | High |
| Missing Eager Loading | No select_related/prefetch_related (Django), includes/eager_load (Rails), JOIN FETCH (JPA) | Critical |
| Unbounded Query | Query without LIMIT or pagination | High |
| Sequential Queries | Multiple queries that could be batched | Medium |
| String SQL Concatenation | Building SQL with string concatenation | Critical |
| Missing Index Hint | Complex queries without index annotations | Medium |

### JavaScript / TypeScript Patterns

| Check | Description | Severity |
|-------|-------------|----------|
| Await in Loop | Sequential async operations instead of parallel | Critical |
| Missing Promise.all | Multiple independent awaits without Promise.all | High |
| Sync File I/O | readFileSync/writeFileSync in server code | High |
| JSON Clone | JSON.parse(JSON.stringify()) for deep cloning | Medium |
| Unbounded Array Ops | Large array operations without chunking | Medium |
| Memory Leak | Event listeners without cleanup | High |
| Missing Memoization | React components without useMemo/useCallback/React.memo | Medium |
| Full Lodash Import | Importing entire lodash instead of specific functions | High |
| Missing Pagination | API responses without pagination | High |
| Console in Production | console.log statements in production code | Low |

### Python Patterns

| Check | Description | Severity |
|-------|-------------|----------|
| Heavy Module in Function | Importing heavy modules inside functions | Medium |
| List vs Generator | Large list comprehensions that should be generators | Medium |
| String Concat in Loop | String concatenation in loops instead of join | Medium |
| Sleep in Async | time.sleep() in async code | Critical |
| Missing Connection Pool | Direct connections without pooling | High |
| Sync in Async | Synchronous I/O in async functions | High |
| Full File Load | Loading entire files into memory | Medium |
| Regex in Loop | Compiling regex inside loops | Medium |

### General Patterns

| Check | Description | Severity |
|-------|-------------|----------|
| Unbounded Retry | Retries without exponential backoff | High |
| Missing Timeout | HTTP requests without timeout | High |
| Polling | Polling instead of webhooks/events | Medium |
| Hardcoded Delay | Hardcoded sleep/delay values | Low |
| Missing Cache | Repeated computations without caching | Medium |
| No Memoization | Recursive functions without memoization | Medium |
| Large Payload | Serialization without streaming | Medium |

## Configuration

Users can configure PerfGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "perfguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "excludePatterns": ["**/node_modules/**", "**/dist/**", "**/.git/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration (limited to 5 source files)
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Supports Python, JavaScript/TypeScript, Ruby, and Java
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = issues found (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://perfguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no source files found in target, report clean scan with info message
- If project stack cannot be auto-detected, try all patterns

## When to Use PerfGuard

The user might say things like:
- "Scan my code for performance issues"
- "Find N+1 queries in my app"
- "Check for async anti-patterns"
- "Are there performance problems in my code?"
- "Look for slow database queries"
- "Find memory leaks in my React app"
- "Check for missing pagination"
- "Scan for sync I/O in my server code"
- "Generate a performance report"
- "Show me performance hotspots"
- "Set up performance checks on my commits"
- "Check if code meets performance budgets"
- "Show performance trends over time"
- "Find unbounded queries"
- "Check for missing eager loading"
