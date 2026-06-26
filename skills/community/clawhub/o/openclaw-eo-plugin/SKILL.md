---
name: eo-collaboration
description: "Everything Openclaw (EO) - Transform OpenClaw into a Steel Crayfish Legion with 141 experts, 9 commands, Skills dual system, and 15 core innovations"
metadata:
  openclaw: {}
---

# Everything Openclaw (EO) - IRON CLAW ⚙️🦞

> Transform your OpenClaw Agent from a lone soldier into a Steel Crayfish Legion — 141 experts, 9 commands, Skills + Experts dual system.

## 🦞⚙️ One-Line Summary

**EO (Everything Openclaw)** supercharges OpenClaw with a multi-expert collaboration engine, giving your agent a "mech suit" that orchestrates 141 specialists across 13 domains — from a single prompt to a coordinated team execution.

---

## 🚀 15 Core Innovations

| # | Innovation | What It Does |
|---|-----------|--------------|
| 1 | **141-Expert Library** | 141 pre-built experts across 13 domains (Architect, Planner, Frontend, Backend, QA, Security, DevOps, CodeReviewer, Design, Academic, Marketing, Specialized, Research) |
| 2 | **9 Standardized Commands** | `/plan`, `/architect`, `/verify`, `/code-review`, `/security-scan`, `/deploy`, `/design`, `/market`, `/research` — one command, one expert |
| 3 | **Skills Dual System** | EO experts + standard OpenClaw skills coexist; experts handle complex decisions, skills handle specialized tasks |
| 4 | **Multi-Expert Parallel Execution** | Spawn multiple experts simultaneously for independent workstreams (e.g., frontend + backend in parallel) |
| 5 | **Checkpoint Validation** | Every milestone gets verified by QA before proceeding — errors caught early, not at deployment |
| 6 | **MD + TS Hybrid Architecture** | Pure markdown expert definitions (human-readable, version-controlled) + TypeScript execution engine (type-safe, fast) |
| 7 | **Proactive Memory Management** | Experts write context to `memory/` autonomously — no manual state management |
| 8 | **Auto Workspace Isolation** | Each expert gets a clean workspace context — no cross-contamination of task state |
| 9 | **Skill Compatibility Layer** | Import Claude Code skills and ECC (everything-claude-code) skills automatically — drop-in compatibility |
| 10 | **Bilingual Documentation** | Full docs in English + 中文; Chinese users get native-language guidance, English users get international standards |
| 11 | **Expert Role Color System** | 🔴 Red (Strategy) / 🔵 Blue (Engineering) / 🟢 Green (Planning) / 🟡 Yellow (Creative) / 🟣 Purple (QA) / ⚪ White (Security) — visual role clarity |
| 12 | **Orchestrated Handoff Protocol** | Structured handover between experts: Planner → Architect → Engineers → QA → DevOps, with explicit checkpoints |
| 13 | **Openclaw Plugin API v1 Compatible** | Built on official `openclaw.plugin.json` schema — installs cleanly, updates safely, no monkey-patching |
| 14 | **Zero-Config Defaults** | Works out-of-the-box with sensible defaults; advanced users can override any expert or workflow |
| 15 | **MIT-0 License** | Completely free — use, modify, redistribute, no attribution required, commercial-friendly |

---

## 📦 Installation

```bash
# Install from GitHub (recommended)
openclaw plugins install https://github.com/467718584/everything-openclaw

# Or install the plugin directly
openclaw plugins install /home/zzy/workspace/everything-openclaw/openclaw-eo-plugin
```

---

## ⚔️ Commands Reference

| Command | Expert | Description |
|---------|--------|-------------|
| `/eo-plan [task]` | Planner | Breaks down project into actionable phases with estimates |
| `/eo-architect [project]` | Architect | Designs system architecture, tech stack, data model |
| `/eo-verify [checkpoint]` | QA | Validates milestone output against spec before handoff |
| `/eo-code-review [path]` | CodeReviewer | Full review: style + security + performance + best practices |
| `/eo-security-scan [path]` | Security | Scans for vulnerabilities, OWASP Top 10, supply chain risks |
| `/eo-deploy [env]` | DevOps | Automated deployment with rollback support |
| `/eo-design [brief]` | Design | UI/UX design with accessibility and brand compliance |
| `/eo-market [product]` | Marketing | Go-to-market strategy, positioning, and campaign planning |
| `/eo-research [topic]` | Research | Deep-dive research with source citation and analysis |

---

## 🔄 EO vs. Native OpenClaw

| Capability | OpenClaw (Native) | OpenClaw + EO |
|-----------|------------------|---------------|
| Agent type | Single agent | N-agent team |
| Expert count | 0 built-in | 141 built-in |
| Task decomposition | Manual prompt engineering | Automatic via Planner |
| Architecture design | You figure it out | Architect expert drafts it |
| Code review | Generic LLM feedback | Multi-expert: security + style + perf |
| Validation | Manual | Automated Checkpoint QA |
| Skill ecosystem | OpenClaw skills only | OpenClaw skills + EO experts |
| Memory management | Manual | Proactive (experts write memory) |
| Workflow orchestration | One-shot prompts | Orchestrated multi-stage pipeline |
| Parallel execution | No | Yes — independent experts run simultaneously |
| Chinese documentation | Partial | Full (EN + 中文) |
| License | OpenClaw terms | MIT-0 (free for all) |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   OpenClaw Agent                      │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │              EO Plugin                          │ │
│  │                                                │ │
│  │  Commands: /eo-* (9 standardized commands)     │ │
│  │  Tools: eo_collab, eo_plan, eo_architect, etc. │ │
│  │  Hooks: before_tool_call (auto-expert dispatch)│ │
│  │                                                │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Expert Library (141 experts)            │  │ │
│  │  │  13 domains × sub-specializations        │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  │                                                │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Skills Layer (EO Skills + OpenClaw Skills)│ │ │
│  │  └──────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

## 🛠️ Quick Start

```bash
# Install EO
openclaw plugins install https://github.com/467718584/everything-openclaw

# Try it — plan a project
/eo-plan "开发一个博客系统"

// Design its architecture
/eo-architect "博客系统"

// Verify the design
/eo-verify "架构设计"

// Run a full code review
/eo-code-review "./src"
```

---

## 📚 Links

- **GitHub**: https://github.com/467718584/everything-openclaw
- **Plugin Source**: https://github.com/467718584/everything-openclaw/tree/main/openclaw-eo-plugin
- **Expert Library**: 141 experts in `expert-library/` directory
- **Issues**: https://github.com/467718584/everything-openclaw/issues

---

## 📋 Requirements

- OpenClaw >= 2026.3.0
- Node.js >= 18.0.0

## 📄 License

**MIT-0** — Free to use, modify, and redistribute. No attribution required.

---

*🦞⚙️ IRON CLAW - 让每个 Agent 都穿上机甲 / Suit Up Every Agent*
