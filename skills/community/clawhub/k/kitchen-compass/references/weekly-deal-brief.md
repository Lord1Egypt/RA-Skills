# Weekly Deal Brief and Combined Deal Sheet

_Last updated: 2026-04-19_

## Purpose
Kitchen Compass supports an **optional**, **manual/guided** weekly deal workflow.

This workflow is deliberately split into two layers:
1. **Per-store weekly deal briefs** — curated, store-specific inputs
2. **Combined weekly deal sheet** — one simple grouped view across all selected stores

This is **not** planner-side deal scoring.
Deals remain decision support outside the planner.

## Product truth
- Store setup is manual/guided.
- Retrieval is retailer-specific and may be brittle.
- Kitchen Compass can remember:
  - saved stores
  - source URLs
  - retrieval recipes
  - preferred weekly scan schedule
- Kitchen Compass can prepare a weekly scan packet and combine curated per-store briefs into one grouped output.
- Kitchen Compass does **not** promise autonomous multi-retailer scraping magic.

---

## Canonical files
### Config
- `household/stores.json`
  - `weekly_deal_brief.enabled`
  - `weekly_deal_brief.default_store_ids`
  - `weekly_deal_brief.scan_schedule`
  - `weekly_deal_brief.stores[]`
    - `source`
    - `retrieval_recipe`

### Authored per-store inputs
- `deals/store-briefs/<store-id>.json`
  - one current curated brief per saved store
  - this is the main input for the combined weekly deal sheet

### Legacy single-store input
- `deals/weekly-deal-brief-input.json`
  - still valid for single-store/manual work
  - not the preferred multi-store path

### Generated outputs
- `generated/deals/weekly-deal-scan-latest.json`
- `generated/deals/weekly-deal-scan-latest.md`
- `generated/deals/combined-weekly-deal-sheet-latest.json`
- `generated/deals/combined-weekly-deal-sheet-latest.md`

---

## Weekly scan schedule
Store the preferred scan schedule inside `household/stores.json`:

```json
{
  "weekly_deal_brief": {
    "enabled": true,
    "default_store_ids": ["acme-west-goshen", "giant-boot-rd"],
    "scan_schedule": {
      "day_of_week": "friday",
      "time_local": "12:00",
      "timezone": "America/New_York"
    },
    "stores": []
  }
}
```

### Notes
- This remembers when the household wants the scan to run.
- It does **not** by itself create automation.
- Current validation expects:
  - weekday name like `friday`
  - `HH:MM` 24-hour format
  - IANA timezone like `America/New_York`

---

## Per-store brief input contract
Each store brief file uses the current-week input shape:

```json
{
  "version": 1,
  "week_of": "2026-04-21",
  "store_id": "acme-west-goshen",
  "source": {
    "type": "retailer-page",
    "url": "https://example.com/weekly-ad",
    "captured_at": null,
    "notes": "Use the saved store source/retrieval recipe from household/stores.json."
  },
  "curated_by": "manual",
  "notes": "Keep only the relevant deals for this store.",
  "items": [
    {
      "title": "Chicken thighs or drumsticks",
      "brief_role": "major-protein",
      "display_category": "meat",
      "price_text": "$1.29/lb",
      "regular_price_text": "$1.99/lb",
      "why_it_matters": "Cheap flexible protein for sheet-pan chicken and simple roast dinners.",
      "meal_lanes": ["sheet-pan chicken", "roast chicken + potatoes"]
    }
  ]
}
```

### `brief_role`
Allowed values:
- `major-protein`
- `supporting-ingredient`
- `side`
- `other`

### `display_category`
Allowed values:
- `meat`
- `starch`
- `dairy`
- `fruit-veg`
- `beverages`
- `misc`

Notes:
- `display_category` controls the **combined output grouping**.
- Filtering logic can still use richer meal/recipe judgment behind the scenes.
- If `display_category` is omitted, Kitchen Compass applies a conservative fallback classifier.

### Price display
Use:
- `price_text` for the sale/display price
- `regular_price_text` when you want to show the normal/reference price directly

This is especially useful for stores like Whole Foods where showing both **Prime** and **regular** price is better than forcing discount math.

---

## Combined weekly deal sheet output
The combined output is intentionally simple.

### Grouping
- `MEAT`
- `STARCH`
- `DAIRY`
- `FRUIT / VEGGIE`
- `BEVERAGES`
- `MISC`

### Line format
```text
Store — Product — Sale Price — Normal Price
```

Rules:
- no store location in the display layer
- use em dash separators
- show category headers above grouped items
- omit the normal price fragment when it is unavailable

Example:
```text
## MEAT
- GIANT — Our Brand Boneless Skinless Chicken Breasts — $2.29/lb
- Whole Foods — Air-Chilled Whole Chicken — Prime $2.79/lb — Regular $3.49/lb
```

---

## Commands
### Manage store sources and scan schedule
```bash
python3 scripts/manage_deal_sources.py --data-root /path/to/kitchen-compass-data show
python3 scripts/manage_deal_sources.py --data-root /path/to/kitchen-compass-data set-scan-schedule \
  --day-of-week friday \
  --time-local 12:00 \
  --timezone America/New_York
```

### Prepare the weekly scan packet + per-store stubs
```bash
python3 scripts/prepare_weekly_deal_scan.py --data-root /path/to/kitchen-compass-data --week-of 2026-04-21
```

This will:
- select the default weekly-deal stores (or all active stores if no defaults are set)
- create `deals/store-briefs/<store-id>.json` stubs if missing
- write the scan packet under `generated/deals/`

### Render the combined weekly deal sheet
```bash
python3 scripts/render_combined_weekly_deal_sheet.py --data-root /path/to/kitchen-compass-data
```

This will:
- read all selected store briefs
- normalize them against saved store setup
- write the combined JSON + markdown outputs under `generated/deals/`

---

## What this feature does NOT promise
- It does not promise autonomous retailer scraping.
- It does not promise that every store works the same way.
- It does not treat deals as planner scoring input.
- It does not hide brittleness in retailer-specific flows.

The honest MVP is:
- save the store once
- save what retrieval recipe worked
- curate the relevant weekly store brief
- let Kitchen Compass combine the information cleanly

---

## Definition of done
This feature is real when:
- saved stores include source + retrieval recipe
- preferred scan schedule can be stored and validated
- a weekly scan packet can be prepared for the selected stores
- per-store weekly brief files can be curated and validated
- a combined grouped weekly deal sheet can be rendered from those saved store briefs
