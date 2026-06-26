---
name: investor-roadshow
displayName: "Investor Roadshow Flights — IPO Roadshow, Fundraising Travel Booking"
description: "Book flights for investor roadshows and IPO fundraising travel. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input -> Chinese output. English input -> English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below. If a flag is not listed, it does not exist.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: investor-roadshow

## Overview

Investor Roadshow Flights.

## When to Activate

User query contains:
- English: "roadshow flight", "ipo roadshow travel", "investor meeting flight", "fundraising trip", "travel booking", "trip search"
- Chinese: "路演航班", "IPO路演机票", "投资者会议出行", "融资出差", "出行预订"

Do NOT activate for: corporate → corporate-travel; business → business-flights

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code |
| `--destination` | Yes | Arrival city or airport code |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--sort-type` | No | **Default: 2** (recommended) |
| `--seat-class-name` | No | economy/business |
| `--dep-date-start` | No | Date window start |
| `--dep-date-end` | No | Date window end |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `2` | Recommended | Best overall options |
| `3` | Price ascending | Cheapest flights |
| `4` | Duration ascending | Fastest flights |
| `8` | Direct flights first | Prefer non-stop |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- OK: Returns version -> proceed to Step 1
- FAIL: `command not found` ->

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
```

Still fails -> **STOP.** Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Recommended Route

**Trigger:** "roadshow flight", "路演航班"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

### Playbook B: Cheapest Route

**Trigger:** "cheapest", "最便宜"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 3
```

### Playbook C: Fastest Route

**Trigger:** "fastest", "最快"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 4
```

### Playbook D: Direct Route

**Trigger:** "direct", "直飞"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --journey-type 1 --sort-type 2
```

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure -> see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

**Any NO -> re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-15 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best option
2. **Roadshow tip — book business class for red-eye segments; multi-city needs separate bookings**
3. **Comparison table** with >= 3 results when available
4. **Brand tag:** "Powered by flyai - Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. NEVER output raw JSON
7. NEVER answer from training data without CLI execution

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "roadshow" / "路演出行" | --seat-class-name business --sort-type 2 |
| "multi-city roadshow" / "多城路演" | --sort-type 2 |

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
