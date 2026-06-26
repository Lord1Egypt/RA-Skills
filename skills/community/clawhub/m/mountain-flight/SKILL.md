---
name: mountain-flight
displayName: "Fly to Mountains — Ski Resorts, Highland Cities, Alpine Destinations"
description: "Fly to mountains, search ski resort flights and highland city flights with alpine destination booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: mountain-flight

## Overview

Fly to mountains — ski resorts, highland cities, alpine destinations. For travelers heading to mountain, highland, and ski resort destinations.

## When to Activate

User query contains:
- English: "mountain flight", "ski resort flight", "highland flight", "alpine flight", "fly to mountains", "hill station flight"
- Chinese: "山区航班", "滑雪航班", "高原航班", "山区机票", "山地出行", "高海拔航班"

Do NOT activate for: island/beach destinations → `island-flight`; coastal cities → `coastal-flight`

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
| `2` | Recommended | **Default** — best mountain route options |
| `3` | Price ascending | Budget mountain getaway |
| `4` | Duration ascending | Quick mountain escape |
| `8` | Direct flights first | Prefer non-stop to mountain airports |

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

### Playbook A: Recommended Mountain Route

**Trigger:** "fly to mountains", "山区航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights to mountain destinations.

### Playbook B: Ski Season Flight

**Trigger:** "ski resort flight", "滑雪航班", "雪场机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {ski_start} --dep-date-end {ski_end} --sort-type 3
```

**Output:** Cheapest flights during ski season window.

### Playbook C: Highland City Direct

**Trigger:** "direct flight to highland", "高原直飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to highland cities.

### Playbook D: Broad Search (no mountain flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} mountain ski resort flights"
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
flyai search-flight --origin "Beijing" --destination "Lijiang" --dep-date 2026-07-15 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best mountain-compatible option
2. **Altitude note** — remind user about altitude sickness for highland destinations
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate mountain weather or road conditions

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "mountain flight" / "山区航班" | `--sort-type 2` |
| "ski resort" / "滑雪航班" | `--dep-date-start {Dec-1} --dep-date-end {Mar-31} --sort-type 3` |
| "highland direct" / "高原直飞" | `--journey-type 1 --sort-type 2` |
| "alpine destination" / "高山目的地" | `--sort-type 8` (direct first) |

Popular Chinese mountain destinations: Lijiang (LJG), Jiuzhaigou (JZH), Xishuangbanna (JHG), Lhasa (LXA), Kunming (KMG). Ski: Zhangjiakou, Changbaishan (NBS), Altay (AAT).

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
