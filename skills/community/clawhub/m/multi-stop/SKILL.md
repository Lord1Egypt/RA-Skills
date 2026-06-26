---
name: multi-stop
description: "Plan complex multi-city flight itineraries — A to B to C to D. Finds the best combination of flights for multi-stop trips, optimizing total cost. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI command output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: multi-stop

## Overview

Plan complex multi-city flight itineraries — A to B to C to D. Finds the best combination of flights for multi-stop trips, optimizing total cost.

## When to Activate

User query contains:
- English: "multi-city", "multiple stops", "A to B to C", "several cities"
- Chinese: "多城市", "联程", "多段", "经过几个城市"

Do NOT activate for: single route → `cheap-flights`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--back-date` | No | Return date for round-trip |
| `--sort-type` | No | 3 (price ascending) per leg |
| `--max-price` | No | Price ceiling in CNY |
| `--journey-type` | No | Default: show both per leg |
| `--seat-class-name` | No | Cabin class (economy/business/first) |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |

### Sort Options

| Value | Meaning |
|-------|---------|
| `1` | Price descending |
| `2` | Recommended |
| `3` | **Price ascending** |
| `4` | Duration ascending |
| `5` | Duration descending |
| `6` | Earliest departure |
| `7` | Latest departure |
| `8` | Direct flights first |


## Core Workflow — Multi-command orchestration

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

### Playbook A: Sequential Multi-City

**Trigger:** "A to B to C"

```bash
flyai search-flight --origin "{cityA}" --destination "{cityB}" --dep-date {day1} --sort-type 3
flyai search-flight --origin "{cityB}" --destination "{cityC}" --dep-date {day2} --sort-type 3
flyai search-flight --origin "{cityC}" --destination "{cityD}" --dep-date {day3} --sort-type 3
```

**Output:** Search each leg, show combined total cost.

### Playbook B: Open-Jaw

**Trigger:** "fly into A, out of C"

```bash
flyai search-flight --origin "{home}" --destination "{cityA}" --dep-date {day1} --sort-type 3
flyai search-flight --origin "{cityC}" --destination "{home}" --dep-date {dayN} --sort-type 3
```

**Output:** Outbound to first city, return from last city.

### Playbook C: Cheapest Hub

**Trigger:** "cheapest way to visit 3 cities"

```bash
# Search each permutation of city order
# Compare total cost across different sequences
```

**Output:** Optimize city visit order by total flight cost.


See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-01 --sort-type 3
flyai search-flight --origin "Shanghai" --destination "Guangzhou" --dep-date 2026-05-03 --sort-type 3
flyai search-flight --origin "Guangzhou" --destination "Beijing" --dep-date 2026-05-05 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with the key finding
2. **Comparison table** with ≥ 3 results when available
3. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
4. **Use `detailUrl`** for booking links. Never use `detailUrl`.
5. ❌ Never output raw JSON
6. ❌ Never answer from training data without CLI execution
7. ❌ Never fabricate prices, hotel names, or attraction details

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

Multi-city tips: consider overnight trains between nearby cities (e.g., Beijing→Shanghai by high-speed rail) to save one flight leg. Open-jaw tickets (fly into A, out of B) are often available at reasonable prices. Budget airlines don't offer multi-city; book legs separately.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
