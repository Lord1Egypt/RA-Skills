---
name: infant-flights
displayName: "Book Infant Flights — Baby Travel, Bassinet Seats, Child Fare Tickets"
description: "Book infant flights, baby travel tickets and bassinet seat options with child fare and infant-in-arm booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: infant-flights

## Overview

Book infant flights — baby travel, bassinet seats, and child fare tickets. For parents traveling with infants and young children.

## When to Activate

User query contains:
- English: "infant flight", "baby flight", "bassinet seat", "child fare", "travel with baby", "infant ticket"
- Chinese: "婴儿机票", "宝宝航班", "婴儿摇篮", "儿童机票", "带婴儿乘机", "婴儿票"

Do NOT activate for: family trip planning (flights+hotel) → `family-trip`; student fares → `student-deal`

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
| `--dep-hour-start` | No | Default: 6 (avoid early morning rush) |
| `--dep-hour-end` | No | Default: 20 (avoid late arrivals with baby) |
| `--sort-type` | No | **Default: 4** (duration ascending — shortest trip for baby comfort) |
| `--journey-type` | No | 1=direct (strongly preferred with infants), 2=connecting |
| `--seat-class-name` | No | economy / business / first |
| `--max-price` | No | Price ceiling in CNY |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `4` | Duration ascending | **Default** — shortest trip for baby comfort |
| `8` | Direct flights first | No transfers — essential with infants |
| `2` | Recommended | Best overall options |
| `3` | Price ascending | Cheapest infant-eligible fares |

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

### Playbook A: Shortest Infant-Friendly Flight

**Trigger:** "infant flights", "婴儿机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 20 --sort-type 4
```

**Output:** Shortest duration flights within comfortable hours.

### Playbook B: Direct-Only Infant Flight

**Trigger:** "direct flight with baby", "带宝宝直飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 20 --journey-type 1 --sort-type 8
```

**Output:** Direct flights only — no transfers with infant.

### Playbook C: Cheapest Infant Flight

**Trigger:** "cheapest baby ticket", "最便宜婴儿票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest fares (removes hour filter for maximum options).

### Playbook D: Broad Search (no suitable flights)

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} infant flights"
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
- [ ] Direct flights prioritized for infant comfort?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-01 --dep-hour-start 6 --dep-hour-end 20 --sort-type 4
```
```bash
flyai search-flight --origin "Shanghai" --destination "Sanya" --dep-date 2026-06-01 --dep-hour-start 6 --dep-hour-end 20 --journey-type 1 --sort-type 8
```

## Output Rules

1. **Conclusion first** — lead with shortest/direct flight
2. **Baby travel tips** — remind about bassinet request, infant fare rules, and carry-on milk policy
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate infant fare rates or airline policies

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "infant flight" / "婴儿机票" | `--dep-hour-start 6 --dep-hour-end 20 --sort-type 4` |
| "direct with baby" / "带宝宝直飞" | add `--journey-type 1 --sort-type 8` |
| "cheapest infant" / "最便宜婴儿票" | add `--sort-type 3` (no hour filter) |
| "round-trip infant" / "婴儿往返" | add `--back-date {date}` |

CLI does not have an infant-age or passenger-type parameter. Infant tickets (under 2 years, no seat) and child tickets (2-12 years, discounted seat) are handled at booking stage. Direct flights are strongly preferred to minimize baby distress during transfers.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
