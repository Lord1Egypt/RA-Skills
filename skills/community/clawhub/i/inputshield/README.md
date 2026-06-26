# inputshield

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90-blue" alt="90 patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/license-COMMERCIAL-orange" alt="Commercial License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the input validation holes your code is hiding. Fix them before attackers exploit them.</h3>

<p align="center">
  <a href="https://inputshield.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#detection-categories">Categories</a> &middot;
  <a href="https://inputshield.pages.dev/#pricing">Pricing</a>
</p>

---

## Your code trusts user input. It should not.

Missing input validation is the root cause of most security vulnerabilities. Command injection through unsanitized shell arguments. Path traversal via unchecked file paths. XSS from raw HTML interpolation. ReDoS from unbounded regex quantifiers. Unsafe deserialization of untrusted data. Every unvalidated input is a door left open.

OWASP consistently ranks injection flaws and input validation failures among the top 10 web application risks. A single unvalidated input can lead to remote code execution, data exfiltration, or denial of service.

**InputShield finds the gaps before they become exploits.** 90 detection patterns across 6 vulnerability categories. Pre-commit hooks. Local scanning. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free tier -- 30 patterns)
clawhub install inputshield

# 2. Scan your repo
inputshield scan

# 3. Scan with specific category
inputshield scan --category CI   # Command injection only

# 4. Install pre-commit hooks (Pro)
inputshield hooks install
```

That is it. Every commit is now scanned for input validation vulnerabilities before it lands.

## What It Does

### Scan files for input validation vulnerabilities
One command to scan any file, directory, or your entire repo. 90 regex patterns detect missing validation, unsafe deserialization, ReDoS, path traversal, command injection, and XSS across all major languages.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If critical or high-severity input validation issues are detected, the commit is blocked with a clear remediation message.

### Generate input validation reports
Produce markdown reports with severity breakdowns, vulnerability categories, and remediation priority. Ideal for security reviews and compliance audits.

### Category-focused scanning
Target specific vulnerability classes with `--category`. Scan only for command injection, only for XSS, or only for ReDoS -- useful when remediating specific vulnerability classes.

### Multiple output formats
Get results in colorized terminal text, structured JSON for CI/CD pipelines, or HTML reports for stakeholder review.

## Detection Categories

InputShield detects 90 vulnerability patterns across 6 categories:

### Input Validation (IV) -- 15 patterns

Missing length checks, absent type validation, raw user input acceptance, missing allowlist validation, missing boundary checks, unvalidated numeric input, unvalidated array indices, missing null/undefined checks, unchecked string formats (email, URL), missing enum validation, no Content-Type validation, absent schema validation, unvalidated query parameters, missing rate limit checks, and unvalidated redirect URLs.

### Deserialization (DS) -- 15 patterns

Unsafe JSON.parse without try-catch, Python pickle.loads on untrusted data, yaml.load without SafeLoader, Java ObjectInputStream from untrusted sources, PHP unserialize of user input, Ruby Marshal.load without filtering, .NET BinaryFormatter deserialization, Java XMLDecoder usage, unvalidated XML external entity parsing, messagepack/protobuf without schema validation, unsafe object spread from external data, unvalidated BSON deserialization, Java readObject without validation, Go gob.Decode from untrusted sources, and unsafe CBOR decoding.

### ReDoS (RD) -- 15 patterns

Nested quantifiers like (a+)+, overlapping alternations like (a|a)*, star-of-star patterns, catastrophic backtracking with optional groups, exponential patterns with nested repetition, unbounded repetition in alternations, grouping with interleaved quantifiers, quantified backreferences, nested character classes with quantifiers, recursive group quantifiers, overlapping character classes under repetition, non-atomic groups with quantifiers, unbounded lazy quantifiers in nested groups, alternation-within-repetition patterns, and quantified lookahead/lookbehind structures.

### Path Traversal (PT) -- 15 patterns

Direct ../ injection in file paths, unsanitized path concatenation, open() with user-controlled paths, file upload without name sanitization, user-controlled require/import paths, symlink-following file access, path.join with user input, URL-encoded path traversal (%2e%2e), file inclusion via user parameter, user-controlled directory listings, archive extraction without path validation (zip slip), template file inclusion with user input, user-controlled log file paths, dynamic file serving from user paths, and null byte injection in file paths.

### Command Injection (CI) -- 15 patterns

Shell exec/system with concatenated user input, eval() on user-provided strings, child_process.exec with variables, Python os.system/os.popen with user data, subprocess with shell=True, PHP exec/passthru/system, Ruby backtick/system execution, template injection via user-controlled templates, SQL query string concatenation, LDAP query injection, SSI (Server-Side Include) injection, Header injection via user input, expression language injection, unsafe reflection from user input, and OS command via Runtime.exec with user data.

### XSS / Output Encoding (XS) -- 15 patterns

innerHTML assignment with user data, dangerouslySetInnerHTML with variables, document.write with user-controlled strings, unescaped template interpolation, jQuery .html() with user data, v-html directive with dynamic content, React ref.current.innerHTML, missing Content-Security-Policy, direct DOM manipulation with user strings, server-side template rendering without encoding, response.write with unescaped user data, JSONP callback with user-controlled function name, SVG injection via user content, CSS injection through style attributes, and open redirect via unvalidated URL.

## Scoring

InputShield calculates an **Input Safety Score** from 0 to 100:

| Severity | Points Deducted |
|----------|----------------|
| Critical | 25 |
| High | 15 |
| Medium | 8 |
| Low | 3 |

| Grade | Score Range | Pass/Fail |
|-------|------------|-----------|
| A | 90-100 | Pass |
| B | 80-89 | Pass |
| C | 70-79 | Pass (threshold) |
| D | 60-69 | Fail |
| F | 0-59 | Fail |

Pass threshold is 70. Exit code 0 for pass, 1 for fail.

## Pricing

| Feature | Free | Pro ($19/mo) | Team ($39/mo) | Enterprise |
|---------|:----:|:------------:|:-------------:|:----------:|
| Patterns | 30 | 60 | 90 (all) | 90 (all) |
| Per category | 5 | 10 | 15 | 15 |
| One-shot scan | Yes | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes | Yes |
| Reports | | Yes | Yes | Yes |
| Category filtering | | | Yes | Yes |
| JSON/HTML output | | | Yes | Yes |
| Verbose audit mode | | | Yes | Yes |
| CI/CD integration | | | Yes | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "inputshield": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
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

Or set the environment variable:

```bash
export INPUTSHIELD_LICENSE_KEY="your_jwt_token_here"
```

## CLI Reference

```
inputshield <command> [options]

Commands:
  scan [file|dir]    Run input validation scan
  hooks install      Install pre-commit hooks (Pro+)
  hooks uninstall    Remove InputShield hooks (Pro+)
  report [dir]       Generate markdown report (Pro+)
  audit [dir]        Deep audit with verbose output (Team+)
  status             Show license and config info
  patterns           List all detection patterns

Options:
  --path <path>       Target file or directory (default: .)
  --format <fmt>      Output format: text, json, html (default: text)
  --tier <tier>       License tier: free, pro, team, enterprise
  --license-key <k>   License key (or set INPUTSHIELD_LICENSE_KEY)
  --category <cat>    Filter by category: IV, DS, RD, PT, CI, XS
  --verbose           Enable verbose output
  --help, -h          Show help
  --version, -v       Show version
```

## How It Compares

| Feature | InputShield | ESLint Security | Semgrep | Snyk Code | SonarQube |
|---------|:-----------:|:---------------:|:-------:|:---------:|:---------:|
| 90 input-focused patterns | Yes | ~20 | Varies | Varies | Varies |
| ReDoS detection | Yes | Partial | Yes | Yes | Yes |
| Path traversal detection | Yes | No | Yes | Yes | Yes |
| Command injection | Yes | Partial | Yes | Yes | Yes |
| XSS detection | Yes | Yes | Yes | Yes | Yes |
| Deserialization checks | Yes | No | Yes | Yes | Yes |
| Zero config scan | Yes | Config required | Rules required | Cloud required | Server required |
| Offline license | Yes | N/A | N/A | Cloud | Server |
| Local-only (no cloud) | Yes | Yes | Optional | No | Optional |
| Zero telemetry | Yes | Yes | Optional | No | Optional |
| No binary deps | Yes | Node.js | Python | Cloud | Java |
| Score and grades | Yes | No | No | No | Yes |
| Price (individual) | Free/$19/mo | Free | Free/$40/mo | Free/$25/mo | Free/$15/mo |

## Ecosystem

InputShield is part of the ClawHub code quality suite:

- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets and credential leak detection
- **[InputShield](https://inputshield.pages.dev)** -- Input validation and sanitization scanning
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[SQLGuard](https://sqlguard.pages.dev)** -- SQL injection detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[EnvGuard](https://envguard.pages.dev)** -- Environment variable security
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[StyleGuard](https://styleguard.pages.dev)** -- Code style enforcement
- **[TestGap](https://testgap.pages.dev)** -- Test coverage gap detection
- **[DocCoverage](https://doccoverage.pages.dev)** -- Documentation coverage analysis

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation (JWT-based)
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- No data collection, no analytics, no tracking

## Contributing

InputShield is a commercial ClawHub skill. For bug reports, feature requests, or pattern contributions:

1. Open an issue at the ClawHub skill repository
2. Include the check ID (e.g., CI-003) and a minimal reproduction case
3. For new pattern suggestions, provide the regex, a severity recommendation, and test cases

## License

Commercial -- see [LICENSE](https://inputshield.pages.dev/license) for details.
Free tier available with 30 patterns (5 per category).
