---
name: last-minute
displayName: "Book Last Minute Flights — Same-Day Tickets, Urgent Departures, Emergency Travel"
description: "Book last minute flights, same-day tickets and urgent departures with emergency travel options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: last-minute

## Overview

Book last minute flights — same-day tickets, urgent departures, and emergency travel. For travelers who need to fly NOW, not tomorrow.

## When to Activate

User query contains:
- English: "last minute flight", "same-day flight", "urgent flight", "emergency flight", "fly today", "last minute ticket"
- Chinese: "临期航班", "当天机票", "紧急机票", "说走就走", "今晚机票", "马上飞"

Do NOT activate for: cheap/budget flights without urgency → `economy-flights`; red eye specifically → `red-flights`

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD`. **Default: today** |
| `--dep-hour-start` | No | Departure hour filter start (0-23). Default: current hour |
| `--dep-hour-end` | No | Departure hour filter end (0-23). Default: 23 |
| `--sort-type` | No | **Default: 6** (earliest departure — fly ASAP) |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--seat-class-name` | No | economy / business / first. Default: economy |
| `--max-price` | No | Price ceiling in CNY |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `6` | Earliest departure | **Default** — fly ASAP |
| `7` | Latest release | Freshly added last-minute inventory |
| `3` | Price ascending | Cheapest among last-minute |
| `4` | Duration ascending | Fastest route |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- ✅ Returns version → proceed to Step 1
- ❌ `command not found` →

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
```

Still fails → **STOP.** Tell user to run `npm i -g @fly-ai/flyai-cli` manually. Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Same-Day Urgent

**Trigger:** "fly today", "当天机票", "马上飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --dep-hour-start {now+1} --sort-type 6
```

**Output:** Flights departing within hours, earliest first.

### Playbook B: Tomorrow Morning

**Trigger:** "tomorrow morning flight", "明早航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --dep-hour-start 6 --dep-hour-end 12 --sort-type 6
```

**Output:** Morning flights for tomorrow, earliest departure first.

### Playbook C: Within 3 Days Bargain

**Trigger:** "last minute deal this week", "这几天有便宜票吗"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {today} --dep-date-end {today+3} --sort-type 3
```

**Output:** Cheapest flights within the next 3 days.

### Playbook D: Broad Search (no last-minute found)

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6
flyai keyword-search --query "{origin} to {destination} last minute flights today"
```

**Output:** Broader search without hour filter + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?
- [ ] All results are for near-term dates (today/tomorrow)?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-04-14 --dep-hour-start 14 --sort-type 6
```
```bash
flyai search-flight --origin "Guangzhou" --destination "Chengdu" --dep-date 2026-04-15 --dep-hour-start 6 --dep-hour-end 12 --sort-type 6
```

## Output Rules

1. **Conclusion first** — lead with earliest departing flight
2. **Urgency indicator** — show "departs in X hours" for same-day flights
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate prices, flight numbers, or schedules

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "last minute" / "临期航班" | `--dep-date {today} --sort-type 6` |
| "fly today" / "当天机票" | `--dep-date {today} --dep-hour-start {now+1}` |
| "tomorrow morning" / "明早航班" | `--dep-date {tomorrow} --dep-hour-start 6 --dep-hour-end 12` |
| "within 3 days" / "这几天" | `--dep-date-start {today} --dep-date-end {today+3}` |
| "cheapest last minute" / "最便宜临期票" | add `--sort-type 3` instead of 6 |
| "direct only" / "只看直飞" | add `--journey-type 1` |
| "under budget" / "预算内" | add `--max-price {budget}` |

Last-minute inventory changes rapidly. If 0 results for tonight, try expanding to tomorrow or removing hour filters. Same-day flights after 21:00 may overlap with red-eye category.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
