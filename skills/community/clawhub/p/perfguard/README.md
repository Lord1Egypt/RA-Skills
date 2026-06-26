# perfguard

<p align="center">
  <img src="https://img.shields.io/badge/checks-40+-blue" alt="40+ performance checks">
  <img src="https://img.shields.io/badge/languages-4-purple" alt="4 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find your N+1 queries before your users do.</h3>

<p align="center">
  <a href="https://perfguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#what-it-catches">Anti-Patterns</a> &middot;
  <a href="https://perfguard.pages.dev/#pricing">Pricing</a>
</p>

---

## Your code is slow. You just don't know where yet.

An `await` inside a `for` loop. A Django queryset without `select_related()`. A `SELECT *` on a table with 40 columns. A `readFileSync` buried in an Express handler. A `JSON.parse(JSON.stringify())` deep clone running on every request.

These are the anti-patterns that don't show up in unit tests but destroy your p99 latency. APM tools find them after your users complain. By then the damage is done.

**PerfGuard scans your code for 40+ performance anti-patterns across 4 languages. Locally. Before you commit.**

## Quick Start

```bash
# Install via ClawHub (free)
clawhub install perfguard

# Scan your codebase
perfguard scan

# Scan a specific directory
perfguard scan src/

# Scan a single file
perfguard scan app/models/orders.py

# Install pre-commit hooks (Pro)
perfguard hooks install

# Generate a performance report (Pro)
perfguard report

# Find performance hotspots (Pro)
perfguard hotspots

# Check performance budgets (Team)
perfguard budget

# Show performance trends (Team)
perfguard trend
```

## What It Catches

PerfGuard runs 40+ performance checks organized in 4 categories:

### Database / ORM

| Check | Description | Severity |
|-------|-------------|----------|
| N+1 Query | Query executed inside a loop | Critical |
| SELECT * | Fetching all columns instead of specific ones | High |
| Missing Eager Loading | No select_related/prefetch_related/includes/JOIN FETCH | Critical |
| Unbounded Query | No LIMIT or pagination on queries | High |
| Sequential Queries | Queries that could be batched | Medium |
| SQL String Concatenation | Building SQL with string interpolation | Critical |
| Missing Index Hint | Complex queries without index annotations | Medium |

### JavaScript / TypeScript

| Check | Description | Severity |
|-------|-------------|----------|
| Await in Loop | Sequential async where parallel is possible | Critical |
| Missing Promise.all | Independent awaits without batching | High |
| Sync File I/O | readFileSync/writeFileSync in server code | High |
| JSON Deep Clone | JSON.parse(JSON.stringify()) for cloning | Medium |
| Unbounded Array Ops | Large maps/forEach without chunking | Medium |
| Memory Leak | Event listeners without cleanup | High |
| Missing React Memo | Components without useMemo/useCallback | Medium |
| Full Lodash Import | `import _ from 'lodash'` instead of submodules | High |
| Missing Pagination | API endpoints without paginated responses | High |
| Console in Production | console.log left in production code | Low |

### Python

| Check | Description | Severity |
|-------|-------------|----------|
| Heavy Import in Function | Importing heavy modules at call time | Medium |
| List vs Generator | List comprehensions that should be generators | Medium |
| String Concat in Loop | Using += in loops instead of join | Medium |
| Sleep in Async | time.sleep() blocking the event loop | Critical |
| Missing Connection Pool | Direct DB connections without pooling | High |
| Sync I/O in Async | Blocking I/O in async functions | High |
| Full File Load | Reading entire files into memory | Medium |
| Regex in Loop | Compiling regex patterns inside loops | Medium |

### General

| Check | Description | Severity |
|-------|-------------|----------|
| Unbounded Retry | Retries without exponential backoff | High |
| Missing Timeout | HTTP requests without timeout | High |
| Polling Pattern | Polling instead of webhooks/events | Medium |
| Hardcoded Delay | Hardcoded sleep/delay values | Low |
| Missing Cache | Repeated computation without caching | Medium |
| No Memoization | Recursive functions without memoization | Medium |
| Large Payload | Serialization without streaming | Medium |

## Supported Languages & Frameworks

| Language | Frameworks | Database Checks | Async Checks | Memory Checks |
|----------|-----------|-----------------|--------------|---------------|
| **Python** | Django, Flask, FastAPI, SQLAlchemy | select_related, prefetch_related, N+1 | asyncio, aiohttp | generators, pooling |
| **JavaScript/TypeScript** | Node.js, Express, React, Next.js | Sequelize, Prisma, TypeORM | Promise.all, await loops | event listeners, useMemo |
| **Ruby** | Rails, ActiveRecord | includes, eager_load, N+1 | -- | -- |
| **Java** | Spring, JPA, Hibernate | JOIN FETCH, @BatchSize, N+1 | -- | -- |

## How It Compares

| Feature | PerfGuard | Datadog APM ($31/host/mo) | New Relic ($0.30/GB) | Lighthouse CI ($0 limited) | SonarQube ($150/mo) |
|---------|:---------:|:-------------------------:|:--------------------:|:--------------------------:|:-------------------:|
| Local-only (no cloud) | Yes | No | No | Yes | Self-hosted |
| Zero config setup | Yes | No | No | Yes | No |
| Pre-commit hooks | Yes | No | No | No | Yes |
| N+1 query detection | Yes | Runtime only | Runtime only | No | No |
| ORM anti-patterns | Yes | No | No | No | Limited |
| Async anti-patterns | Yes | No | No | No | Limited |
| Memory leak detection | Yes | Runtime only | Runtime only | No | No |
| Performance scoring | Yes | Yes | Yes | Yes | Yes |
| Trend tracking | Yes | Yes | Yes | Yes | No |
| No code upload required | Yes | No | No | Yes | Self-hosted |
| Zero telemetry | Yes | No | No | No | Self-hosted |
| ClawHub integration | Yes | No | No | No | No |
| Setup time | 30 seconds | 60+ minutes | 30+ minutes | 15+ minutes | 60+ minutes |
| Price (individual) | Free/$19/mo | $31/host/mo | $0.30/GB | Free (limited) | $150/mo |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| Performance scan (40+ checks) | 5 files | Unlimited | Unlimited |
| 4 language support | Yes | Yes | Yes |
| Performance score + grade | Yes | Yes | Yes |
| Detailed remediation advice | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Performance audit report | | Yes | Yes |
| Hot path identification | | Yes | Yes |
| Performance budgets | | | Yes |
| Trend tracking | | | Yes |

## Commands

### Free Tier (no license required)

| Command | Description |
|---------|-------------|
| `perfguard scan [target]` | Performance scan (up to 5 source files) |
| `perfguard status` | Show license and config info |
| `perfguard help` | Show help |

### Pro Tier ($19/user/month)

| Command | Description |
|---------|-------------|
| `perfguard scan [target]` | Unlimited source file scanning |
| `perfguard hooks install` | Install pre-commit performance hooks |
| `perfguard hooks uninstall` | Remove PerfGuard hooks |
| `perfguard report [dir]` | Generate markdown performance report |
| `perfguard hotspots [dir]` | Identify performance hot paths |

### Team Tier ($39/user/month)

| Command | Description |
|---------|-------------|
| `perfguard budget [dir]` | Check against performance budgets |
| `perfguard trend [dir]` | Performance trend over git history |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "perfguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "excludePatterns": ["**/node_modules/**", "**/dist/**"],
          "reportFormat": "markdown",
          "budgets": {
            "maxCritical": 0,
            "maxTotal": 20,
            "minScore": 70
          }
        }
      }
    }
  }
}
```

Or set the environment variable:

```bash
export PERFGUARD_LICENSE_KEY="your-key-here"
```

## Exit Codes

- `0` -- Clean (score >= 70, no critical issues)
- `1` -- Issues found (score < 70 or critical issues present)

Perfect for CI/CD integration.

## Privacy

- 100% local -- no code or data sent externally
- Zero telemetry
- Offline license validation (JWT-based)
- Pattern matching only -- no AST parsing or code execution

## Part of the ClawHub Ecosystem

PerfGuard is built for [ClawHub](https://openclaw.dev), the marketplace for developer tools that plug into your CLI. Other skills in the ecosystem:

- **[DocSync](https://docsync-1q4.pages.dev)** -- Keep docs in sync with code
- **[DepGuard](https://depguard.pages.dev)** -- Dependency audit and vulnerability scanning
- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[APIShield](https://apishield.pages.dev)** -- API endpoint security auditor
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checks

## License

MIT
