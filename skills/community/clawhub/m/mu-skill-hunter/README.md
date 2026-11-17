<p align="center">
  <img alt="mu-skill-hunter" src="assets/default-banner.png" width="100%">
</p>

# 🔍 mu-skill-hunter · Skill Hunter

> Discover, audit, and track AI agent skills across 4 sources — GitHub, ClawHub, SkillHub, and Skills.sh — with automated security scanning and weekly trending reports.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-skill-hunter/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-skill-hunter)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-skill-hunter)](https://github.com/muippt/mu-skill-hunter/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-skill-hunter)](https://github.com/muippt/mu-skill-hunter/stargazers)

---

### 💡 Usage Examples

- 🔍 **"Find a skill that can fill PDF forms"** — Searches all 4 sources simultaneously, returns ranked results with descriptions, links, and popularity metrics
- 🛡️ **"Audit this skill before I install it"** — Downloads to a sandboxed staging area, runs 12-rule static security scan, reports risk level (LOW/MEDIUM/HIGH/EXTREME)
- 📊 **"What's trending this week?"** — Generates a weekly report of top 8 curated skills using a three-signal selection model (heat 50% + relevance 30% + freshness 20%)
- 📦 **"Search ClawHub for MCP tools"** — Source-specific search with parallel `clawhub inspect` calls for download counts and summaries
- 🐉 **"Find skills on SkillHub (CN)"** — Queries the Tencent SkillHub public API for China-accelerated, compliant skill discovery
- ⏰ **"Set up weekly auto-report"** — Scheduled recurring report with curated top 8 picks, delivered to your preferred messaging platform at your chosen frequency
- 🧹 **"Find newly created agent skills on GitHub"** — Tracks repos created in the past week, surfaces fresh projects before they go mainstream
- ✅ **"Install this skill safely"** — Staging area isolation + scanner.py audit + risk-gated install command output

---

### ✨ Core Highlights

#### 🌐 Four-Source Discovery

| Source | API Type | Auth Required | Strength |
|--------|----------|---------------|----------|
| GitHub | HTTP API | GITHUB_TOKEN (optional, 60→5000 req/h) | Largest repo pool, stars/language/update metadata |
| ClawHub | CLI (npx) | None | Curated skill registry, inspect for downloads/summary |
| SkillHub | HTTP API + CLI | None (public) | China-accelerated, Tencent-backed, CN-friendly |
| Skills.sh | CLI (npx) | None | Install-count visibility, emerging ecosystem |

The search engine queries all 4 sources in parallel based on your keywords, deduplicates results, and presents them in a unified ranked format with source labels (🐙GitHub / 🦀ClawHub / 🐉SkillHub / 🛠️Skills.sh).

#### 🛡️ 12-Rule Security Scanner

Every external skill is scanned before installation using `scanner.py` with:

- **10 Hard Reject rules** (R1-R10): External URL requests, base64 execution, eval/exec, credential path access, Agent file access, code obfuscation, bare IP requests, privilege escalation, credential exfiltration, undeclared package installs
- **2 AI-specific rules** (AI1-AI2): Prompt injection detection, cryptocurrency mining signatures
- **4 Yellow Flag rules** (Y1-Y4): Agent directory writes, network requests, env var modifications, background processes

Scanner outputs **summaries only** (rule_id, file, line number) — never raw code — to prevent prompt injection through scanned content.

#### 📊 Three-Signal Curation Model

```
Curation basis = Heat (50%) + Relevance (30%) + Freshness (20%)
```

- **Heat**: Log-normalized stars/downloads across all results
- **Relevance**: Keyword density matching (agent-skill, mcp, automation, etc.)
- **Freshness**: Created this week = 20, this month = 10, older = 2

Forced mixing in weekly reports: ≥4 GitHub + ≥2 ClawHub + ≥1 SkillHub + ≥1 Skills.sh (when available).

#### 📨 Scheduled Trend Reports

- Top 8 curated picks + backup section
- Source-forced diversity (no single-source dominance)
- Deduplication: ClawHub by slug, GitHub same-owner ≤2
- Auto-delivered to your preferred messaging platform
- User scene profiling for personalized recommendations
- Schedule frequency is fully customizable — weekly, bi-weekly, or any interval that fits your workflow.

---

### 📌 Comparison

| Feature | mu-skill-hunter | Manual GitHub Search | ClawHub CLI Only | Skills.sh Only |
|---------|----------------|---------------------|-------------------|----------------|
| Sources | 4 (GitHub + ClawHub + SkillHub + Skills.sh) | 1 (GitHub) | 1 (ClawHub) | 1 (Skills.sh) |
| Security scan | 12-rule static analysis | None | None | None |
| Three-signal curation | Heat + Relevance + Freshness | None | None | None |
| Weekly report | Auto + curated top 8 | Manual | None | None |
| Parallel search | All sources simultaneously | Sequential | Single source | Single source |
| Download counts | ClawHub inspect + SkillHub API | N/A | Yes | Yes |
| China acceleration | SkillHub (Tencent) | No | No | No |
| Risk-gated install | 4-level (LOW/MED/HIGH/EXTREME) | User judgment | None | None |
| Prompt injection guard | AI1 rule + sandbox isolation | None | None | None |

---

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|----------|----------|---------|
| 🔍 Search Discovery | "Find a skill that can do X" | User describes a need or says "find skill" |
| 🛡️ Security Audit | "Audit/install this skill" | User ready to install an external skill |
| 📊 Weekly Report | Weekly trending digest | Scheduled (customizable) or manual `trending.py --period weekly` |

---

### ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Language | Python 3.8+ |
| Dependencies | None (stdlib only: urllib, subprocess, json, re, argparse) |
| External CLIs | Optional: `clawhub` (npm), `skillhub` (curl install), `skills` (npm) |
| GitHub API | REST v3, GITHUB_TOKEN optional (60→5000 req/h) |
| SkillHub API | Public HTTP, no auth required |
| Output formats | Human-readable table (default) or JSON (`--json` flag) |
| Security scanner | 12 rules (10 Hard Reject + 2 AI-specific) + 4 Yellow Flags |
| Curation model | Heat 50% + Relevance 30% + Freshness 20%, three-signal ranking |
| Platform | macOS / Linux / Windows (Python 3.8+) |
| Package size | ~50KB (3 Python scripts + 3 reference docs) |

---

### 🛠️ Quick Start

**1. Clone and configure**

```bash
git clone https://github.com/muippt/mu-skill-hunter.git
cd mu-skill-hunter
# Optional: configure GitHub token for higher API limits
export GITHUB_TOKEN="your_github_token"
```

**2. Search across all 4 sources**

```bash
python3 scripts/search.py "agent skill mcp" --limit 8
```

**3. Audit a skill before installing**

```bash
python3 scripts/scanner.py /path/to/external-skill --json
```

---

### 🔒 Security & Privacy

- **Local execution only** — all scripts run on your machine, no data sent to any server
- **No telemetry** — zero tracking, zero analytics, zero phone-home
- **Sandboxed staging** — external skills are downloaded to `/tmp/skill-hunter-staging/`, never directly to your skills directory
- **Scanner isolation** — `scanner.py` outputs summaries only, never raw code, to prevent prompt injection through scanned content
- **Risk-gated installation** — 4-level risk assessment (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME) with mandatory human approval for HIGH/EXTREME
- **Token safety** — GITHUB_TOKEN is read from environment only, never written to any file

---

### ⭐ Star History

If mu-skill-hunter helps you discover great skills, please consider giving it a star! ⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-skill-hunter&type=date)

> Discover, audit, and install AI agent skills with confidence — 4 sources, 12 security rules, 1 curated selection model.

---

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 木先生iPPT

This project builds upon the following excellent platforms and tools:
- [GitHub API](https://docs.github.com/en/rest) — Repository search and metadata
- [ClawHub](https://clawhub.ai) — Curated AI agent skill registry
- [SkillHub](https://skillhub.cn) — China-accelerated skill marketplace by Tencent
- [Skills.sh](https://skills.sh) — Emerging skill discovery platform

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
