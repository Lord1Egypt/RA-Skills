# VibeSafe Starter — Your First Security Pack

> **3 files. 2 minutes. No more "it works on my machine" disasters.**

You vibe-code with AI agents. Cool. But here's what AI won't tell you: **67% of npm packages used in AI-generated projects have known vulnerabilities.** The AI doesn't check. It just imports.

This starter pack catches the obvious stuff before it catches you.

## What You're Risking (Right Now)

Every time an AI agent writes `npm install` or `pip install` without checking:

| Risk | Reality |
|------|---------|
| **Known CVEs** | Public vulnerabilities that attackers already exploit |
| **Abandoned packages** | Last updated in 2022. No fixes coming. |
| **Credential leaks** | `.env` files committed to git. API keys in code. |
| **Supply chain attacks** | Malicious packages that look legitimate |
| **Unmaintained dependencies** | 47% of npm packages have no active maintainer |

**One vulnerable dependency → your entire project is compromised.**

## The Fix (3 Files)

### 1. `.github/workflows/security.yml`
Drop this into any repo. Runs on every push.

### 2. `audit.sh`
Run before `npm install`. Catches critical CVEs.

### 3. `checklib.sh`
Check a library before adding it to your project.

---

## Quick Start

```bash
# Clone into your project
git clone https://github.com/nerua1/vibe-safe-starter.git
cp vibe-safe-starter/.github/workflows/security.yml .github/workflows/
cp vibe-safe-starter/audit.sh .
cp vibe-safe-starter/checklib.sh .
chmod +x audit.sh checklib.sh

# Check a library before installing
./checklib.sh react
./checklib.sh flask

# Audit your dependencies
./audit.sh
```

---

## The Numbers

- **67%** of AI-suggested npm packages have known vulnerabilities
- **47%** of npm packages are unmaintained
- **1 in 10** GitHub repos leak credentials
- **Average CVE goes undetected for 208 days** before disclosure

Your AI agent will happily install all of them. This pack won't.

---

## Extend It

This is the minimum. If you want more:

| Need | Solution |
|------|----------|
| VS Code integration | [VibeSafe Extension](https://github.com/nerua1/vibe-safe) |
| AI-powered risk explanation | [VibeSafe AI Explain](https://github.com/nerua1/vibe-safe/tree/main/tools) |
| Multi-agent HARNESS | [VibeSafe HARNESS §14](https://github.com/nerua1/vibe-safe/tree/main/harness) |
| Full audit pipeline | [VibeSafe Full](https://github.com/nerua1/vibe-safe) |
| Dashboard | `vibe-safe/tools/dashboard.py --html` |

---

## Philosophy

- **80/20 rule**: Catch 80% of risks with 20% of effort
- **Non-blocking**: Suggests, doesn't block your flow
- **Zero config**: Drop in, works immediately
- **Minimal**: 3 files. No frameworks. No databases.

---

*Built by [nerua1](https://github.com/nerua1). ⭐ Star if this saves you from a security incident.*

☕ [PayPal.me/nerudek](https://www.paypal.me/nerudek)
