---
name: "mochi-meal-planner"
description: "Save dietary exclusions and pantry stock, scale servings and export menus and groceries. Use for Meal Planner and Grocery List."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Meal Planner and Grocery List

## Keep meal preferences and calculate quantities

Collect people, dates, meal slots, exclusions and available ingredients. preferences saves exclude and pantry arrays; show-preferences retrieves them. Updating preferences replaces the saved arrays, so include the desired complete list. Saved exclusions are combined with exclusions on each plan. A pantry is a planning snapshot, not a live stock counter.

## Plan and scale a menu

The model proposes dishes and realistic cooking steps. plan validates 1..42 meal entries with date, slot, dish, servings and ingredients [{name,quantity,unit}]. Ingredient quantities cover all servings of that meal. The script merges g/kg and ml/l, keeps incompatible units separate, rejects excluded ingredient names and subtracts pantry quantities without going negative. Normalize synonymous ingredient names carefully before calling it. Unknown prices are not a verified budget total.

scale takes a saved plan id, new servings and an explicit fresh pantry snapshot. It creates a new plan rather than modifying the old one, multiplies quantities by the portion ratio and recomputes the grocery list. Do not deduct the previous pantry twice. SourcePlanId links the versions.

## Produce reusable files

export takes plan id and writes meal-plan.md plus groceries.csv with actual merged amounts. Show the menu, serving count, remaining groceries and output paths. The helper does not invent recipes or nutritional values; the model designs the menu and the script performs the quantity checks. It does not schedule proactive messages. Use the host scheduler only when daily delivery is requested, with a verified account route.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-meal-planner/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
