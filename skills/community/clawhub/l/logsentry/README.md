# LogSentry

**Logging Quality & Observability Analyzer**

LogSentry scans codebases for logging anti-patterns, missing structured logging, sensitive data exposure in log output, inconsistent log levels, missing correlation IDs, and log injection vulnerabilities. 90 detection patterns across 6 categories. 100% local. Zero telemetry.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [CLI Options](#cli-options)
- [Check Categories](#check-categories)
- [Scoring](#scoring)
- [Output Formats](#output-formats)
- [Tier System](#tier-system)
- [Configuration](#configuration)
- [Git Hooks](#git-hooks)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

LogSentry is a ClawHub skill. It requires `bash` and `grep` (POSIX ERE-compatible).

### Prerequisites

- **bash** 4.0+ (macOS, Linux, or WSL on Windows)
- **grep** with `-E` flag support (GNU grep or BSD grep)
- **git** (for hook integration)
- **lefthook** (optional, for git pre-commit hooks)

### Install via ClawHub

```bash
# LogSentry is available as a ClawHub skill
# Place in ~/.openclaw/skills/logsentry/ or your skill directory
```

### Manual Installation

```bash
git clone https://github.com/clawhub/logsentry.git
cd logsentry
chmod +x scripts/dispatcher.sh
```

---

## Quick Start

```bash
# Scan current directory for logging issues (free tier)
bash scripts/dispatcher.sh --path .

# Scan a specific file
bash scripts/dispatcher.sh --path src/server.ts

# Scan with JSON output
bash scripts/dispatcher.sh --path . --format json

# Scan only sensitive data patterns
bash scripts/dispatcher.sh --path . --category SD

# Verbose output
bash scripts/dispatcher.sh --path . --verbose
```

---

## Usage

### Basic Scan (Free)

```bash
bash scripts/dispatcher.sh --path /path/to/project
```

Scans all source files and reports findings from the first 30 patterns (Structured Logging and Log Levels categories).

### Extended Scan (Pro)

```bash
LOGSENTRY_LICENSE_KEY="your-jwt-key" \
  bash scripts/dispatcher.sh --path /path/to/project
```

With a Pro license, scans with 60 patterns covering Structured Logging, Log Levels, Sensitive Data, and Log Injection.

### Full Scan (Team/Enterprise)

```bash
LOGSENTRY_LICENSE_KEY="your-jwt-key" \
  bash scripts/dispatcher.sh --path /path/to/project
```

With a Team or Enterprise license, runs all 90 patterns across all 6 categories.

---

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--path <path>` | File or directory to scan | `.` (current directory) |
| `--format <fmt>` | Output format: `text`, `json`, `html` | `text` |
| `--tier <tier>` | Override tier: `free`, `pro`, `team`, `enterprise` | auto-detected |
| `--license-key <key>` | Provide license key directly | env/config |
| `--verbose` | Show detailed per-match output | off |
| `--category <cat>` | Filter to specific category: `SL`, `LL`, `SD`, `LI`, `CI`, `OB` | all available |
| `--help` | Show help | -- |
| `--version` | Show version | -- |

---

## Check Categories

### 1. Structured Logging (SL-001 through SL-015)

Detects code that uses unstructured print/println statements instead of structured logging libraries, string concatenation in log messages instead of parameterized logging, and missing contextual fields.

**Examples detected:**
- `System.out.println("User logged in: " + user)` -- use a logger
- `console.log("Error: " + err.message)` -- use structured fields
- `print(f"Request from {ip}")` -- use logging library with fields
- String concatenation in log calls instead of parameterized messages

### 2. Log Levels (LL-001 through LL-015)

Identifies incorrect or inconsistent log level usage such as using debug level for error conditions, logging exceptions at info level, or using trace/debug in production code paths.

**Examples detected:**
- `logger.debug("Payment failed")` -- should be error
- `log.info(exception)` -- exceptions should be at error level
- `LOG.trace()` calls in production handlers
- Inconsistent level usage across similar operations

### 3. Sensitive Data (SD-001 through SD-015)

Catches sensitive information being written to log output including passwords, API tokens, credit card numbers, SSNs, email addresses, and full HTTP request/response bodies.

**Examples detected:**
- `logger.info("Password: " + password)` -- never log passwords
- `log.debug("Token: " + apiToken)` -- never log tokens
- Credit card number patterns in log strings
- Logging raw HTTP request bodies that may contain PII

### 4. Log Injection (LI-001 through LI-015)

Finds log injection vulnerabilities where unsanitized user input is written directly to logs, enabling newline injection, CRLF attacks, log forging, and format string exploits.

**Examples detected:**
- `logger.info("User input: " + request.getParameter("q"))` -- injection risk
- User-controlled values passed directly to log format strings
- Missing input sanitization before logging
- CRLF sequences that can forge log entries

### 5. Correlation & Context (CI-001 through CI-015)

Identifies missing correlation IDs, request IDs, trace IDs, span IDs, and structured context that is essential for distributed tracing and log aggregation.

**Examples detected:**
- HTTP handlers without request ID logging
- Missing `traceId` / `spanId` in service-to-service calls
- Log messages without structured key-value context
- Inconsistent or missing timestamp formats

### 6. Observability (OB-001 through OB-015)

Detects missing observability practices including absent metrics emission, missing health check logging, no audit trail events, and absent error rate tracking.

**Examples detected:**
- Request handlers without latency metrics
- Missing health check endpoint logging
- No audit log for authentication events
- Missing error counters / rate tracking

---

## Scoring

LogSentry calculates a **Logging Quality Score** from 0 to 100:

| Severity | Point Deduction |
|----------|-----------------|
| Critical | -25 per finding |
| High | -15 per finding |
| Medium | -8 per finding |
| Low | -3 per finding |

### Grading

| Grade | Score | Status |
|-------|-------|--------|
| A | 90-100 | Excellent |
| B | 80-89 | Good |
| C | 70-79 | Acceptable (pass threshold) |
| D | 60-69 | Poor |
| F | <60 | Critical |

**Pass/Fail threshold:** Score >= 70 (exit code 0 = pass, 1 = fail)

---

## Output Formats

### Text (default)

Human-readable console output with color-coded severity levels and per-file breakdown.

```bash
bash scripts/dispatcher.sh --path . --format text
```

### JSON

Machine-readable JSON output suitable for CI/CD pipelines and integrations.

```bash
bash scripts/dispatcher.sh --path . --format json
```

Output structure:
```json
{
  "tool": "LogSentry",
  "version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "target": ".",
  "score": 72,
  "grade": "C",
  "pass": true,
  "summary": {
    "files_scanned": 45,
    "total_findings": 12,
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 5
  },
  "findings": [...]
}
```

### HTML

Generates a self-contained HTML report with styling, sortable tables, and category charts.

```bash
bash scripts/dispatcher.sh --path . --format html > report.html
```

---

## Tier System

| Tier | Price | Patterns | Categories |
|------|-------|----------|------------|
| Free | $0 | 30 | SL, LL |
| Pro | $19/user/month | 60 | SL, LL, SD, LI |
| Team | $39/user/month | 90 | SL, LL, SD, LI, CI, OB |
| Enterprise | Custom | 90 | All + priority support |

Get a license at [https://logsentry.pages.dev/pricing](https://logsentry.pages.dev/pricing)

---

## Configuration

### Environment Variable

```bash
export LOGSENTRY_LICENSE_KEY="your-jwt-license-key"
```

### Config File

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "logsentry": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**"],
          "ignoreChecks": [],
          "reportFormat": "text"
        }
      }
    }
  }
}
```

### CLI Flag

```bash
bash scripts/dispatcher.sh --path . --license-key "your-jwt-key"
```

---

## Git Hooks

LogSentry integrates with [lefthook](https://github.com/evilmartians/lefthook) for pre-commit scanning.

### Install Hooks

```bash
# Requires lefthook: brew install lefthook
cp config/lefthook.yml /path/to/repo/lefthook.yml
cd /path/to/repo && lefthook install
```

### How It Works

On every `git commit`, LogSentry scans staged files for logging issues. If critical or high-severity findings are detected, the commit is blocked with remediation advice.

### Skip Hook (Not Recommended)

```bash
git commit --no-verify
```

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: LogSentry Scan
  run: |
    bash path/to/logsentry/scripts/dispatcher.sh \
      --path . \
      --format json \
      --license-key ${{ secrets.LOGSENTRY_LICENSE_KEY }}
```

### GitLab CI

```yaml
logsentry:
  script:
    - bash path/to/logsentry/scripts/dispatcher.sh --path . --format json
  allow_failure: false
```

### Pre-Push Hook

The included `config/lefthook.yml` also configures a pre-push hook that runs a full scan before pushing to remote branches.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-pattern`)
3. Add patterns to the appropriate category in `scripts/patterns.sh`
4. Ensure all regex patterns are valid POSIX ERE (`grep -E` compatible)
5. Test patterns against real-world code samples
6. Submit a pull request

### Pattern Format

Each pattern follows the pipe-delimited format:

```
REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
```

- **REGEX:** POSIX Extended Regular Expression (grep -E compatible)
- **SEVERITY:** `critical`, `high`, `medium`, or `low`
- **CHECK_ID:** Category prefix + number (e.g., `SL-001`)
- **DESCRIPTION:** What the pattern detects
- **RECOMMENDATION:** How to fix the issue

---

## License

LogSentry is commercial software. See [LICENSE](https://logsentry.pages.dev/license) for details.

- Free tier: Available at no cost
- Pro/Team/Enterprise: Requires a valid license key
- All scanning is local -- no code leaves your machine

**Website:** [https://logsentry.pages.dev](https://logsentry.pages.dev)
**Support:** [https://logsentry.pages.dev/support](https://logsentry.pages.dev/support)
**Pricing:** [https://logsentry.pages.dev/pricing](https://logsentry.pages.dev/pricing)
