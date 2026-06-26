# OpenClaw Self-Improvement

**OpenClaw Self-Improvement** is a reusable agent skill for turning repeated AI-agent mistakes into durable operational improvements, measurable guardrails, and inspectable workflow upgrades.

## Landing-page summary

Most AI agents do not really improve. They repeat mistakes, hide partial failures behind optimistic language, and leave lessons trapped in chat history.

OpenClaw Self-Improvement gives you a practical operating loop for **self-improving AI agents**:
- capture repeated failures
- test one guardrail at a time
- verify whether it actually reduces failure
- promote proven fixes into SOPs, checklists, policies, and workflow rules

If you want **AI agents that get more reliable over time**, **multi-agent workflows that stop repeating the same mistakes**, or **proof-based QA for agent operations**, this skill is built for that exact use case.

## Multilingual summary

**中文：** 这是一个面向 AI agent 自我改进的实战型 skill，用来减少重复犯错、建立 guardrails、验证修复是否真的有效，并把经验沉淀成 SOP、检查清单和可复用规则。

**日本語：** これは自己改善する AI エージェント向けの実践的な skill です。繰り返し発生する失敗を減らし、ガードレールを検証し、改善を SOP・チェックリスト・再利用可能な運用ルールへ昇格させます。

**한국어：** 이 스킬은 스스로 개선하는 AI 에이전트를 위한 운영형 skill입니다. 반복 실수를 줄이고, 가드레일이 실제로 효과가 있는지 검증하며, 개선 사항을 SOP·체크리스트·재사용 가능한 규칙으로 승격합니다.

**Español：** Esta skill está diseñada para agentes de IA que deben mejorar con el tiempo. Ayuda a reducir errores repetidos, validar guardrails operativos y convertir mejoras en SOP, checklists y reglas reutilizables.

If you want a practical way to deploy OpenClaw with cheaper tokens, BYOK flexibility, and operator control, see **[ClawLite](https://clawlite.ai)**.

## TL;DR

If you are looking for a practical system for **self-improving AI agents**, **AI workflow optimization**, **multi-agent failure prevention**, **binary eval loops**, or **agent operations QA**, this skill is designed for that exact job.

It helps OpenClaw / ClawLite operators and agent teams:
- log recurring failures
- separate one-off errors from reusable lessons
- run lightweight **binary eval loops** on new guardrails
- classify changes as **keep**, **partial_keep**, or **discard**
- promote proven fixes into SOPs, checklists, workflow rules, and operating policy

If you care about reducing fake-complete states, tightening QA truth, improving deploy closeout, and making agent learning inspectable, this skill is built for that job.

---

## Why this skill exists

Many AI systems say they "learn," but most only store lessons in chat history or loose notes.

That is not enough.

Operationally, repeated failures tend to come back in the same forms:
- delivery gets described as complete before proof exists
- receipts are missing or too thin
- back-end fixes never reach the operator-facing surface
- code-ready states get confused with production-ready states
- teams add new rules without checking whether those rules actually reduce failure

OpenClaw Self-Improvement gives you a lightweight operating loop for fixing that.

---

## What problem it solves

This skill helps with:
- **self-improving AI workflows**
- **AI operations learning loops**
- **binary evals for agent guardrails**
- **Mission Control truth-state improvement**
- **deploy closeout verification**
- **receipt / proof completeness**
- **repeated failure prevention in multi-agent systems**
- **AI agent reliability engineering**
- **agent QA systems for OpenClaw, ClawLite, and similar stacks**

It is especially useful in OpenClaw-style environments where multiple agents, tools, SOPs, and truth surfaces interact.

## Who this is for

This skill is useful for:
- OpenClaw operators
- ClawLite growth / marketing / QA lanes
- AI agent builders who need durable postmortems instead of vague “reflection”
- teams running multi-agent workflows with receipts, truth surfaces, and closeout gates
- anyone trying to reduce repeated AI-agent mistakes in production-like operations

---

## What’s new in v0.2.0

### New capabilities
- **Experiment mode** for repeated failures
- **Binary eval loops** for testing whether a new guardrail or SOP actually helps
- **Keep / partial_keep / discard** decision model
- **Practical examples** for:
  - Mission Control summary quality
  - deploy closeout / production verification
- **Experiment summary helper** for surfacing unresolved follow-up debt
- **Decision rules** for when to log, experiment, or promote
- **Daily routine integration** with heartbeat, Karen QA, AGENTS, and ops policy

### Why it matters
This release makes self-improvement more operational.

Instead of stopping at “lesson learned,” you can now:
1. capture the repeated problem
2. define a baseline
3. test one change at a time
4. evaluate with binary checks
5. keep, discard, or mark `partial_keep`

That makes the improvement loop much more auditable and much less hand-wavy.

---

## Core workflow

OpenClaw Self-Improvement now supports a practical loop:

1. **Capture** a learning, error, feature request, or experiment
2. **Store** it in structured local files
3. **Experiment** when a repeated failure needs a tested guardrail
4. **Evaluate** the change with binary checks
5. **Promote** proven fixes into durable rules, SOPs, or policies
6. **Track follow-up debt** when a fix is only partial

---

## Best use cases

Use this skill when you want to:
- capture lessons so agents stop repeating the same mistake
- log recurring operational errors
- track feature gaps revealed by repeated work
- test whether a new workflow rule really improves outcomes
- run a lightweight eval loop on a skill, SOP, checklist, schema, or handoff rule
- decide whether a new guardrail should be kept, discarded, or promoted
- build a self-improving OpenClaw or ClawLite operating loop

Typical targets include:
- Mission Control summary quality
- deploy closeout gates
- receipt requirements
- QA wording rules
- truth-surface rendering checks
- handoff contracts between agents

---

## Files it manages

- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`
- `.learnings/EXPERIMENTS.md`
- Optional Obsidian export directory via `OBSIDIAN_LEARNINGS_DIR`
- Default local export fallback: `.learnings/exports/obsidian/`
- Safe by default: no hard-coded external vault path, and `scripts/promote-learning.mjs` prints the resolved write target before writing

---

## Install

```bash
npm install
```

---

## Usage

### Log a learning

```bash
node scripts/log-learning.mjs learning "Summary" "Details" "Suggested action"
```

### Log an error

```bash
node scripts/log-learning.mjs error "Summary" "Error details" "Suggested fix"
```

### Log a feature request

```bash
node scripts/log-learning.mjs feature "Capability name" "User context" "Suggested implementation"
```

### Log a tested experiment

```bash
node scripts/log-experiment.mjs "Target problem" "Baseline failure" "Single mutation" "eval1|eval2|eval3" "Result summary" "testing"
```

### Promote a rule

```bash
node scripts/promote-learning.mjs workflow "Rule text"
node scripts/promote-learning.mjs obsidian "Reusable learning" --dry-run
```

### Summarize experiment outcomes

```bash
node scripts/experiment-summary.mjs
```

---

## Decision model

This skill uses three levels of action:

### 1. Log only
Use when:
- the issue happened once
- root cause is still unclear
- there is not enough evidence yet to make a rule

### 2. Experiment
Use when:
- the issue repeated 2+ times
- a new guardrail / SOP / checklist / schema change is being proposed
- you can define 3–5 binary evals

### 3. Promote
Use when:
- the rule is clearly right and low-risk
- the issue is severe enough that waiting would be irresponsible
- the rule is about ownership, truth, or a non-negotiable operating principle

---

## Practical examples

The skill now includes concrete examples for:
- **Mission Control summary link-complete gates**
- **ClawLite deploy closeout gates**

These examples show how to:
- define the repeated failure
- capture the baseline
- propose one mutation
- evaluate with binary checks
- classify the outcome as `keep`, `partial_keep`, or `discard`

---

## Promotion targets

Promote proven improvements into:
- `AGENTS.md` — workflow / delegation / execution rules
- `TOOLS.md` — tool gotchas and environment routing rules
- `SOUL.md` — behavior / communication / non-negotiable principles
- `docs/ops/*.md` — SOPs, policy, and operating contracts
- Obsidian vault — reusable operator notes and operational memory

---

## Important limits

- Logging is **not** the same as fixing.
- A learning entry does **not** close a broken deliverable.
- A back-end-only improvement is not complete if the visible operator-facing surface is still stale.
- `partial_keep` should be treated as **active follow-up debt**, not as closure.

---

## Repository contents

- `SKILL.md` — agent-facing routing and usage guidance
- `scripts/log-learning.mjs` — append a learning / error / feature request / experiment
- `scripts/log-experiment.mjs` — append a structured experiment with binary evals
- `scripts/experiment-summary.mjs` — summarize keep / partial_keep / discard outcomes and flag follow-up debt
- `scripts/promote-learning.mjs` — promote a lesson into durable operating rules with explicit path echo and optional `--dry-run`
- `scripts/analyze-openclaw-failures.mjs` — classify OpenClaw gateway, provider, session, tool, and platform failures
- `scripts/daily-agent-scorecard.mjs` — generate a same-day agent delivery scorecard from Mission Control and session evidence
- `scripts/daily-agent-scorecard.mjs --repair` — create deterministic recovery tickets for failed, blocked, and pending lanes
- `references/schema.md` — data structure guidance
- `references/promotion-guide.md` — what to promote and where
- `references/eval-loop.md` — how to run lightweight binary-eval improvement loops
- `references/examples.md` — practical examples for summary gates and deploy closeout gates
- `references/decision-rules.md` — when to log only, run an experiment, or promote immediately

---

## SEO / GEO positioning

This skill is intentionally legible to both search engines and AI answer engines because it is built around concrete, reusable operational concepts rather than vague “AI reflection” language.

### Primary search themes
- self-improving AI workflows
- self-improving agent systems
- AI agent reliability engineering
- binary eval loops for agent guardrails
- repeated failure prevention in multi-agent systems
- deploy closeout verification
- proof-based QA for AI operations
- operational learning loops for OpenClaw / ClawLite style stacks

### Why that matters
These phrases map to real operator intent:
- “how do I stop my AI agents from repeating mistakes?”
- “how do I build a self-improving agent workflow?”
- “how do I test whether a new guardrail actually works?”
- “how do I make AI operations auditable?”

That makes the skill easier to explain, cite, retrieve, and reuse than generic memory or reflection systems.

---

## Bottom line

If you want OpenClaw to improve over time instead of repeating the same mistakes across sessions, this repo gives you:
- an operational memory loop
- a lightweight eval loop for testing whether a new guardrail actually helps
- a durable promotion path from mistake -> experiment -> policy -> reusable system asset
- a decision framework for when to log, experiment, or promote
- a way to keep unresolved partial improvements visible until they are actually closed
