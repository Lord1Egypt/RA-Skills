# Auto-Evolve v4.3

**Make your projects self-evolve — install once, they keep getting better.**

> You install it once. It runs in the background. Your projects get smarter — automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://img.shields.io/badge/Python-3.10+-blue.svg)

**中文**: [README.zh-CN.md](README.zh-CN.md)

---

## ✨ Why Auto-Evolve?

Without it, codebases slowly rot:

```
TODO pile-up     →  Duplicate code spreads     →  Technical debt accumulates
Manual review    →  Good practices don't stick  →  Teams work in silos
```

Auto-Evolve fixes all of this — **projects get better on their own, without constant manual intervention.**

---

## 🎯 Core Capabilities

### Four-Perspective Smart Inspection

Unlike other scanners that only report "code problems," Auto-Evolve examines projects from four dimensions:

```
👤 User      📦 Product      🏗 Project      ⚙️ Tech
"Usable?"  "Delivered?"   "Healthy?"    "Clean code?"
```

Each dimension has different weights, dynamically adjusted based on project type.

### Supports 12+ Project Types

```
Frontend     →  Web / Mobile App / Desktop / Mini-app / VSCode Plugin
Backend      →  REST API / Microservice / CLI / DevOps / Middleware
AI/Agent    →  Skill / Agent / ML Pipeline / AI Service
Infrastructure →  IoT Firmware / Blockchain / Data Pipeline
Content     →  SSG Docs / API Docs / Static Blog
```

Auto-detects project type, matches corresponding inspection standards.

### Seamless project-standard Integration

Auto-Evolve has **project-standard** built in as its evaluation engine:

```
Scan project → Detect type → Load standards → Four-perspective scan → Report
                                       ↓
                     product-requirements.md (Product)
                     user-perspective.md   (User)
                     project-inspection.md (Project)
                     code-standards.md   (Tech)
```

Not arbitrary judgment — **systematic inspection with standards.**

### learnings — Project Memory

```
.learnings/
├── approvals.json    ← Approved changes
├── rejections.json  ← Rejected changes + reasons
└── metrics/        ← Iteration metrics
```

The same mistake won't be made twice. Auto-Evolve gets smarter about each project.

---

## 🚀 Quick Start

```bash
# One-line install (recommended)
clawhub install auto-evolve
clawhub install project-standard
clawhub install soul-force

# Configure project to inspect
python3 scripts/auto-evolve.py repo-add ~/.openclaw/workspace/skills/soul-force --type skill --monitor

# Start fully automated inspection
python3 scripts/auto-evolve.py set-mode full-auto
python3 scripts/auto-evolve.py schedule --every 10
```

---

## 🔍 Inspection Output Example

```
🔍 Auto-Evolve Scanner v4.3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Project: soul-force (AI/Agent)
   Type: AI/Agent  |  Weights: Product30% / User25% / Tech25% / Project20%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 User Perspective ★★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.8
     SOUL.md lacks README entry — newcomers can't find where to start
     → Suggestion: Add 3-step quickstart at top of SOUL.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Product Perspective ★★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🚨 Impact 0.7
     README promises "auto-evolution" but no scheduled inspection mechanism exists
     → Suggestion: Add auto-evolve schedule config docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ Tech Perspective ★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [opt] 🟡 duplicate_code: memory.py has 3 repeated logic blocks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Learnings: 3 approvals, 1 rejection
   🚫 Owner rejected: generating test files (2x) → Stopped trying
```

---

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `scan` | Inspect all projects |
| `scan --dry-run` | Preview mode (no execution) |
| `scan --recall-persona master` | Recall owner memory for inspection |
| `scan --github-event pr_review` | Post results to GitHub |
| `confirm` | Confirm and execute pending changes |
| `approve / reject` | Approve/reject, record to learnings |
| `set-mode full-auto` | Full automation mode |
| `learnings` | View learning history |
| `learnings --summary` | Summary statistics (v4.3) |
| `trends --repo <path>` | Scan trend for a project (v4.3) |
| `rollback` | Rollback to previous version |
| `schedule --every 10` | Auto-inspect every 10 minutes |

---

## 🧠 Three-Layer Memory Architecture

```
Layer 1: OpenClaw SQLite  ← Full conversation history, cross-persona recall
Layer 2: hawk-bridge     ← Vector semantic memory, persona-isolated
Layer 3: learnings/      ← Project-level memory, approvals/rejections
```

Three layers stacked, Auto-Evolve gets better with every use.

---

## 🛡️ Safety Mechanisms

```
✓ Version control        All changes have git history, rollbackable
✓ Quality gates         pytest / jest tests must pass
✓ learnings filter     Rejected changes never repeat
✓ Privacy protection   Closed repo code never leaks
✓ Permission split    High-risk changes require owner confirmation
```

---

## 📦 Dependency Skills

| Skill | Role | Required |
|-------|------|---------|
| **project-standard** | Project taxonomy + four-perspective standards | ✅ |
| **auto-evolve** | Inspection engine + executor | ✅ |
| **soul-force** | learnings analysis + daily memory summary | Recommended |
| **hawk-bridge** | Vector semantic memory, persona-isolated | Optional |

---

## How It Works (v4.3)

```
auto-evolve scan
    │
    ▼
┌──────────────────────────────────────────────────────┐
│  Step 1: project-standard Project Type Detection      │
│  Auto-detects: Frontend / Backend / AI/Agent / Infrastructure │
│  Determines perspective weights for this type        │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 2: Four-Perspective × Standards               │
│                                                      │
│  👤 USER    → user/user-perspective.md           │
│  📦 PRODUCT → product-requirements.md              │
│  🏗 PROJECT → project-inspection.md              │
│  ⚙️ TECH   → code-standards.md                 │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 3: Compare findings against reference docs    │
│  Trend tracking (v4.3): findings from last 10 scans│
└──────────────────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│  Step 4: Execute / Notify / Record to learnings   │
└──────────────────────────────────────────────────────┘
```

---

## Related Projects

- [project-standard](https://github.com/relunctance/project-standard) — Four-perspective inspection standard library
- [SoulForce](https://github.com/relunctance/soul-force) — AI Agent memory evolution system
- [hawk-bridge](https://github.com/relunctance/hawk-bridge) — OpenClaw context memory integration

---

## License

MIT
