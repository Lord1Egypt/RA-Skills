---
name: memguard
description: Memory leak & resource management scanner -- detects unclosed handles, event listener leaks, circular references, unbounded caches, missing cleanup, dangling timers, and resource lifecycle issues across all languages
homepage: https://memguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83e\udde0",
      "primaryEnv": "MEMGUARD_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash"]
      },
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

# MemGuard -- Memory Leak & Resource Management Scanner

MemGuard scans codebases for memory leaks and resource management issues: unclosed file handles, event listener leaks, circular references, unbounded caches/maps, missing cleanup in React useEffect, dangling timers/intervals, unreleased database connections, missing stream close, forgotten subscriptions, and retained DOM references -- across JS/TS, Python, Java, Go, Rust, and C#. It uses regex-based pattern matching against 90+ resource lifecycle patterns, lefthook for git hook integration, and produces markdown reports with actionable remediation recommendations. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `memguard scan [file|directory]`
One-shot memory leak and resource management scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/memguard.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 90+ resource lifecycle detection patterns against each file
4. Respects .gitignore and allowlist files
5. Calculates a resource health score (0-100) per file and overall
6. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if too many issues found
9. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Scan my code for memory leaks" -> runs `memguard scan .`
- "Check this file for resource leaks" -> runs `memguard scan src/app.ts`
- "Find unclosed file handles in my project" -> runs `memguard scan src/`
- "Are there event listener leaks in my codebase?" -> runs `memguard scan .`
- "Check for missing useEffect cleanup" -> runs `memguard scan .`

#### `memguard hook install`
Install git pre-commit hooks that scan staged files for memory leaks before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/memguard.sh" hook install
```

**What it does:**
1. Copies lefthook config to project root
2. Installs lefthook pre-commit hook
3. On every commit: scans all staged files for resource leaks, blocks commit if critical/high findings, shows remediation advice

#### `memguard hook uninstall`
Remove MemGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" hook uninstall
```

#### `memguard report [directory]`
Generate a markdown resource health report with findings, severity breakdown, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" report [directory]
```

**What it does:**
1. Runs full scan of the directory
2. Generates a formatted markdown report from template
3. Includes per-file breakdowns, resource health scores, remediation priority
4. Output suitable for code reviews and tech debt tracking

### Pro Tier ($19/user/month -- requires MEMGUARD_LICENSE_KEY)

#### `memguard watch [directory]`
Continuous monitoring mode that watches for file changes and re-scans automatically.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/memguard.sh" watch [directory]
```

**What it does:**
1. Validates Pro+ license
2. Monitors directory for file changes using filesystem polling
3. Re-scans changed files automatically
4. Outputs real-time findings as files are modified
5. Useful during development for immediate feedback on resource leaks

#### `memguard ci [directory]`
CI/CD integration mode with structured exit codes and machine-readable output.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" ci [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Outputs findings in a CI-friendly format
4. Exit code 0 if clean, 1 if critical/high issues found
5. Compatible with GitHub Actions, GitLab CI, Jenkins, CircleCI
6. Supports severity threshold configuration

### Team Tier ($39/user/month -- requires MEMGUARD_LICENSE_KEY with team tier)

#### `memguard team-report [directory]`
Aggregate team metrics across the codebase with trend analysis.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" team-report [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs comprehensive scan of the entire codebase
3. Generates aggregate team metrics and category breakdowns
4. Identifies hotspot files with the most resource issues
5. Produces trend data when baselines exist for comparison
6. Output suitable for engineering leadership and sprint planning

#### `memguard baseline [directory]`
Establish a baseline of known resource issues for tracking progress over time.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" baseline [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans directory and records all current findings as baseline
3. Saves baseline to .memguard-baseline.json
4. Future scans report improvement/regression against the baseline
5. Useful for tech debt tracking in established codebases

#### `memguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/memguard.sh" status
```

## Detected Resource Leak Patterns

MemGuard detects 90+ resource lifecycle patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **File Handles (FH)** | Python open() without close/with, Java FileInputStream without close, Node fs.open without fs.close, missing using/with statements, unclosed database connections | Critical/High |
| **Event Listeners (EL)** | addEventListener without removeEventListener, on() without off(), missing event cleanup in React lifecycle, event emitter leaks, global event handlers never removed | High/Medium |
| **Circular References (CR)** | Parent-child circular refs, self-referencing objects, closure-captured references to parent scope, mutual references between classes, WeakRef/WeakMap needed but not used | High/Medium |
| **Unbounded Caches (UC)** | Map/Set growing without limit, in-memory cache without TTL/eviction, global arrays accumulating, memoization without size limit, localStorage unbounded writes | High/Medium |
| **React Cleanup (RC)** | useEffect without cleanup return, setInterval in useEffect without clearInterval, subscription in useEffect without unsubscribe, state update after unmount, ref held after unmount | High/Medium |
| **Timers & Streams (TM)** | setInterval without clearInterval, setTimeout in loops, stream pipe without error handling, readable stream not destroyed, missing stream.end(), unclosed WebSocket | Critical/High |

## Configuration

Users can configure MemGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "memguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "allowlistFile": ".memguard-allowlist",
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning JS/TS, Python, Java, Go, Rust, and C# in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = resource issues detected (for CI/CD integration)
- Scoring: critical=25pts, high=15pts, medium=8pts, low=3pts deducted from 100 base

## Error Handling

- If lefthook is not installed and user tries `hook install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://memguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If .memguard-allowlist is missing, skip allowlist filtering gracefully

## When to Use MemGuard

The user might say things like:
- "Scan my code for memory leaks"
- "Find unclosed file handles in my project"
- "Check for event listener leaks"
- "Are there missing useEffect cleanups?"
- "Find resource leaks in my codebase"
- "Scan for dangling timers and intervals"
- "Check for unbounded caches"
- "Find circular references in my code"
- "Detect missing stream close calls"
- "Check for database connection leaks"
- "Run a memory scan before I push"
- "Set up pre-commit hooks for resource leak detection"
- "Generate a resource health report"
- "Find forgotten event subscriptions"
- "Check for missing cleanup functions"
- "Scan for retained DOM references"
- "Establish a baseline for resource issues"
- "Monitor my code for memory leaks in real-time"
