<p align="center">
  <picture>
    <img alt="mu-dev-workflow" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🔄 mu-dev-workflow · 人虾协作开发工作流

> A lightweight methodology framework that forces AI agents to align with user requirements before coding — saving tokens and preventing rework.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-dev-workflow/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-dev-workflow)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-dev-workflow)](https://github.com/muippt/mu-dev-workflow/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-dev-workflow)](https://github.com/muippt/mu-dev-workflow/stargazers)

---

### 💡 Usage Examples

1. 🆕 **Creating a new Skill from scratch** — The Agent asks 5 clarifying questions before writing a single line of code, producing an Intent Brief for your confirmation
2. 🐛 **Fixing a bug** — Quick mode: confirm the issue, fix, verify with actual command output (no "should be fine" allowed)
3. 🏗️ **Building a new feature** — Full 5-stage workflow with design doc, architecture pattern selection, and dual-stage review
4. 🔄 **Refactoring existing code** — Stages 1-3 only, with explicit guardrails against over-refactoring
5. 📋 **Outputting a proposal or plan** — Three-question self-check (real problem? reinventing the wheel? edge cases?) ensures quality before delivery
6. 🤖 **Multi-agent task delegation** — Dual-stage review (spec review + quality review) with Monitor mechanism for long-running tasks
7. 🚫 **Preventing Agent from wasting tokens** — Hard gates physically block the Agent from coding before requirements are clear and confirmed
8. 📝 **Skill quality audit** — Integration with `skill-audit.sh` for automated 23-item quality checklist on Skill files

---

### ✨ Core Highlights

#### 🚧 Five-Stage Hard-Gated Workflow

The entire development lifecycle is divided into five stages with explicit entry and exit conditions. No stage can be skipped — the Agent physically cannot write code until Stage 1 (Requirements Clarification) is complete and you confirm the direction.

| Stage | Name | Entry Condition | Exit Condition |
|-------|------|-----------------|----------------|
| 1 | Requirements Clarification | Received a dev/Skill request | Requirements type clear + options presented + user confirmed |
| 2 | Design Confirmation | Stage 1 complete, direction confirmed | Design doc with self-check output + user says "go" |
| 2.5 | Skill Quality Gate | (Skill dev only) Stage 2 done | mu-skill-creator flow complete + security check passed |
| 3/4 | Plan & Execute | Stage 2 complete | Tasks executed, sub-agents returned, core feature runnable |
| 5 | Verification & Wrap-up | Stage 3/4 complete | Checklist all green + committed + reported |

#### 🧠 Critical Three-Question Self-Check

Every proposal, plan, or strategy output must include a "Critical Self-Check" section — delivered together with the proposal itself. No self-check = incomplete proposal = blocked from submission.

| # | Self-Check Question | Dev Scenario | HR Scenario | Planning Scenario |
|---|-------------------|-------------|-------------|-------------------|
| 1 | **Real problem? Simpler solution?** | Is the plan over-engineering? | Is the strategy targeting the real bottleneck? | Is the goal a real need or just inertia? |
| 2 | **Reinventing the wheel? Reuse?** | Can existing Skills/tools cover it? | Is there an existing process/team doing this? | Can upstream/downstream goals align? |
| 3 | **Edge cases? How to handle?** | Are references complete? Degradation chain? | Candidate no-show / HC freeze / JD change? | Resource shortage / direction change / missing people? |

#### 🎯 Skill Intent Clarification Protocol

Before creating any Skill, the Agent must ask up to 5 targeted questions (one at a time) to nail down the Skill's core value, boundaries, and risk modes. The output is a **Skill Intent Brief** that must be confirmed before entering the design phase.

| # | Question | Purpose |
|---|----------|---------|
| 1 | What cognitive burden must this Skill eliminate? | Define core value |
| 2 | What do you least want it to be misunderstood as? | Define boundaries |
| 3 | What is its most dangerous failure mode? | Identify risks |
| 4 | Whose behavior should its output change? | Identify beneficiaries |
| 5 | If it works, which existing workflow becomes redundant? | Assess impact scope |

#### 🛡️ Anti-Rationalization Excuse Table

Six common skip-excuses with reality checks, pre-registered as anti-patterns. When the Agent encounters any excuse to skip Stage 1, it is forced to stop and complete requirements clarification first.

| Common Excuse | Reality |
|---------------|---------|
| "The requirement is simple, no design needed" | Simple requirements have hidden dependencies too; 30 min of design saves 3 hours of rework |
| "I already know how to do this" | Knowing how ≠ the user knowing what you'll do; the design doc is an alignment tool |
| "It's just a one-line change" | One line can affect ten callers; check impact scope first |
| "No time, just do it first" | Rushed code becomes tech debt; design takes at most 5 minutes |
| "I've done this feature before" | Previous context may have changed; verify interface compatibility before reuse |
| "The user is rushing me, skip design" | The user wants results, not a broken process; slow is fast |

#### 🔄 ICE-5 Incident Closure

When a qualifying incident occurs (same-type failure second occurrence, or first-time external delivery/publish incident, or irreversible/silent-degradation risk), five fields must be embedded directly into the execution path — not in a separate log or memory entry.

| Field | Description |
|-------|-------------|
| **Trigger Step** | What sequence of actions triggers the failure |
| **Enforcement Point** | Where in the code/script/checklist the gate is placed |
| **Failure Behavior** | What happens when the gate fires |
| **Evidence** | Actual command output or audit proof at the enforcement point |
| **Post-Failure Action** | What the Agent must do after the gate fires |

#### 🤖 Sub-Agent Dual-Stage Review

Complex tasks are delegated to sub-agents with a mandatory two-stage review pipeline. A Monitor Agent watches long-running tasks and reports anomalies. Task size constraints prevent context truncation.

| Stage | Reviewer | Checks |
|-------|----------|--------|
| Spec Review | Spec Review Agent | All designed features implemented? Nothing missing? Nothing extra? |
| Quality Review | Quality Review Agent | Readability, conciseness, robustness, consistency |
| Monitor (long tasks) | Monitor Agent | Reads task board every 5 min, reports blocked/timeout to main agent |

#### 🏗️ Architecture Pattern Library

Six architecture patterns with a decision tree and shared component checklist, so every new Skill starts from a proven structure instead of from scratch.

| Pattern | Name | Best For |
|---------|------|----------|
| A | Route Dispatch | Multi-scenario coverage |
| B | Linear Pipeline | Fixed-step document production |
| C | Dual-Mode Interaction | Users may already have partial info |
| D | Capability Module | Multi-function composite Skills |
| E | Rule Engine | Quality scan / security check / format fix |
| F | Three-Tier Priority | Must-do vs. could-do separation |

---

### 📌 Comparison

| Dimension | 🧭 mu-dev-workflow | Manual/Bare Dev | Superpowers |
|-----------|-------------------|-----------------|-------------|
| Structure | 1 file + 3 refs, self-contained | None | 14 built-in skills, granular |
| Target User | Technical beginners | No barrier | Experienced developers |
| Scope | Skill development + code development | Anything | General software engineering |
| Incident Closure | ICE-5 five-field mechanism | None | None |
| Anti-Skip | Explicit excuse table + reality check | None | Implicit in flow |
| Architecture Guide | 6 patterns + decision tree | None | None |
| Skill Creation | Intent clarification + 4 type templates | None | None |
| Sub-Agent Review | Dual-stage + Monitor + size constraints | None | Has sub-agent mechanism |
| Platform | Agent-agnostic (works with any AI agent) | Any | Claude Code native |
| License | MIT | N/A | MIT |

---

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|----------|----------|---------|
| Full 5-Stage | New Skill development, large features | "develop" / "write code" / "new feature" / "new skill" |
| Quick Mode | Skill creation <1500 lines | Auto-detected by size estimation |
| Bug Fix Shortcut | Small bugs (<30 min) | "fix bug" / "fix" |
| Non-Dev Self-Check | Proposals, plans, strategies | "self-check" / "three-question check" |

---

### ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Type | AI Agent Methodology Framework (Markdown rules) |
| Dependencies | None (pure Markdown, no runtime) |
| Compatible Environments | Any AI agent that supports custom instructions/skills (Claude Code, Cursor, CatPaw, etc.) |
| Package Size | ~30KB (4 Markdown files) |
| File Structure | SKILL.md + references/ (3 files) |
| Input Support | Natural language triggers |
| Output Format | Design docs, code, verification reports |
| Language | Chinese (primary), English (README) |
| Version | 2.1.0 |
| License | MIT |

---

### 🛠️ Quick Start

**1. Install**

```bash
git clone https://github.com/muippt/mu-dev-workflow.git ~/.claude/skills/mu-dev-workflow
```

> Other agents (Cursor, CatPaw, etc.) may use their own skill directory or project-level `.claude/skills/mu-dev-workflow`.

**2. Verify**

Restart your agent, then type:

```
List my available skills
```

**3. Run**

```
Help me develop a new feature
```

Or invoke a specific workflow:

```
Help me create a new Skill
```

```
Self-check this proposal with the three questions
```

---

### 🔒 Security & Privacy

- 100% local execution, no network calls
- No telemetry, no data collection
- Pure Markdown files, no executable code
- No API keys or credentials needed

---

### ⭐ Star History

If mu-dev-workflow saves your tokens, consider giving it a star!

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-dev-workflow&type=date)

> A lightweight methodology framework that forces AI agents to align with user requirements before coding — saving tokens and preventing rework.

---

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 木先生 (muippt)

This project draws inspiration from [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent. The critical-thinking framework references *Asking the Right Questions* (Browne & Keeley).

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
