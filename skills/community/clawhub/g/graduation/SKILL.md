---
name: graduation
displayName: "Graduation Trip Flights — Post-Grad Travel, Student Fare, Class Trip Booking"
description: "Book graduation trip flights, post-grad travel and class trip booking with student fare deals. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below. If a flag is not listed, it does not exist.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: graduation

## Overview

Graduation trip flights — post-grad travel, student fare, class trip booking. For graduates celebrating with travel.

## When to Activate

User query contains:
- English: "graduation flight", "grad trip", "post-grad travel", "class trip flight", "graduation travel"
- Chinese: "毕业航班", "毕业旅行", "毕业出行", "毕业季机票", "同学旅行"

Do NOT activate for: student discounts (general) → `student-deal`; budget trips → `economy-flights`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code |
| `--destination` | Yes | Arrival city or airport code |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--sort-type` | No | **Default: 3** (price ascending — budget priority) |
| `--seat-class-name` | No | economy (default for grads) |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--max-price` | No | Price ceiling in CNY |
| `--dep-date-start` | No | Grad season window start |
| `--dep-date-end` | No | Grad season window end |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- ✅ Returns version → proceed
- ❌ `command not found` → install flyai-cli first

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Grad Season Budget Trip

**Trigger:** "graduation flight", "毕业航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {jun_start} --dep-date-end {aug_end} --seat-class-name economy --sort-type 3
```

### Playbook B: Class Trip Group Search

**Trigger:** "class trip", "同学旅行"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --sort-type 2
```

### Playbook C: Flexible Date Grad Trip

**Trigger:** "grad trip flexible dates", "毕业旅行随便哪天"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

### Playbook D: Broad Search

**Trigger:** 0 results from above.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} graduation trip flights"
```

See [references/playbooks.md](references/playbooks.md). On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

## Usage Examples

```bash
flyai search-flight --origin "Wuhan" --destination "Lijiang" --dep-date-start 2026-06-15 --dep-date-end 2026-07-15 --seat-class-name economy --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with cheapest option (budget priority)
2. **Grad tip** — note popular grad destinations and timing
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "graduation flight" / "毕业航班" | `--seat-class-name economy --sort-type 3` |
| "class trip" / "同学旅行" | `--seat-class-name economy --sort-type 2` |
| "grad season" / "毕业季" | `--dep-date-start {Jun-1} --dep-date-end {Aug-31} --sort-type 3` |

Grad season in China: June-August. Popular grad destinations: Lijiang, Chengdu, Xiamen, Chongqing, Changsha.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
