---
name: print-failure-analyst
description: Diagnose 3D printing failures and recommend slicer setting fixes. Maintains a personal failure log to track recurring problems. Use when: user says "print failed", "3d print problem", "why did my print fail", "print diagnosis", or mentions stringing, warping, layer adhesion, delamination, under extrusion, over extrusion, elephant foot, layer shifting, bridging, pillowing, ringing, ghosting, z-banding, clogged nozzle, wet filament, first layer issues, seam visibility, or asks about slicer settings for a specific failure. Also triggers on "log a failure", "failure history", "print failure report".
---

# Print Failure Analyst

Diagnose failures, recommend slicer fixes, and track a personal failure log.

## References

- `references/failure-types.md` — 18 failure types with keywords, causes, visual symptoms
- `references/slicer-fixes.md` — Specific values for PrusaSlicer, Cura, OrcaSlicer per failure type

Read these when formulating diagnoses or recommending fixes. Do not recite them wholesale — extract relevant sections.

## Scripts

All scripts use Python stdlib only. Log stored at `assets/failure-log.json`.

### diagnose.py — Identify failure mode from symptoms

```bash
python3 scripts/diagnose.py --symptoms "stringing,warping"
python3 scripts/diagnose.py --description "hair between parts and corners lifting"
python3 scripts/diagnose.py --symptoms "stringing" --description "worse at layer transitions" --json
```

Outputs: ranked failure types with confidence, causes, and slicer-specific fixes.
Use `--json` when you need structured output to reason over.

### log_failure.py — Record a print failure

```bash
python3 scripts/log_failure.py \
  --printer "Prusa MK4" \
  --material "PETG" \
  --failure-type "stringing" \
  --description "Heavy stringing between towers" \
  --slicer-settings '{"temperature": 235, "retraction_distance_mm": 1.0}' \
  --fixed-by "Reduced temp to 230C, enabled wipe" \
  --notes "Filament may be wet"
```

Valid `--failure-type` values: `stringing`, `warping`, `layer_adhesion`, `under_extrusion`, `over_extrusion`, `elephant_foot`, `layer_shifting`, `bridging`, `overhang`, `clog`, `pillowing`, `ringing`, `z_banding`, `seam`, `supports`, `first_layer`, `wet_filament`, `spaghetti`, `other`

### history.py — View failure history and patterns

```bash
python3 scripts/history.py                          # All failures
python3 scripts/history.py --last 10               # Last 10
python3 scripts/history.py --material PETG         # Filter by material
python3 scripts/history.py --printer "Prusa MK4"  # Filter by printer
python3 scripts/history.py --failure-type stringing
python3 scripts/history.py --patterns              # Pattern analysis only
```

### report.py — Generate markdown report

```bash
python3 scripts/report.py                  # Print to stdout
python3 scripts/report.py --output r.md   # Save to file
python3 scripts/report.py --days 30       # Last 30 days only
```

## Workflow

### User describes a failure
1. Run `diagnose.py --symptoms` or `--description` with the user's input
2. Read `references/failure-types.md` for the top match to get full context
3. Read `references/slicer-fixes.md` for that failure type to get specific values
4. Present: most likely failure type, top 2–3 causes, and slicer fixes (ask which slicer if unknown)
5. Offer to log the failure with `log_failure.py`

### User provides an image
1. Analyze the image to identify visual symptoms (stringing, warping, layer gaps, etc.)
2. Map observed symptoms to failure type keywords from `references/failure-types.md`
3. Run `diagnose.py --symptoms "<observed symptoms>"` for structured output
4. Present diagnosis with causes and fixes

### User asks to log a failure
- Collect: printer, material, failure type, description. Ask for missing required fields.
- Optional: slicer settings used, what fixed it, notes
- Run `log_failure.py` with collected info

### User asks for history or patterns
- Run `history.py` with appropriate filters
- Highlight any patterns flagged (recurring type+material combos, worst printer/material)

### User asks for a report
- Run `report.py`, optionally with `--days` if user wants a time-bounded view
- Present the markdown output or save it and tell user where it is
