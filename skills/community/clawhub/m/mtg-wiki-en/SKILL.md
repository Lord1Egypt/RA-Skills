---
name: mtg-wiki
description: MTG (Magic: The Gathering) comprehensive knowledge base assistant. Answers rules questions, queries cards in Chinese/English, analyzes card interactions, explains formats and strategies, and tells lore. Triggers when users ask about MTG-related topics (card names, rules, formats, strategies, lore) or invoke /mtg-wiki.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: []
    os: ["darwin", "linux"]
---

# MTG Wiki — Magic: The Gathering Knowledge Base Assistant

## Overview

Your all-in-one Magic: The Gathering companion covering **rules, card lookup, interactions, formats, strategies, and lore**. Powered by a local knowledge base including ~187 wiki pages, 37,230-card Oracle database, and complete bilingual CR/MTR/IPG rule documents.

## Knowledge Base Structure

| Directory | Contents |
|-----------|----------|
| `wiki/concepts/` | Rule concepts, mechanics, strategies (~174 pages) |
| `wiki/entities/` | Characters, organizations, products |
| `wiki/sources/` | Source document summaries |
| `wiki/synthesis/` | Comparative analysis |
| `raw/cr/` | Complete Comprehensive Rules (bilingual) |
| `raw/mtr/` | Magic Tournament Rules |
| `raw/ipg/` | Infraction Procedure Guide |

## Core Capabilities

### 1. Rules Lookup (CR/MTR/IPG)

Triggered by: "how does first strike + deathtouch work", "stack resolution order", "layer system"

Workflow:
1. Read relevant concept pages in `wiki/concepts/`
2. For precise rules text, use `rule_search.py` to search the local rules index
3. Cite exact rule numbers (e.g., CR 510.4, CR 613.6)

Key rules quick reference:
- **Layer system**: CR 613 (copy → control → text → type → color → abilities → P/T)
- **APNAP**: CR 101.4 (active player decides first)
- **Stack**: CR 405 (LIFO)
- **State-based actions**: CR 704 (automatic, don't use the stack)

### 2. Card Lookup (Chinese & English Fuzzy Search)

Triggered by: user mentions a card name (in either language, fuzzy, or slang)

Workflow:
1. Call `card_search.py` for unified search
2. Return bilingual card info (name, mana cost, type, rules text, format legality)

Card name format:
- First mention: `Chinese Name (English Name)`
- Subsequent mentions: `Chinese Name`

### 3. Card Interaction Analysis

Triggered by: user describes a multi-card scenario ("what happens if...")

Analysis framework:
- **Layer determination**: identify which layer each effect belongs to → check for cross-layer (613.6) or dependency (613.8)
- **Stack resolution**: APNAP order → LIFO
- **Zone determination**: "permanent" (battlefield only) vs "spell" (stack only)

### 4. Strategy & Format Analysis

Triggered by: user discusses deck archetypes, format selection, banned/restricted lists

Format pages: `standard.md` / `pioneer.md` / `modern.md` / `legacy.md` / `vintage.md`
Commander: `commander.md` / `cedh.md`

### 5. Article Translation

When translating MTG deck guides or strategy articles:
1. Extract card names, use `name_translator.py` for official Chinese translations
2. Standardize terminology
3. Output Markdown with card name reference table and terminology glossary

## Tools

```bash
# Card lookup (supports Chinese/English fuzzy search)
python3 ./raw/tools/mtg_wiki/card_search.py "Lightning Bolt"
python3 ./raw/tools/mtg_wiki/card_search.py "闪电击"

# Rules lookup (by rule number or keyword)
python3 ./raw/tools/mtg_wiki/rule_search.py "101.4"
python3 ./raw/tools/mtg_wiki/rule_search.py "stack"

# Name translation (EN↔CN)
python3 ./raw/tools/mtg_wiki/name_translator.py "Lightning Bolt"
```

API priority:
1. mtgch API (`https://mtgch.com/api/v1/`) — Chinese first, bilingual
2. Scryfall API (`https://api.scryfall.com/`) — English primary
3. Local 37k Oracle DB — offline exact match

## Layer System Quick Reference (CR 613)

| Layer | Effect | Example |
|-------|--------|---------|
| 1 | Copy effects | Clone |
| 2 | Control-changing | Betray |
| 3 | Text-changing | Alter Reality |
| 4 | Type-changing | Blood Moon vs. Urborg |
| 5 | Color-changing | Sleight of Mind |
| 6 | Add/Remove abilities | Tidebinder / Suppression Field |
| 7 | Power/Toughness | Various +/- P/T |

Key distinctions:
- **Cross-layer effects (613.6)**: different parts of the same effect apply in different layers independently, even if the source ability disappears
- **Dependency (613.8)**: only exists when effects are in the **same layer**

## Turn Structure

```
Untap → Upkeep → Draw → Precombat Main → Combat → Postcombat Main → End
```

APNAP (CR 101.4):
- Active player decides first, non-active player decides later
- Multiple triggered abilities go on stack simultaneously via APNAP
- Result: non-active player's triggers **resolve last** (LIFO within APNAP)

## Answering Standards

1. **Prefer wiki citations**: check `wiki/concepts/` first for relevant pages
2. **Precise rule citations**: cite CR/MTR rule numbers, don't answer from memory
3. **Bilingual card names**: use `Chinese (English)` format
4. **Cross-links**: include `[[slug|display]]` references

## Complete Rule Files

| File | Contents |
|------|----------|
| `raw/cr/1.md` | Game concepts, priority, costs |
| `raw/cr/6.md` | **Spells, abilities, layer system (613)** |
| `raw/cr/7.md` | **Keyword abilities (702), keyword actions (701)** |
| `raw/cr/glossarycn.md` | Chinese terminology glossary |

## For Judges

Decision trees: `wiki/branches/referee/decision-trees/`
Analysis frameworks: `wiki/branches/referee/frameworks/`

Judge rules questions must:
1. Decompose by timeline and mechanics
2. Force deep search of keyword actions (check CR 702)
3. Four-step rule text reading: copy fully → circle qualifiers → verify each word → reverse-validate
4. Output compliance report

## Full Knowledge Base

This published skill contains only the core code. For the complete **~187 wiki pages + 37,230 card database + bilingual CR/MTR/IPG rules** (~13MB), clone the full repository:

```bash
git clone https://github.com/RaymondYHH/mtg-skill.git
cd mtg-skill/magic-skill
```

Full repository contents:
- `wiki/` — 187 pages of local knowledge (concepts, entities, sources, synthesis)
- `raw/cr/` — Complete Comprehensive Rules (bilingual)
- `raw/mtr/` — Magic Tournament Rules (bilingual)
- `raw/ipg/` — Infraction Procedure Guide (bilingual)
- `raw/data/` — 37,230-card Oracle database + analysis scripts

After installing, run `python3 raw/tools/mtg_wiki/build_indices.py` to build local indices.

## Notes

- **Always verify specific cards** — use `card_search.py` or API, never from memory
- **Confirm Chinese card names via mtgch** — user input may contain errors or slang
- **Watch for layer系统和时间印记** — identify the layer first for complex interactions
- **Commander rules in CR 903** — extra deck limits, color identity, command tax