# Menu Engineering Analysis

**Platforms:** Claude · Openclaw · Codex
**Domain:** Hospitality

## Purpose

Runs a Kasavana-Smith menu-engineering analysis on a single restaurant menu over a defined sales period. Computes per-item contribution margin and popularity, classifies each item as Star / Plowhorse / Puzzle / Dog, and produces an action playbook by class — promote, re-engineer, reposition, or remove. Designed for the chef, GM, or multi-unit operator who needs an evidence-anchored review before reprinting, repricing, or re-platforming a menu.

## When to Use

- Restaurant chef or GM running a quarterly menu review
- Multi-unit operator standardizing menu mix across locations
- Culinary director re-engineering recipes to hit a target food-cost percentage
- Marketing or design lead preparing a menu redesign and needing item-level priorities
- Owner-operator preparing a price-increase plan and needing per-item evidence

## What It Does

**Phase 1: Intake**
1. Captures the menu scope, sales period, currency, and target food-cost percentage
2. Walks each menu item through required fields: name, category, selling price, food cost, units sold
3. Flags missing or implausible data before any calculation

**Phase 2: Calculation & Classification**
4. Computes per-item contribution margin (price − food cost), food-cost %, total CM, and popularity share
5. Calculates the menu-wide CM threshold (weighted-average CM) and popularity threshold (`(1 / item-count) × 0.7`, the Kasavana-Smith convention)
6. Classifies each item: Star (high CM, high popularity), Plowhorse (low CM, high popularity), Puzzle (high CM, low popularity), Dog (low CM, low popularity)

**Phase 3: Recommendations**
7. Produces an action playbook by class with concrete moves (hold price, raise price, re-engineer recipe, reposition on menu, rename, replace, remove)
8. Surfaces Top-3 quick wins ranked by expected CM impact
9. Recommends menu-design moves (placement, eye anchors, descriptive copy, decoy pricing) tied to the classifications
10. Lists data-quality flags and unresolved questions

## Output

A structured DRAFT menu-engineering report: scope header, data-quality flags, per-item calculation table with classification, four per-class action playbooks, Top-3 quick wins, menu-design recommendations, and an unresolved-information list. Labeled for operator review before any price change, recipe change, or menu reprint.

## Safety Notes

The skill never publishes price changes, never sends data to delivery platforms or POS systems, and never claims an exact profit lift. All recommendations are advisory — operator judgment on brand, guest expectations, supply continuity, and labor capacity is required before execution. The skill treats per-item cost, vendor terms, and unit-level sales data as confidential and never reuses them in examples.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.