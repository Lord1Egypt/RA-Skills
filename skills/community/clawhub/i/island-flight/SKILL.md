---
name: island-flight
displayName: "Fly to Islands — Island Destinations, Beach Flights, Tropical Route Booking"
description: "Fly to islands, search island destination flights and beach flights with tropical route booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: island-flight

## Overview

Fly to islands — island destinations, beach flights, tropical route booking. For travelers heading to island and beach destinations.

## When to Activate

User query contains:
- English: "island flight", "beach flight", "tropical flight", "fly to island", "island destination", "seaside flight"
- Chinese: "海岛航班", "海岛机票", "海岛游", "海岛出行", "热带海岛", "海滨航班"

Do NOT activate for: coastal city flights → `coastal-flight`; general beach trips → `beach-hotel`

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
| `--journey-type` | No | 1=direct, 2=connecting |
| `--max-price` | No | Price ceiling in CNY |
| `--dep-date-start` | No | Date range start |
| `--dep-date-end` | No | Date range end |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `2` | Recommended | **Default** — best island route options |
| `3` | Price ascending | Budget island getaway |
| `4` | Duration ascending | Quick island escape |
| `8` | Direct flights first | Prefer non-stop to islands |

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

Still fails → **STOP.** Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Recommended Island Route

**Trigger:** "fly to island", "海岛航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to island destinations, recommended first.

### Playbook B: Budget Island Getaway

**Trigger:** "cheap island flight", "便宜海岛机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest flights to island within date range.

### Playbook C: Connecting Island Route

**Trigger:** "connecting flight to island", "中转海岛"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 2
```

**Output:** Connecting flights for islands without direct service.

### Playbook D: Broad Search (no island flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} island flights beach tropical"
```

**Output:** Broader search + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Shanghai" --destination "Sanya" --dep-date 2026-07-15 --journey-type 1 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best island-compatible option
2. **Island tip** — note ferry/transfer requirements for specific islands
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate island flight schedules or ferry connections

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "island flight" / "海岛航班" | `--journey-type 1 --sort-type 2` |
| "cheap island" / "便宜海岛" | `--sort-type 3` with date range |
| "tropical island" / "热带海岛" | `--sort-type 2` (recommended) |
| "beach destination" / "海滨目的地" | `--journey-type 1 --sort-type 8` (direct first) |

Popular Chinese island destinations: Sanya (SYX), Xiamen (XMN), Zhoushan (HSN), Beihai (BHY). International: Phuket (HKT), Bali (DPS), Malé (MLE), Okinawa (OKA).

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
