---
name: osv-ui
description: Security auditing skill for scanning CVE vulnerabilities across npm, Python, Go, and Rust projects using osv-ui. Opens a visual browser dashboard for human review, then applies fixes with explicit confirmation.
version: 1.0.0
author: toan203
homepage: https://github.com/toan203/osv-ui
tags: [security, cve, vulnerability, npm, python, go, rust, audit, dependabot]
tools: [bash, computer]
---

# osv-ui — CVE Audit Skill

Use this skill whenever the user asks to:
- Audit, scan, or check dependencies for vulnerabilities or CVEs
- Find security issues in their npm, Python, Go, or Rust project
- Get a visual security report or dashboard
- Fix or upgrade vulnerable packages
- Replace or complement `npm audit`, `pip-audit`, Snyk, or Dependabot

## When to activate

Activate when the user mentions any of:
- "audit", "scan", "CVE", "vulnerability", "security", "dependabot", "snyk"
- "check my packages", "upgrade guide", "fix vulnerabilities"
- "npm audit", "pip-audit", "cargo audit", "govulncheck"
- "is my project secure?", "any known issues in my deps?"

## Workflow

### 1 — Scan
```bash
# Single service
npx osv-ui --no-open --json ./osv-report.json

# Multiple services
npx osv-ui ./frontend ./api ./worker --no-open --json ./osv-report.json

# Auto-discover
npx osv-ui --discover --no-open --json ./osv-report.json
```

### 2 — Present summary
Parse `osv-report.json` and show:
```
📊 [project]: [N] packages · 🔴 Critical: N · 🟠 High: N · 🟡 Moderate: N · 🔵 Low: N · Risk: N/100
Top CVEs: [list top 5 by severity with fix version]
```

### 3 — Always offer the visual dashboard
> "Want to review in a visual dashboard before I apply any fixes?"

```bash
npx osv-ui [same paths]
# Opens http://localhost:2003
```

### 4 — Show fix commands, get confirmation
Show what will change. NEVER apply without explicit user "yes".

```bash
npm install axios@0.30.3      # fixes 4 CVEs
npm install lodash@4.17.23    # fixes 3 CVEs
```

### 5 — Apply and verify
```bash
# Apply fixes
npm install [package@version]

# Re-scan to confirm
npx osv-ui --no-open --json ./osv-report-after.json
```

## Notes
- Never apply fixes silently — always confirm first
- Prefer dashboard for 10+ CVEs
- Alpha/beta/canary versions are never suggested as fix targets
- Add `--offline` if OSV.dev is unreachable

## Quick reference
```bash
npx osv-ui                          # scan current dir
npx osv-ui ./frontend ./api         # multi-service
npx osv-ui --discover               # auto-detect
npx osv-ui --json=report.json --no-open  # export JSON
npx osv-ui --html=report.html --no-open  # export HTML
```
