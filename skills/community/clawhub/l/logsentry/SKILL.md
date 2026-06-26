---
name: LogSentry
version: 1.0.0
description: "Logging quality & observability analyzer -- detects missing structured logging, sensitive data in logs, inconsistent log levels, and log injection vulnerabilities"
homepage: https://logsentry.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udcdd",
      "primaryEnv": "LOGSENTRY_LICENSE_KEY",
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

# LogSentry -- Logging Quality & Observability Analyzer

LogSentry scans codebases for logging anti-patterns, missing structured logging, sensitive data exposure in log output, inconsistent log levels, missing correlation IDs, and log injection vulnerabilities. It uses regex-based pattern matching against 90 logging-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `logsentry scan [file|directory]`
One-shot logging quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 logging quality patterns against each file (free tier limit)
4. Calculates a logging quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if logging quality is poor
8. Free tier limited to first 30 patterns (SL + LL categories)

**Example usage scenarios:**
- "Scan my code for logging issues" -> runs `logsentry scan .`
- "Check this file for logging anti-patterns" -> runs `logsentry scan src/server.ts`
- "Find sensitive data in my logs" -> runs `logsentry scan src/`
- "Audit logging quality in my project" -> runs `logsentry scan .`
- "Check for log injection vulnerabilities" -> runs `logsentry scan .`

### Pro Tier ($19/user/month -- requires LOGSENTRY_LICENSE_KEY)

#### `logsentry scan --tier pro [file|directory]`
Extended scan with 60 patterns covering structured logging, log levels, sensitive data, and log injection.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 logging patterns (SL, LL, SD, LI categories)
3. Detects sensitive data in logs (passwords, tokens, PII)
4. Identifies log injection vulnerabilities
5. Full category breakdown reporting

#### `logsentry scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `logsentry scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `logsentry scan --category SD [directory]`
Filter scan to a specific check category (SL, LL, SD, LI, CI, OB).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category SD
```

### Team Tier ($39/user/month -- requires LOGSENTRY_LICENSE_KEY with team tier)

#### `logsentry scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including correlation IDs and observability.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes correlation/context checks (missing request IDs, trace IDs)
4. Includes observability checks (missing metrics, health checks, audit trails)
5. Full category breakdown with per-file results

#### `logsentry scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `logsentry status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

LogSentry detects 90 logging anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Structured Logging** | SL | 15 | Missing structured logging, print/println instead of loggers, string concatenation in log messages, missing log context fields | medium -- high |
| **Log Levels** | LL | 15 | Incorrect log level usage, debug in production, missing error-level for exceptions, inconsistent level patterns | low -- high |
| **Sensitive Data** | SD | 15 | Passwords/tokens/PII in log output, logging request bodies, credit card patterns, SSN/email exposure | high -- critical |
| **Log Injection** | LI | 15 | Unsanitized user input in logs, newline injection, CRLF attacks, format string vulnerabilities | high -- critical |
| **Correlation & Context** | CI | 15 | Missing request/trace IDs, missing correlation IDs, no structured context, inconsistent timestamp formats | low -- medium |
| **Observability** | OB | 15 | Missing metrics emission, no health check logging, missing audit trail events, absent error rate tracking | low -- medium |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | SL, LL |
| **Pro** | 60 | SL, LL, SD, LI |
| **Team** | 90 | SL, LL, SD, LI, CI, OB |
| **Enterprise** | 90 | SL, LL, SD, LI, CI, OB + priority support |

## Scoring

LogSentry uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe security issue (sensitive data exposure, injection) |
| **High** | -15 per finding | Significant quality problem (missing loggers, concatenation) |
| **Medium** | -8 per finding | Moderate concern (debug levels, missing context) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent logging quality |
| **B** | 80-89 | Good logging with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor logging quality |
| **F** | Below 60 | Critical logging problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure LogSentry in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "logsentry": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
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
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://logsentry.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use LogSentry

The user might say things like:
- "Scan my code for logging issues"
- "Check my logging quality"
- "Find sensitive data in my logs"
- "Detect log injection vulnerabilities"
- "Are there any passwords being logged?"
- "Check for missing structured logging"
- "Audit my observability practices"
- "Find inconsistent log levels"
- "Check for missing correlation IDs"
- "Scan for logging anti-patterns"
- "Run a logging quality audit"
- "Generate a logging quality report"
- "Check if user input is being logged unsafely"
- "Find print statements that should be logger calls"
- "Check my code for log injection risks"
