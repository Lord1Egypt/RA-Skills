---
name: lobster-subagent-dev
version: 1.0.0
description: "Subagent-driven development. Dispatch fresh subagent per task with 2-stage review (spec + quality). Cost-aware model routing. From Superpowers by Jesse Vincent."
author: "Super Lobster 🦞"
tags: ["subagent", "development", "tdd", "review", "parallel"]
license: MIT
---

# Lobster Subagent-Driven Development 🦞

**Fresh subagent per task. Two-stage review. Ship with confidence.**

Inspired by [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent.

## Core Principle

```
Fresh subagent per task + 2-stage review = high quality, fast iteration
```

Subagents never inherit session context. You construct exactly what they need. This preserves your own context for coordination work.

## The Process

### 1. Read Plan → Extract Tasks
- Read implementation plan once
- Extract ALL tasks with full text
- Create TodoWrite tracking

### 2. Per Task: Implementer → Spec Review → Quality Review

```
[Dispatch Implementer]
  ↓ (if questions → answer → re-dispatch)
[Implementer: implement + test + commit + self-review]
  ↓
[Dispatch Spec Reviewer]
  ↓ ❌ → Fix → Re-review
  ↓ ✅
[Dispatch Code Quality Reviewer]
  ↓ ❌ → Fix → Re-review
  ↓ ✅
[Mark task complete]
  ↓
[Next task...]
```

### 3. Final Review
After all tasks complete:
- Dispatch final code reviewer for entire implementation
- Verify all requirements met
- Run full test suite

## Model Selection

| Task Type | Model | Why |
|-----------|-------|-----|
| 1-2 files, complete spec | Cheapest | Mechanical |
| Multi-file integration | Standard | Needs judgment |
| Architecture/review | Strongest | Needs expertise |

## Agent Status Handling

| Status | Action |
|--------|--------|
| DONE | Proceed to spec review |
| DONE_WITH_CONCERNS | Read concerns, then decide |
| NEEDS_CONTEXT | Provide context, re-dispatch |
| BLOCKED | Change model / split task / escalate |

## Never

- Skip reviews (spec OR quality)
- Start quality review before spec passes
- Let implementer self-review replace actual review
- Move to next task while review has open issues
- Dispatch multiple implementers in parallel (conflicts)
