---
name: gstack-pro
slug: gstack-pro
version: "1.0.0"
tagline: "Your AI Development Team in 10 Roles"
description: >
  Transform your AI assistant into a structured virtual software engineering team with 10 specialist roles —
  inspired by Garry Tan's GStack (YC CEO, 16K GitHub Stars) and adapted for OpenClaw's subagent architecture.
  Covers the full development lifecycle: product thinking → architecture → design → code review → QA → ship → retro.
  Generator-Evaluator pattern included. Health Score (0-100) for every sprint. Automated browser QA.
  Activate when: starting a new feature, preparing to ship, doing code review, running QA, or needing a product rethink.
  Works with: OpenClaw subagents (coder/tester/architect/writer/operator/designer/progress/requirer).
---

# GStack Pro — 10-Role AI Engineering Team

> Built on the philosophy of Garry Tan's GStack (YC CEO) · 16K GitHub Stars · MIT License  
> Adapted for OpenClaw subagent + session architecture

---

## What It Does

GStack Pro gives your AI **10 specialist roles** — each with a clear mandate, a structured output format, and a measurable quality bar.

Instead of one generic AI doing everything badly, you get a team:

| # | Role | Icon | Subagent | Best For |
|---|------|------|----------|----------|
| 1 | CEO / Product Thinker | 🏛️ | `requirer` | Rethink the problem before building |
| 2 | Architect / Tech Lead | 🏗️ | `architect` | Lock in data flow, failure modes, tests |
| 3 | Designer Review | 🎨 | `designer` | 80-item design audit, AI slop detection |
| 4 | Paranoid Code Review | 🔍 | `tester` | N+1, race conditions, trust boundaries |
| 5 | Browser QA | 🌐 | `browser` tool | AI with eyes — login, click, screenshot, verify |
| 6 | Automated QA + Fix | 🧪 | `tester` + `coder` | Find → fix → re-verify with Health Score |
| 7 | QA Reporter | 📊 | `tester` | Report-only, clean handoff to team |
| 8 | One-Command Ship | 🚀 | `operator` | sync → test → push → PR |
| 9 | Engineering Retro | 🔄 | `progress` | Commit analysis, praise, growth areas |
| 10 | Release Docs | 📝 | `writer` | Sync docs to match what shipped |

---

## The Development Cycle

```
User Request
     ↓
① CEO审视 (/plan-ceo)
   → Is this worth building? What's the 10-star product?
     ↓
② Architecture Lock (/plan-eng)
   → Data flow, state machine, failure modes, test matrix
     ↓
③ Design Review (/plan-design)
   → 80-item audit, design quality grades, AI slop detection
     ↓
④ Paranoid Code Review (/review)
   → N+1, race conditions, trust boundary violations
     ↓
⑤ Automated Browser QA (/qa)
   → AI drives browser, finds bugs, fixes them, re-verifies
   → Health Score 0-100 determines ship-readiness
     ↓
⑥ One-Command Ship (/ship)
   → sync main → run tests → push → open PR
     ↓
⑦ Engineering Retro (/retro)
   → Commit analysis, team performance, improvement plan
     ↓
⑧ Release Docs (/document)
   → Update README/ARCHITECTURE to match what shipped
```

---

## How to Activate a Role

### Method 1: Direct Command (e.g., in conversation)

```
/plan-ceo: 为AICFO设计一个新功能：员工工资条自动生成PDF

/review: 审查deepfmt Sprint 3的代码改动

/qa: 对 https://xxx.space.minimaxi.com 运行标准QA测试
```

### Method 2: Subagent (for background/parallel work)

```javascript
sessions_spawn({
  agentId: "tester",  // QA + Review
  task: "Read skills/gstack-pro/roles/review.md then review the code at /workspace/projects/aicfo/aicfo-mvp/src/api/"
})
```

---

## Health Score System

After every `/qa` session, output a structured score:

```json
{
  "healthScore": 85,
  "status": "🟡 Good",
  "breakdown": {
    "functional": { "passed": 8, "total": 10, "score": 24 },
    "edgeCases": { "covered": 4, "total": 5, "score": 20 },
    "consoleErrors": { "passed": true, "score": 25 },
    "designRegressions": { "passed": true, "score": 16 }
  },
  "shipRecommendation": "🟡 Fix 2 minor issues before ship"
}
```

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | 🟢 Excellent | Ready to ship immediately |
| 70-89 | 🟡 Good | 2-3 minor issues, fix before ship |
| 50-69 | 🟠 Needs Work | Significant bugs, fix before next sprint |
| <50 | 🔴 Do Not Ship | Core functionality broken, redo required |

---

## Quality Bars

### Code Must Pass

- ✅ N+1 queries eliminated
- ✅ All external calls have timeouts
- ✅ Retries with exponential backoff
- ✅ Database transactions properly bounded
- ✅ Input validation on all untrusted data
- ✅ No trust boundary violations
- ✅ Structured logging (JSON, with trace IDs)

### Design Must Pass

- ✅ Consistent visual hierarchy
- ✅ No AI slop patterns (copy-paste generic cards, overuse of gradients)
- ✅ Responsive at 375px / 768px / 1440px
- ✅ Accessible (color contrast, focus states)
- ✅ Meaningful empty states

---

## Anti-Patterns Detected

| Pattern | Why It Fails | Detection |
|---------|-------------|----------|
| "Looks good!" | AI self-evaluation bias | Evaluator never reads generator code |
| Circular dependency | Unmaintainable architecture | Dependency graph analysis |
| AI slop | Generic, low-quality design | 80-item designer audit |
| Magic numbers | Hard to maintain | `no-magic-numbers` lint rule |
| Forgotten edge cases | Silent production failures | Mandatory test matrix |
| No rollback plan | Can't safely deploy | `/ship` requires rollback plan |

---

## OpenClaw Subagent Mapping

| Role | Subagent ID | Type |
|------|-------------|------|
| CEO Product | `requirer` | demand analysis |
| Architect | `architect` | tech design |
| Designer | `designer` | UI/UX review |
| Code Review | `tester` | quality assurance |
| Browser QA | `browser` tool | automated testing |
| QA + Fix | `tester` + `coder` | test + implement |
| QA Reporter | `tester` | reporting |
| Ship | `operator` | release |
| Retro | `progress` | analysis |
| Docs | `writer` | documentation |

---

## Key Insight: Generator vs Evaluator

**GStack Pro separates creation from judgment.**

```
Generator Agent  ──→  builds code  ──→  Evaluator Agent
  (creates)         (artifact)           (judges from SPEC + URL only)
                                              ↑
                                       Never reads generator's code
```

This eliminates **cognitive commitment bias** — the AI can't judge what it already committed to building.

Inspired by: Anthropic Engineering, "Harness Design for Long-Running Application Development" (2026)

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — overview and usage |
| `references/plan-ceo.md` | CEO product thinking SOP |
| `references/plan-eng.md` | Architecture review SOP |
| `references/review.md` | Paranoid code review SOP |
| `references/qa.md` | Automated QA SOP + Health Score |
| `references/ship.md` | One-command ship SOP |
| `references/retro.md` | Engineering retro SOP |

---

*Inspired by Garry Tan's GStack (https://gstacks.org) · MIT License*
*For OpenClaw · Compatible with Claude Code GStack workflows*
