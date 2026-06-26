---
name: PipelineLint
version: 1.0.0
description: "CI/CD pipeline anti-pattern analyzer -- detects hardcoded secrets, missing cache configs, skipped tests, unsafe deployments, no approval gates, and environment configuration issues"
homepage: https://pipelinelint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd27",
      "primaryEnv": "PIPELINELINT_LICENSE_KEY",
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

# PipelineLint -- CI/CD Pipeline Anti-Pattern Analyzer

PipelineLint scans codebases for CI/CD pipeline anti-patterns, hardcoded secrets, missing cache configurations, skipped tests, unsafe deployments, no approval gates, unpinned dependencies, and environment configuration issues. It uses regex-based pattern matching against 90 pipeline-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `pipelinelint scan [file|directory]`
One-shot pipeline quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 pipeline quality patterns against each file (free tier limit)
4. Calculates a pipeline quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if pipeline quality is poor
8. Free tier limited to first 30 patterns (SE + CF categories)

**Example usage scenarios:**
- "Scan my pipeline for security issues" -> runs `pipelinelint scan .`
- "Check this workflow file for anti-patterns" -> runs `pipelinelint scan .github/workflows/ci.yml`
- "Find hardcoded secrets in my CI config" -> runs `pipelinelint scan .`
- "Audit my CI/CD pipeline configuration" -> runs `pipelinelint scan .`
- "Check for missing cache configs" -> runs `pipelinelint scan .`

### Pro Tier ($19/user/month -- requires PIPELINELINT_LICENSE_KEY)

#### `pipelinelint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering secrets, caching, testing, and dependency safety.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 pipeline patterns (SE, CF, TS, AR categories)
3. Detects skipped tests and disabled quality checks
4. Identifies unsafe dependency management practices
5. Full category breakdown reporting

#### `pipelinelint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `pipelinelint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `pipelinelint scan --category SE [directory]`
Filter scan to a specific check category (SE, CF, TS, AR, DP, EN).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category SE
```

### Team Tier ($39/user/month -- requires PIPELINELINT_LICENSE_KEY with team tier)

#### `pipelinelint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including deployment safety and environment configuration.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes deployment safety checks (no approval gates, force push, destructive operations)
4. Includes environment configuration checks (hardcoded values, no timeouts, plain HTTP)
5. Full category breakdown with per-file results

#### `pipelinelint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `pipelinelint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

PipelineLint detects 90 CI/CD pipeline anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Secrets & Security** | SE | 15 | Hardcoded passwords, API keys in YAML, tokens in logs, credentials in curl commands, SSH keys inline | high -- critical |
| **Caching & Performance** | CF | 15 | No cache for npm/pip/maven, redundant installs, missing dependency caching, slow Docker builds | low -- medium |
| **Testing & Quality** | TS | 15 | Skipped tests, disabled linting, no coverage enforcement, --no-verify flags, continue-on-error abuse | medium -- high |
| **Artifacts & Dependencies** | AR | 15 | Unpinned Docker tags, curl-to-shell, unverified downloads, disabled SSL, GitHub Actions on branch refs | medium -- high |
| **Deployment Safety** | DP | 15 | No approval gates, force push, auto-approve terraform, destructive SQL, no rollback strategy | high -- critical |
| **Environment & Configuration** | EN | 15 | Hardcoded localhost, no timeouts, no retries, plain HTTP URLs, hardcoded database connection strings | low -- high |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | SE, CF |
| **Pro** | 60 | SE, CF, TS, AR |
| **Team** | 90 | SE, CF, TS, AR, DP, EN |
| **Enterprise** | 90 | SE, CF, TS, AR, DP, EN + priority support |

## Scoring

PipelineLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Security vulnerability or deployment safety risk |
| **High** | -15 per finding | Significant pipeline problem (skipped tests, insecure deps) |
| **Medium** | -8 per finding | Moderate concern (missing caching, env misconfiguration) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent pipeline configuration |
| **B** | 80-89 | Good configuration with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor pipeline quality |
| **F** | Below 60 | Critical pipeline problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure PipelineLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "pipelinelint": {
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
- If license key is invalid or expired, show clear message with link to https://pipelinelint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use PipelineLint

The user might say things like:
- "Scan my CI/CD pipeline for issues"
- "Check my GitHub Actions workflow"
- "Find hardcoded secrets in my pipeline config"
- "Detect unsafe deployment practices"
- "Are there any missing cache configurations?"
- "Check for skipped tests in my CI"
- "Audit my pipeline security"
- "Find unpinned dependencies in my workflow"
- "Check for deployment safety issues"
- "Scan for pipeline anti-patterns"
- "Run a pipeline quality audit"
- "Generate a pipeline quality report"
- "Check if my Jenkinsfile has security issues"
- "Find force push commands in my CI config"
- "Check my GitLab CI for best practices"
