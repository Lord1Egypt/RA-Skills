# i18ncheck

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90+-blue" alt="90+ patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
  <img src="https://img.shields.io/badge/languages-JS%2FTS%20%7C%20Python%20%7C%20Java%20%7C%20Go%20%7C%20Ruby%20%7C%20PHP-orange" alt="Multi-language">
</p>

<h3 align="center">Find the i18n issues hiding in your codebase. Ship to every locale with confidence.</h3>

<p align="center">
  <a href="https://i18ncheck.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#detection-categories">Categories</a> &middot;
  <a href="https://i18ncheck.pages.dev/#pricing">Pricing</a>
</p>

---

## Your codebase is not ready for localization.

Hardcoded strings in JSX components. Date formatting that assumes MM/DD/YYYY. CSS that breaks in RTL languages. String concatenation that makes translation impossible. Missing lang attributes. Timezone-naive datetime operations. ASCII-only regex patterns that reject international names.

These issues are invisible until you try to ship in Arabic, Japanese, or German. By then, it costs 10x more to fix. Translation vendors charge per-word for context they do not have. RTL layout bugs take days to track down. Pluralization rules differ across every language.

**I18nCheck finds every internationalization issue before localization begins.** Pre-commit hooks. Local scanning. 90+ patterns across 6 detection categories. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install i18ncheck

# 2. Scan your repo
i18ncheck scan

# 3. Install pre-commit hooks (free)
i18ncheck hook install
```

That is it. Every commit is now scanned for i18n issues before it lands.

## What It Does

### Scan files for internationalization issues
One command to scan any file, directory, or your entire repo. 90+ regex patterns detect i18n anti-patterns across hardcoded strings, missing translations, date/number formatting, RTL layout, string concatenation, and encoding issues.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If i18n issues are detected, the commit is blocked with a clear remediation message showing exactly what to fix.

### Generate i18n readiness reports
Produce markdown reports with severity breakdowns, i18n categories, and remediation priority. Ideal for localization planning and i18n audits.

### Continuous monitoring (Pro)
Watch mode monitors file changes in real-time and reports new i18n issues as they are introduced. Never let hardcoded strings slip through again.

### CI/CD integration (Pro)
Add i18n checks to your CI pipeline with strict exit codes and machine-parseable output. Fail builds that introduce new i18n regressions.

### Baseline known issues (Team)
Record existing i18n issues in legacy codebases so future scans only report new regressions. Track incremental improvement over time.

## How It Compares

| Feature | I18nCheck | i18n-lint ($0) | eslint-plugin-i18n ($0) | i18next-scanner ($0) | FormatJS ($0) |
|---------|:---------:|:--------------:|:-----------------------:|:--------------------:|:-------------:|
| 90+ patterns | Yes | ~15 | ~10 | ~5 | ~8 |
| Multi-language (6 langs) | Yes | JS only | JS only | JS only | JS only |
| RTL layout detection | Yes | No | No | No | No |
| Date/number formatting | Yes | No | No | No | Partial |
| Encoding issues | Yes | No | No | No | No |
| String concatenation | Yes | Partial | Partial | No | No |
| Pre-commit hooks | Yes | No | Yes | No | No |
| Baseline/allowlist | Yes | No | No | No | No |
| Zero config scan | Yes | Config required | Config required | Config required | Config required |
| Offline license | Yes | N/A | N/A | N/A | N/A |
| Local-only (no cloud) | Yes | Yes | Yes | Yes | Yes |
| Zero telemetry | Yes | Yes | Yes | Yes | Yes |
| No binary deps | Yes | Node.js | Node.js | Node.js | Node.js |
| Score & grades | Yes | No | No | No | No |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free | Free | Free |

## Detection Categories

I18nCheck detects 90+ i18n patterns across 6 categories:

### Hardcoded Strings -- HS (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| HS-001 | Critical | Hardcoded text content in JSX/TSX elements |
| HS-002 | Critical | Hardcoded string in alert()/confirm()/prompt() calls |
| HS-003 | High | Hardcoded placeholder attribute text |
| HS-004 | High | Hardcoded title attribute text |
| HS-005 | High | Hardcoded button/submit value text |
| HS-006 | High | Hardcoded label text in HTML/JSX |
| HS-007 | High | Hardcoded error message strings in UI code |
| HS-008 | Medium | Hardcoded tooltip/popover text |
| HS-009 | High | Hardcoded option text in select elements |
| HS-010 | High | Hardcoded heading text (h1-h6) |
| HS-011 | Medium | Hardcoded paragraph text content |
| HS-012 | High | Hardcoded string in document.title assignment |
| HS-013 | Medium | Hardcoded text in console-facing user messages |
| HS-014 | High | Hardcoded strings in Python/Ruby/Java UI frameworks |
| HS-015 | Medium | Hardcoded notification/toast message text |

### Translation Keys -- TK (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| TK-001 | High | String literal missing t()/i18n() wrapper |
| TK-002 | High | Untranslated aria-label attribute value |
| TK-003 | High | Untranslated aria-placeholder attribute |
| TK-004 | Medium | Missing translation key in JSON locale file |
| TK-005 | Medium | Duplicate translation key in locale file |
| TK-006 | Medium | Inconsistent translation key naming convention |
| TK-007 | High | Raw string passed to component prop expecting translation |
| TK-008 | Medium | Translation key exists in source but not in locale file |
| TK-009 | Medium | Hardcoded string in gettext/ngettext call |
| TK-010 | High | Missing i18n import in file with UI strings |
| TK-011 | Medium | Translation function called with empty string |
| TK-012 | High | Untranslated alt text on images |
| TK-013 | Medium | Hardcoded strings in validation messages |
| TK-014 | High | Untranslated content in meta tags |
| TK-015 | Medium | Missing translation for enum/constant display values |

### Date & Number Formatting -- DF (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| DF-001 | High | toLocaleDateString() without explicit locale parameter |
| DF-002 | High | Hardcoded date format string (MM/DD/YYYY, DD.MM.YYYY) |
| DF-003 | High | Manual number formatting instead of Intl.NumberFormat |
| DF-004 | High | Hardcoded currency symbol ($, EUR, GBP) in display |
| DF-005 | Medium | Locale-dependent parseFloat/parseInt usage |
| DF-006 | High | Timezone-naive Date constructor or new Date() |
| DF-007 | Medium | Hardcoded decimal separator (period or comma) |
| DF-008 | High | strftime/strptime without locale awareness |
| DF-009 | Medium | Hardcoded thousand separator in number display |
| DF-010 | High | SimpleDateFormat without explicit Locale (Java) |
| DF-011 | Medium | time.Format with hardcoded US layout (Go) |
| DF-012 | High | Date.parse() with locale-dependent string |
| DF-013 | Medium | Hardcoded time format (AM/PM assumption) |
| DF-014 | Medium | Number.toFixed() for currency display |
| DF-015 | High | moment() without locale configuration |

### RTL & Layout -- RL (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| RL-001 | High | Missing dir attribute on html element |
| RL-002 | High | Hardcoded text-align: left without RTL consideration |
| RL-003 | High | Hardcoded text-align: right without RTL consideration |
| RL-004 | Medium | float: left without logical alternative |
| RL-005 | Medium | float: right without logical alternative |
| RL-006 | High | margin-left/margin-right instead of margin-inline |
| RL-007 | High | padding-left/padding-right instead of padding-inline |
| RL-008 | Medium | border-left/border-right instead of border-inline |
| RL-009 | High | Missing lang attribute on html element |
| RL-010 | Medium | left/right in CSS position without logical properties |
| RL-011 | Medium | Hardcoded text direction (ltr) in CSS |
| RL-012 | High | text-indent with fixed direction assumption |
| RL-013 | Medium | CSS transform with directional translate |
| RL-014 | High | Directional icon/arrow without RTL flip |
| RL-015 | Medium | CSS grid/flex with directional assumptions |

### String Concatenation -- SC (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| SC-001 | Critical | String concatenation in translated message |
| SC-002 | High | Template literal interpolation in translation call |
| SC-003 | High | Printf-style format string without i18n library |
| SC-004 | Critical | Word order assumption in concatenated translation |
| SC-005 | High | Plural handling with simple if/else |
| SC-006 | High | Gender assumption in string construction |
| SC-007 | Medium | Number-to-string concatenation for display |
| SC-008 | High | Conditional string building for UI messages |
| SC-009 | Medium | Array join for sentence construction |
| SC-010 | High | String replace for dynamic translation values |
| SC-011 | Critical | Sentence fragments concatenated across variables |
| SC-012 | Medium | Ordinal number formatting without i18n |
| SC-013 | High | Possessive form with apostrophe-s assumption |
| SC-014 | Medium | List formatting without Intl.ListFormat |
| SC-015 | High | Relative time expressed via string concatenation |

### Encoding & Locale -- EN (15 patterns)

| Check ID | Severity | Description |
|----------|----------|-------------|
| EN-001 | High | Non-UTF-8 charset declaration in HTML |
| EN-002 | High | Locale-dependent toLowerCase/toUpperCase (Turkish I) |
| EN-003 | Medium | ASCII-only regex pattern for name/text validation |
| EN-004 | Medium | Hardcoded locale identifier string |
| EN-005 | Medium | Missing Unicode normalization before comparison |
| EN-006 | High | Byte-level string operation on multi-byte text |
| EN-007 | Medium | strcmp/strcasecmp without locale-aware collation |
| EN-008 | Medium | Hardcoded character encoding in file operations |
| EN-009 | Low | ASCII-only character class in regex validation |
| EN-010 | Medium | String.length used for display truncation (multi-byte) |
| EN-011 | Medium | Locale-dependent number comparison in sort |
| EN-012 | Low | Hardcoded thousands/decimal separators in validation |
| EN-013 | Medium | Non-locale-aware string sorting |
| EN-014 | Medium | Fixed-width assumption for character display |
| EN-015 | Low | Missing BOM handling for UTF-8 files |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot i18n scan | 5 files | Unlimited | Unlimited |
| 90+ detection patterns | Yes | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes |
| I18n readiness reports | Yes | Yes | Yes |
| Watch mode (continuous) | | Yes | Yes |
| CI/CD integration | | Yes | Yes |
| Team aggregate reports | | | Yes |
| Baseline management | | | Yes |
| Custom policy rules | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "i18ncheck": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
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

## Ecosystem

I18nCheck is part of the ClawHub code quality suite:

- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets & credential leak detection
- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[TypeDrift](https://typedrift.pages.dev)** -- Type safety drift detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[StyleGuard](https://styleguard.pages.dev)** -- Code style enforcement
- **[AccessLint](https://accesslint.pages.dev)** -- Accessibility scanning
- **[I18nCheck](https://i18ncheck.pages.dev)** -- Internationalization & localization readiness scanning

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies beyond bash

## License

MIT
