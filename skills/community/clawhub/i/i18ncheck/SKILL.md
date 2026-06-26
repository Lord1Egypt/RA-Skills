---
name: i18ncheck
description: Internationalization & localization readiness scanner -- detects hardcoded strings, missing translations, locale-sensitive formatting, RTL issues, string concatenation in translations, and i18n anti-patterns across all languages
homepage: https://i18ncheck.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83c\udf0d",
      "primaryEnv": "I18NCHECK_LICENSE_KEY",
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

# I18nCheck -- Internationalization & Localization Readiness Scanner

I18nCheck scans codebases for internationalization issues: hardcoded UI strings, missing translation keys, locale-sensitive date/number formatting, RTL layout issues, string concatenation for translations, missing lang attributes, non-Unicode encodings, locale-dependent comparisons, missing pluralization, and timezone-naive datetime usage. It uses regex-based pattern matching against 90+ i18n patterns across JS/TS, Python, Java, Go, Ruby, and PHP. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `i18ncheck scan [file|directory]`
One-shot i18n scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 90+ i18n detection patterns against each file
4. Respects .gitignore and allowlist files
5. Calculates an i18n readiness score (0-100) per file and overall
6. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if too many issues found
9. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Scan my code for i18n issues" -> runs `i18ncheck scan .`
- "Check this file for hardcoded strings" -> runs `i18ncheck scan src/components/Header.tsx`
- "Find internationalization problems in my project" -> runs `i18ncheck scan src/`
- "Are there any untranslated strings in my app?" -> runs `i18ncheck scan .`
- "Check for RTL layout issues" -> runs `i18ncheck scan .`

#### `i18ncheck hook`
Install git pre-commit hooks that scan staged files for i18n issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" hook install
```

**What it does:**
1. Copies lefthook config to project root
2. Installs lefthook pre-commit hook
3. On every commit: scans all staged files for i18n issues, blocks commit if critical/high findings, shows remediation advice

#### `i18ncheck report [directory]`
Generate a markdown i18n readiness report with findings, severity breakdown, and remediation steps.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" report [directory]
```

**What it does:**
1. Runs full scan of the directory
2. Generates a formatted markdown report from template
3. Includes per-file breakdowns, i18n readiness scores, remediation priority
4. Output suitable for i18n audits and localization planning

### Pro Tier ($19/user/month -- requires I18NCHECK_LICENSE_KEY)

#### `i18ncheck watch [directory]`
Continuous monitoring mode that watches for file changes and scans in real-time.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" watch [directory]
```

**What it does:**
1. Validates Pro+ license
2. Watches the directory for file changes using filesystem events
3. Automatically scans changed files for i18n issues
4. Reports new issues as they are introduced
5. Runs until interrupted (Ctrl+C)

#### `i18ncheck ci [directory]`
CI/CD integration mode with strict exit codes and machine-parseable output.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" ci [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan with all patterns
3. Exit code 0 = clean (score >= 70), exit code 1 = issues found
4. Output is formatted for CI log parsing
5. Supports severity threshold configuration

### Team Tier ($39/user/month -- requires I18NCHECK_LICENSE_KEY with team tier)

#### `i18ncheck team-report [directory]`
Generate aggregate team i18n metrics and trend reports.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" team-report [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans directory with all patterns
3. Generates team-level metrics: top issues by category, worst files, trends
4. Produces a comprehensive markdown report for team leads
5. Includes remediation priority matrix

#### `i18ncheck baseline [directory]`
Establish a baseline of known i18n issues for incremental improvement tracking.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" baseline [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans directory and records all current findings as baseline
3. Saves baseline to .i18ncheck-baseline.json
4. Future scans only report NEW issues not in the baseline
5. Useful for legacy codebases with known i18n debt

#### `i18ncheck status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/i18ncheck.sh" status
```

## Detected Pattern Categories

I18nCheck detects 90+ i18n patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **Hardcoded Strings (HS)** | JSX/TSX hardcoded text, alert()/confirm() strings, hardcoded placeholder/label/button text, template literal UI text | Critical/High |
| **Translation Keys (TK)** | Missing t()/i18n() calls, untranslated aria-label, missing translation JSON keys, orphaned/duplicate keys, inconsistent key naming | High/Medium |
| **Date & Number Formatting (DF)** | toLocaleDateString() without locale, hardcoded MM/DD/YYYY, manual number formatting, hardcoded currency symbols, timezone-naive Date ops | High/Medium |
| **RTL & Layout (RL)** | Missing dir/lang attributes, hardcoded left/right CSS, text-align without RTL, float without logical alternatives, margin-left/right instead of inline | High/Medium |
| **String Concatenation (SC)** | Concatenated translated messages, template literal interpolation in translations, printf without i18n, word order assumptions, if/else plurals | High/Medium |
| **Encoding & Locale (EN)** | Non-UTF-8 charset, locale-dependent toLowerCase, ASCII-only regex for intl text, hardcoded locale IDs, missing Unicode normalization | Medium/Low |

## Configuration

Users can configure I18nCheck in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "i18ncheck": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "allowlistFile": ".i18ncheck-allowlist",
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
- Supports scanning JS/TS, Python, Java, Go, Ruby, and PHP in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = i18n issues detected (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hook install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://i18ncheck.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If .i18ncheck-allowlist is missing, skip allowlist filtering gracefully

## When to Use I18nCheck

The user might say things like:
- "Scan my code for i18n issues"
- "Find hardcoded strings in my project"
- "Check for internationalization problems"
- "Are there untranslated strings in my app?"
- "Scan for localization issues"
- "Check RTL layout support"
- "Find date formatting issues for i18n"
- "Detect locale-sensitive code"
- "Check if my app is ready for localization"
- "Find string concatenation in translations"
- "Scan for non-UTF-8 encoding issues"
- "Check for missing lang attributes"
- "Find timezone-naive datetime usage"
- "Run an i18n audit on my codebase"
- "Set up pre-commit hooks for i18n checks"
- "Generate an i18n readiness report"
- "Baseline existing i18n issues in my legacy project"
