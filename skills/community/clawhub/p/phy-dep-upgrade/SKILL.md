---
name: Dep Upgrade
description: Dependency audit and upgrade planner for Node.js, Python, Rust, Go, and Ruby projects. Scans for outdated packages, vulnerability CVEs, and breaking changes, then produces a prioritized upgrade plan with exact commands. Zero external API required — works entirely from your project files and standard package manager CLIs. Triggers on "audit dependencies", "check for vulnerabilities", "upgrade packages", "outdated deps", "/dep-upgrade".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - dependencies
    - security
    - npm
    - pip
    - cargo
    - go
    - audit
    - upgrade
    - maintenance
---

# Dependency Audit & Upgrade Planner

Scan any project for outdated and vulnerable dependencies across Node.js, Python, Rust, Go, and Ruby — then produce a prioritized, actionable upgrade plan with exact commands and breaking-change warnings.

**No API keys. No external services. Works entirely from your project files and standard CLIs.**

---

## Trigger Phrases

- "audit dependencies", "check deps", "check for vulnerabilities"
- "upgrade packages", "update dependencies", "outdated packages"
- "npm audit", "pip audit", "security vulnerabilities in deps"
- "/dep-upgrade"

---

## Step 1: Detect Project Type

Scan the current directory for lockfiles and manifests to identify all project types present:

```bash
# Detect all project types in one pass
ls package.json package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null && echo "NODE"
ls requirements.txt pyproject.toml setup.py Pipfile 2>/dev/null && echo "PYTHON"
ls Cargo.toml Cargo.lock 2>/dev/null && echo "RUST"
ls go.mod go.sum 2>/dev/null && echo "GO"
ls Gemfile Gemfile.lock 2>/dev/null && echo "RUBY"
```

A project may have multiple types (e.g., Python backend + Node frontend). Run audits for all detected types.

---

## Step 2: Run Audit Commands

Run the appropriate commands for each detected type. Execute all simultaneously where possible.

### Node.js / npm / yarn / pnpm

```bash
# Security vulnerabilities (built-in)
npm audit --json 2>/dev/null || yarn audit --json 2>/dev/null

# Outdated packages
npm outdated --json 2>/dev/null || yarn outdated --json 2>/dev/null

# If pnpm
pnpm audit --json 2>/dev/null
pnpm outdated 2>/dev/null
```

### Python

```bash
# Check outdated (pip)
pip list --outdated --format=json 2>/dev/null

# Security audit (pip-audit if available, else safety)
pip-audit --format=json 2>/dev/null || \
  python3 -m pip_audit --format=json 2>/dev/null || \
  safety check --json 2>/dev/null || \
  echo "Install pip-audit: pip install pip-audit"

# Check pyproject.toml / requirements.txt exists
cat requirements.txt 2>/dev/null | head -50
cat pyproject.toml 2>/dev/null | head -30
```

### Rust

```bash
# Security audit
cargo audit 2>/dev/null || echo "Install: cargo install cargo-audit"

# Outdated
cargo outdated 2>/dev/null || echo "Install: cargo install cargo-outdated"
```

### Go

```bash
# Vulnerability check
govulncheck ./... 2>/dev/null || echo "Install: go install golang.org/x/vuln/cmd/govulncheck@latest"

# List all deps and versions
go list -m -json all 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        m = json.loads(line)
        if m.get('Update'):
            print(f\"{m['Path']}: {m['Version']} → {m['Update']['Version']}\")
    except: pass
"
```

### Ruby

```bash
# Security audit
bundle audit check --update 2>/dev/null || echo "Install: gem install bundler-audit"

# Outdated gems
bundle outdated 2>/dev/null
```

---

## Step 3: Categorize and Prioritize

After collecting all audit output, categorize every finding:

### Severity Tiers

| Tier | Criteria | Action |
|------|----------|--------|
| 🔴 **CRITICAL** | CVE with CVSS ≥ 9.0, or RCE/auth bypass | Fix immediately before any deployment |
| 🟠 **HIGH** | CVE with CVSS 7.0–8.9, or data exposure | Fix within this sprint |
| 🟡 **MEDIUM** | CVE CVSS 4.0–6.9, or major version outdated | Plan for next sprint |
| 🟢 **LOW** | Minor version outdated, no CVE | Batch update quarterly |
| ⚪ **INFO** | Dev-only dependency, outdated but no CVE | Optional |

### Breaking Change Detection

For each package flagged as outdated, check if the upgrade crosses a major version boundary:
- `1.x → 2.x` = **BREAKING** (check CHANGELOG)
- `1.2 → 1.9` = likely safe
- `0.x → 1.x` = **BREAKING** (pre-1.0 APIs are unstable)

Flag any package where current version and latest version have different major numbers.

---

## Step 4: Generate Upgrade Plan

Output a structured report with copy-pasteable commands:

```markdown
## Dependency Audit Report
Project: [detected type(s)] | Directory: [path] | Date: [today]

### Summary
| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟠 High | N |
| 🟡 Medium | N |
| 🟢 Low | N |
| Total outdated | N |

---

### 🔴 CRITICAL — Fix Immediately

**[package-name]** `1.2.3` → `1.2.9`
- CVE: CVE-2026-XXXX (CVSS 9.8) — Remote Code Execution via [description]
- Fix: `npm install package-name@1.2.9`
- Breaking changes: None (patch release)

---

### 🟠 HIGH — Fix This Sprint

**[package-name]** `2.1.0` → `3.0.1` ⚠️ MAJOR VERSION CHANGE
- CVE: CVE-2026-XXXX (CVSS 7.5) — [description]
- Fix: `npm install package-name@3.0.1`
- ⚠️ Breaking changes: Check CHANGELOG — v3.0 changes [X]
- Migration guide: [URL if findable]

---

### 🟡 MEDIUM — Next Sprint

[list]

---

### 🟢 LOW — Batch Update

Run all safe patch/minor updates at once:
\`\`\`bash
# Node: update all non-breaking
npx npm-check-updates -u --target minor && npm install

# Python: update all non-breaking
pip install --upgrade [list of safe packages]
\`\`\`

---

### Recommended Fix Order

1. [package] — Critical CVE, patch only, safe
2. [package] — High CVE, test breaking changes first
3. [package] — Medium, can batch with others
```

---

## Step 5: Quick Fix Mode

If the user says "just fix the critical ones" or "auto-fix safe updates", run:

### Node.js — fix critical + non-breaking
```bash
# Fix all audit-flagged vulns that have non-breaking fixes
npm audit fix

# Fix breaking changes only if user confirms
npm audit fix --force  # ⚠️ ask user first
```

### Python — fix critical
```bash
# Update specific vulnerable packages
pip install --upgrade [package1] [package2]
```

### Verify after fix
```bash
# Re-run audit to confirm vulns resolved
npm audit 2>/dev/null || pip-audit 2>/dev/null
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No package manager installed | Suggest install command, parse manifest file directly |
| Monorepo (multiple package.json) | `find . -name "package.json" -not -path "*/node_modules/*"` and audit each |
| Private packages | Skip CVE lookup for `@company/` scoped packages, still flag outdated versions |
| No internet / offline | Use cached `npm audit` data, note that CVE DB may be stale |
| Conflicting peer dependencies | Report conflict, suggest `--legacy-peer-deps` or manual resolution |

---

## Example Output

```
## Dependency Audit — my-app (Node.js + Python)
Date: 2026-03-18

### Summary
🔴 Critical: 1  🟠 High: 2  🟡 Medium: 4  🟢 Low: 11

---
🔴 CRITICAL

lodash 4.17.15 → 4.17.21
CVE-2021-23337 (CVSS 9.1) — Command injection via template
Fix: npm install lodash@4.17.21
Safe: patch release, no breaking changes ✅

---
🟠 HIGH

axios 0.21.1 → 1.6.8  ⚠️ MAJOR VERSION
CVE-2023-45857 (CVSS 8.8) — CSRF via forged headers
Fix: npm install axios@1.6.8
⚠️ axios v1.x changed default adapter — test HTTP calls after upgrade

---
One-liner to fix critical + high (safe patches only):
npm install lodash@4.17.21
npm install axios@1.6.8  # review breaking changes first
```

---

## Why No Competitor Exists

Most security tools (Snyk, Dependabot, Socket.dev) require:
- External API keys / account signup
- CI/CD pipeline integration
- Cloud access to your repo

This skill works **entirely locally** — reads your lockfiles, runs your package manager CLI, and gives you the full picture in one pass. No auth, no upload, no account required.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
