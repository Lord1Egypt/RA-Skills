---
name: InputShield
version: 1.0.0
description: "Input validation & sanitization scanner -- catches missing validation, unsafe deserialization, ReDoS, path traversal, command injection, and XSS patterns"
author: ClawHub
tags: [input-validation, sanitization, xss, injection, security, redos]
license: COMMERCIAL
triggers:
  - "inputshield scan"
  - "inputshield check"
  - "inputshield audit"
tools: [Bash, Read, Glob, Grep]
homepage: https://inputshield.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udee1\ufe0f",
      "primaryEnv": "INPUTSHIELD_LICENSE_KEY",
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

# InputShield -- Input Validation & Sanitization Scanner

InputShield scans codebases for missing input validation, unsafe deserialization, ReDoS (Regular Expression Denial of Service), path traversal, command injection, XSS via unsanitized output, and other input handling vulnerabilities. It uses regex-based pattern matching against 90 vulnerability patterns across 6 detection categories, produces markdown reports with actionable remediation recommendations, and integrates with git hooks via lefthook. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `inputshield scan [file|directory]`
One-shot input validation scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 90 input validation vulnerability detection patterns against each file
4. Respects .gitignore and exclusion files
5. Calculates an input safety score (0-100) per file and overall
6. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if score < 70
9. Free tier limited to first 30 patterns (5 per category)

**Example usage scenarios:**
- "Scan my code for input validation issues" -> runs `inputshield scan .`
- "Check for XSS vulnerabilities" -> runs `inputshield scan src/`
- "Find command injection risks" -> runs `inputshield scan .`
- "Audit input handling in my project" -> runs `inputshield scan .`
- "Check for ReDoS patterns" -> runs `inputshield scan .`
- "Find path traversal vulnerabilities" -> runs `inputshield scan src/`

### Pro Tier ($19/user/month -- requires INPUTSHIELD_LICENSE_KEY)

#### `inputshield scan --tier pro [file|directory]`
Full scan with 60 patterns (10 per category).

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro --license-key "$INPUTSHIELD_LICENSE_KEY"
```

**What it does:**
1. Validates Pro+ license
2. Runs expanded pattern set (60 of 90 patterns)
3. All free tier features plus deeper detection coverage
4. Unlimited file scanning

#### `inputshield hooks install`
Install git pre-commit hooks that scan staged files for input validation issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged files, blocks commit if critical/high findings

#### `inputshield hooks uninstall`
Remove InputShield git hooks.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks uninstall
```

#### `inputshield report [directory]`
Generate a markdown input validation report with findings, severity breakdown, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" report --path [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, input safety scores, remediation priority
5. Output suitable for security reviews and compliance audits

### Team/Enterprise Tier ($39/user/month -- requires INPUTSHIELD_LICENSE_KEY with team tier)

#### `inputshield scan --tier team [file|directory]`
Complete scan with all 90 patterns (15 per category).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier team --license-key "$INPUTSHIELD_LICENSE_KEY"
```

#### `inputshield audit [directory]`
Deep input validation audit with all 90 patterns and verbose output.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" audit --path [directory] --verbose
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns with verbose output
3. Per-category breakdown with detailed statistics
4. JSON/HTML output formats available

#### `inputshield scan --category [IV|DS|RD|PT|CI|XS]`
Category-specific scan to focus on a single vulnerability class.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --category CI
```

#### `inputshield status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Detection Categories

InputShield detects 90 vulnerability patterns across 6 categories (15 patterns each):

| Category | Code | Examples | Severities |
|----------|------|----------|------------|
| **Input Validation** | IV | Missing length checks, no type validation, raw user input acceptance, missing allowlist, no boundary checks, unvalidated numeric input, missing null checks, regex-less format validation | Critical/High/Medium/Low |
| **Deserialization** | DS | Unsafe JSON.parse, pickle.loads, yaml.load without SafeLoader, Java ObjectInputStream, unvalidated unmarshaling, PHP unserialize, Ruby Marshal.load, .NET BinaryFormatter | Critical/High/Medium |
| **ReDoS** | RD | Catastrophic backtracking, nested quantifiers, overlapping alternations, exponential patterns, unbounded repetition on complex groups, evil regex constructs | High/Medium/Low |
| **Path Traversal** | PT | Directory traversal (../), unsanitized file paths, user-controlled file access, symlink following, path joining with user input, open() with variables, file inclusion | Critical/High/Medium |
| **Command Injection** | CI | Shell exec with user input, eval(), exec(), system() with variables, subprocess with shell=True, os.popen, template injection, child_process.exec | Critical/High/Medium |
| **XSS/Output** | XS | innerHTML with user data, dangerouslySetInnerHTML, document.write, unsanitized template interpolation, missing output encoding, v-html directive, raw HTML rendering | Critical/High/Medium/Low |

## Severity Levels

| Level | Meaning | Score Weight | Action Required |
|-------|---------|-------------|-----------------|
| **Critical** | Directly exploitable vulnerabilities (RCE, injection) | -25 points | Fix immediately -- blocks deployment |
| **High** | Serious security risks requiring prompt attention | -15 points | Fix in current sprint |
| **Medium** | Potential vulnerabilities that need review | -8 points | Review and remediate |
| **Low** | Informational, possible false positives, style issues | -3 points | Investigate when convenient |

## Scoring System

InputShield calculates an **Input Safety Score** from 0 to 100:

- Score starts at **100** (clean)
- Each finding deducts points based on severity: critical=25, high=15, medium=8, low=3
- Score floors at **0** (cannot go negative)
- **Pass threshold: 70** (exit code 0 if >= 70, exit code 1 if < 70)

### Letter Grades

| Grade | Score Range | Meaning |
|-------|------------|---------|
| **A** | 90-100 | Excellent -- minimal or no input validation issues |
| **B** | 80-89 | Good -- minor issues that should be addressed |
| **C** | 70-79 | Acceptable -- passing threshold, issues need attention |
| **D** | 60-69 | Poor -- below threshold, significant issues found |
| **F** | 0-59 | Failing -- critical input validation vulnerabilities detected |

## Tier-Based Pattern Access

| Tier | Patterns Available | Per Category | Price |
|------|-------------------|-------------|-------|
| **Free** | 30 patterns | 5 per category | $0 |
| **Pro** | 60 patterns | 10 per category | $19/user/month |
| **Team** | 90 patterns (all) | 15 per category | $39/user/month |
| **Enterprise** | 90 patterns (all) | 15 per category | Custom pricing |

## Configuration

Users can configure InputShield in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "inputshield": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "markdown",
          "categories": ["IV", "DS", "RD", "PT", "CI", "XS"]
        }
      }
    }
  }
}
```

## Output Formats

InputShield supports three output formats via `--format`:

- **text** (default) -- Colorized terminal output with severity badges
- **json** -- Structured JSON output for CI/CD integration
- **html** -- HTML report with severity highlighting and category charts

## Important Notes

- **Free tier** works immediately with no configuration (30 patterns, 5 per category)
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (score < 70, for CI/CD integration)
- All regex patterns use POSIX ERE syntax compatible with `grep -E`

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://inputshield.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If --category specifies an invalid category, show available categories

## When to Use InputShield

The user might say things like:
- "Scan my code for input validation issues"
- "Check for XSS vulnerabilities"
- "Find command injection risks in my project"
- "Audit input handling"
- "Check for ReDoS patterns"
- "Find path traversal vulnerabilities"
- "Scan for unsafe deserialization"
- "Check if my code sanitizes user input"
- "Find missing input validation"
- "Detect SQL injection and command injection"
- "Check for unsafe eval usage"
- "Scan for innerHTML XSS risks"
- "Find pickle.loads and yaml.load issues"
- "Generate an input validation report"
- "Set up pre-commit hooks for input validation"
- "Run a security scan focused on input handling"
