---
name: one-way
displayName: "Search One-Way Flights — Single-Trip Tickets, No Return, Open-Ended Travel"
description: "Search one-way flights, single-trip tickets and open-ended travel bookings with no return date required. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: one-way

## Overview

Search one-way flights — single-trip tickets, no return, open-ended travel. For travelers who don't need a round-trip booking.

## When to Activate

User query contains:
- English: "one-way flight", "single trip", "one way ticket", "no return flight", "one-way only", "open-ended flight"
- Chinese: "单程机票", "单程票", "不回程航班", "单程航班", "单程出行", "单飞"

Do NOT activate for: round-trip flights → `round-trip`

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--sort-type` | No | **Default: 3** (price ascending — cheapest one-way first) |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--seat-class-name` | No | economy / business / first |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |
| `--max-price` | No | Price ceiling in CNY |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `3` | Price ascending | **Default** — cheapest one-way |
| `4` | Duration ascending | Fastest one-way |
| `2` | Recommended | Best overall one-way options |
| `8` | Direct flights first | Non-stop one-way |

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

### Playbook A: Cheapest One-Way

**Trigger:** "one-way flights", "单程机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest one-way flights. **Never add `--back-date`.**

### Playbook B: Flexible Date One-Way

**Trigger:** "cheapest one-way any day", "单程哪天最便宜"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
```

**Output:** Cheapest one-way across a 7-day window.

### Playbook C: Direct One-Way

**Trigger:** "direct one-way flight", "单程直飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

**Output:** Direct one-way flights only.

### Playbook D: Broad Search (no one-way found)

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} one-way flights"
```

**Output:** Broader search + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?
- [ ] No `--back-date` was used (one-way only)?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-01 --sort-type 3
```
```bash
flyai search-flight --origin "Shanghai" --destination "Chengdu" --dep-date-start 2026-06-01 --dep-date-end 2026-06-07 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with cheapest one-way fare
2. **One-way indicator** — clearly label as one-way, no return included
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never add `--back-date` — this is a one-way skill

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "one-way flight" / "单程机票" | `--sort-type 3` (no `--back-date`) |
| "cheapest one-way" / "最便宜单程" | add `--sort-type 3` |
| "flexible one-way" / "日期灵活单程" | add `--dep-date-start "{date-3}" --dep-date-end "{date+3}"` |
| "direct one-way" / "单程直飞" | add `--journey-type 1 --sort-type 8` |
| "budget one-way" / "预算内单程" | add `--max-price {budget}` |

One-way tickets are sometimes more expensive per-segment than round-trip. If user mentions return needs, redirect to `round-trip`. Never add `--back-date` in this skill.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
