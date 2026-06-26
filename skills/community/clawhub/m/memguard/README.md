# memguard

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90+-blue" alt="90+ patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/languages-6-orange" alt="6 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the memory leaks your code is hiding. Fix them before production does.</h3>

<p align="center">
  <a href="https://memguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#detection-categories">Categories</a> &middot;
  <a href="https://memguard.pages.dev/#pricing">Pricing</a>
</p>

---

## Your code leaks resources. Silently.

Memory leaks are the silent killers of production systems. An unclosed file handle in a hot path. An event listener added on every render. A cache that grows forever. A setInterval that outlives its component. A database connection pool drained by forgotten releases. A useEffect without a cleanup return.

These issues don't crash your app immediately. They degrade it slowly -- increasing memory consumption, exhausting file descriptors, starving connection pools -- until your 3am pager goes off.

**MemGuard finds the leaks before they reach production.** Pre-commit hooks. Local scanning. 90+ patterns across 6 resource lifecycle categories. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install memguard

# 2. Scan your repo
memguard scan

# 3. Install pre-commit hooks
memguard hook install
```

That's it. Every commit is now scanned for resource leaks before it lands.

## What It Does

### Scan files for resource leaks
One command to scan any file, directory, or your entire repo. 90+ regex patterns detect leaks across file handles, event listeners, circular references, unbounded caches, React cleanup, and timers/streams.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If resource leaks are detected, the commit is blocked with a clear remediation message.

### Generate resource health reports
Produce markdown reports with severity breakdowns, leak categories, and remediation priority. Ideal for code reviews and tech debt tracking.

### Continuous watch mode
Monitor your codebase in real-time during development. As files change, MemGuard re-scans and reports new issues immediately.

### CI/CD integration
Run MemGuard in your CI pipeline with structured exit codes. Block merges that introduce new resource leaks.

### Baseline tracking
Record existing leaks in legacy codebases so future scans only report new issues. Track improvement over time with team reports.

## How It Compares

| Feature | MemGuard | ESLint ($0) | SonarQube ($0+) | PMD ($0) | Semgrep ($0+) |
|---------|:--------:|:-----------:|:---------------:|:--------:|:-------------:|
| 90+ resource patterns | Yes | ~5 | ~20 | ~10 | ~15 |
| Multi-language (6) | Yes | JS/TS only | Yes | Java only | Yes |
| File handle detection | Yes | No | Partial | Partial | Partial |
| Event listener leaks | Yes | Partial | No | No | Partial |
| Circular reference detection | Yes | No | No | No | Partial |
| Unbounded cache detection | Yes | No | No | No | No |
| React useEffect cleanup | Yes | Partial | No | No | Partial |
| Timer/stream leaks | Yes | Partial | Partial | No | Partial |
| Pre-commit hooks | Yes | Via config | No | No | Yes |
| Score & grades | Yes | No | Yes | No | No |
| Baseline tracking | Yes | No | Yes | No | No |
| Zero config scan | Yes | Config required | Config required | Config required | Config required |
| No binary deps | Yes | Node.js | Java | Java | Python |
| Zero telemetry | Yes | Yes | No | Yes | No |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free/$15/mo | Free | Free/$40/mo |

## Detection Categories

MemGuard detects 90+ resource lifecycle patterns across 6 categories:

### File Handles (FH-001 to FH-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| FH-001 | Critical | Python | open() without close() or context manager |
| FH-002 | Critical | Java | FileInputStream/FileOutputStream without close |
| FH-003 | High | JS/TS | fs.open/fs.createReadStream without close |
| FH-004 | High | Python | Database cursor not closed |
| FH-005 | High | Java | JDBC Connection/Statement not closed |
| FH-006 | High | C# | FileStream/StreamReader without using/Dispose |
| FH-007 | High | Go | os.Open without defer Close |
| FH-008 | Medium | Python | tempfile creation without cleanup |
| FH-009 | High | Java | BufferedReader/Writer without close |
| FH-010 | High | All | Database connection opened without close pattern |

### Event Listeners (EL-001 to EL-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| EL-001 | High | JS/TS | addEventListener without removeEventListener |
| EL-002 | High | JS/TS | .on() without corresponding .off() |
| EL-003 | High | JS/TS | window/document event listener never removed |
| EL-004 | Medium | Python | signal.connect without disconnect |
| EL-005 | High | JS/TS | EventEmitter listener without removal |
| EL-006 | Medium | Java | addListener/addObserver without remove |

### Circular References (CR-001 to CR-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| CR-001 | High | JS/TS | this.parent = parent; parent.child = this |
| CR-002 | Medium | Python | Mutual class attribute references |
| CR-003 | Medium | JS/TS | Closure capturing outer scope reference |
| CR-004 | High | All | Self-referencing object pattern |
| CR-005 | Medium | JS/TS | Map/Set storing objects with back-references |

### Unbounded Caches (UC-001 to UC-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| UC-001 | High | JS/TS | new Map() at module level without cleanup |
| UC-002 | High | Python | Global dict used as cache without eviction |
| UC-003 | Medium | All | In-memory cache without TTL/max size |
| UC-004 | High | JS/TS | Array.push in loop without bounds |
| UC-005 | Medium | All | Memoization without cache size limit |

### React Cleanup (RC-001 to RC-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| RC-001 | High | JS/TS | useEffect without cleanup return |
| RC-002 | Critical | JS/TS | setInterval in useEffect without clearInterval |
| RC-003 | High | JS/TS | subscribe in useEffect without unsubscribe |
| RC-004 | High | JS/TS | addEventListener in useEffect without remove |
| RC-005 | Medium | JS/TS | State update pattern without mounted check |

### Timers & Streams (TM-001 to TM-015)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| TM-001 | Critical | JS/TS | setInterval without clearInterval |
| TM-002 | High | JS/TS | setTimeout in loop without cleanup |
| TM-003 | High | JS/TS/Python | Stream pipe without error handling |
| TM-004 | High | Go | goroutine without done channel or context |
| TM-005 | High | JS/TS | WebSocket opened without close handler |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot resource scan | 5 files | Unlimited | Unlimited |
| 90+ detection patterns | Yes | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes |
| Resource health reports | Yes | Yes | Yes |
| Watch mode (live) | | Yes | Yes |
| CI/CD integration | | Yes | Yes |
| Baseline tracking | | | Yes |
| Team aggregate reports | | | Yes |
| Trend analysis | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "memguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
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

## Ecosystem

MemGuard is part of the ClawHub code quality suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[TypeDrift](https://typedrift.pages.dev)** -- Type safety drift detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[DocSync](https://docsync.pages.dev)** -- Documentation drift detection
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checking
- **[LicenseGuard](https://licenseguard.pages.dev)** -- License compliance scanning
- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets & credential leak detection
- **[MemGuard](https://memguard.pages.dev)** -- Memory leak & resource management scanning

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies beyond bash

## License

MIT
