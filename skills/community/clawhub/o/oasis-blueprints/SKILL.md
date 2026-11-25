---
name: oasis-blueprints
description: Create or revise construction drawing sheets as self-contained HTML and scaled PDFs, with plans, sections, details, title blocks, and tracked open items. Use for HTML drawing sets and permit-sheet drafting; not for structural design calculations or native CAD/DWG editing.
version: 0.4.0
homepage: https://docs.oasisengineering.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📐",
        "homepage": "https://docs.oasisengineering.com",
        "requires": { "anyBins": ["python3", "python"] },
      },
  }
---

# Oasis Blueprints

Draft a drawing set from project evidence: one editable, self-contained HTML file and, when available,
a 36 × 24 in landscape PDF. The kit supplies a cover, one field sheet, and optional reserved sheets.
It draws geometry and checks layout; it does not calculate structural adequacy or establish approval.

## Preserve the engineering record

- Use the user's dimensions, decisions, and supplied project documents. Identify the source and
  revision of engineering values; distinguish proposed values from engineer-approved requirements.
  Resolve conflicting sources before showing a value as settled.
- Do not invent member sizes, spacing, connectors, anchors, embedment, footings, loads, capacities,
  or code editions to complete a drawing. Track missing requirements as keyed `openItems`. An
  explicitly requested engineering analysis is separate from this drafting kit.
- Sample projects demonstrate layout, not suitable designs. Replace sample addresses, branding,
  notes, geometry, and criteria with this project's evidence. Mark schematic geometry clearly;
  do not dimension it as a selected design. Mark scanned, scaled, or assumed dimensions ± and
  identify what needs field verification.
- An entered answer records information; it does not establish who approved it. Preserve its
  source and verification status in the item text or project notes. Keep new sets `draft` by default.
  Use `review` when requested; change to `permit` or `construction` only on explicit direction
  confirming engineer review and closure of all outstanding items. Never add a seal or signature.

## Start from the project

Inspect the relevant project files and existing drawing before asking for missing information.
Collect scope, location, geometry and units, new versus existing work, supplied member/connection
requirements, and title-block details. Ask only for information needed to proceed; record other
unknowns as open items. A returned edited HTML or `.project.json` takes precedence over the older
project copy for the user's edits. Preserve unrelated work and version standalone revisions.

Reuse a verified project `brand.json` or supplied company details. If creating one, adapt
[assets/brand.example.json](assets/brand.example.json); leave unavailable fields blank and identify
those gaps. Use the actual company name as a wordmark when no logo is available. Do not substitute
sample branding or infer a license number.

## Choose the drawing resources

| Job type | Use | Resource |
|---|---|---|
| `deck` | Freestanding rectangular deck; inches or millimetres | [assets/views/deck.js](assets/views/deck.js) |
| `sunroom` | Sloped roof on posts against a house; inches only | [assets/views/sunroom.js](assets/views/sunroom.js) |
| `library` | A set made only of sheets of standard details | [assets/views/library.js](assets/views/library.js) |
| Custom | A scope the supplied views do not represent | Read [references/writing-views.md](references/writing-views.md), then adapt `deck.js` beside the project file |

The standalone skill ZIP includes the libraries under `assets/library/` in this skill folder.
For a repository/plugin checkout, use `library/` at the repository root instead. Standard details
live in `details/<collection>/index.json` under that library root. Search an index by title or category, then place details on
a sheet of type `details` by id, as described in references/project-file.md. A library detail is the
engineer's drawing: add one only when the engineer of record says it applies, never edit the sizes or
notes inside it, and say when its index entry shows it has not been checked by the engineer.

The library root also has a drawing map: `drawing-map/types/<type>__<variant>.json` lists the sheets,
details and note blocks that past sets of a project type contained, and `type-map.json` says how
each sheet kind is handled by the kit and which detail categories to search. When the user names a project
type, use them to propose a sheet index and candidate details, add sheets the kit cannot draw as `reserved`,
and record the proposal as an open item for the engineer. The map counts past sets; it is never a
requirement, and a type built from fewer than three sets is thin evidence. Say so.

Keep job-specific drawing code beside the project, not inside the installed skill. Never force a
project into an incompatible example. For each new or revised project, read
[references/project-file.md](references/project-file.md) for the JSON contract and
[references/sheet-standard.md](references/sheet-standard.md) for scale, status, and sheet conventions.
Use [assets/samples/](assets/samples/) as schema samples only.

Keep all lengths in the declared unit system. Check positive dimensions and spacing, ordered
coordinates, consistent units, and nonzero scale denominators before rendering. Do not convert an
imperial project by changing only its `units` label. A custom view must validate its own geometry.

Give each open item a unique key. Use `{key}` in text and `answer(P, key)` in the view so the same
answer appears throughout. Blank design criteria also remain outstanding. When an answer changes
geometry, update the numeric geometry and related notes; entering answer text alone does not resize
members, footings, or connections.

## Build, inspect, and export

`{baseDir}` is this skill's installed folder. Quote absolute paths when the
project is elsewhere or paths contain spaces. These examples assume the skill folder is current:

```bash
python {baseDir}/scripts/build.py /path/to/project.json /path/to/sheet-set.html --brand /path/to/brand.json
python {baseDir}/scripts/print.py /path/to/sheet-set.html /path/to/sheet-set.pdf --png /path/to/preview-
```

Omit `--brand` if none is supplied; the builder also checks beside the project and in the current
folder. Use `--view /path/to/custom.js` for an explicitly selected view. Build requires only Python's
standard library. PDF export and automated layout checks need Python Playwright plus Chromium
(`python -m pip install playwright`, then `python -m playwright install chromium`) in that same
Python environment. Prefer an available environment over changing system-wide dependencies.

`print.py` exits 2 for layout/audit or script errors. Inspect the findings, correct their cause,
rebuild, and rerun. Do not present a failed export as checked. Inspect every preview for overlaps,
clipped notes, misplaced leaders, and legible dimensions. Verify PDF page size and measured-view
scale; a 192 in span at 1:24 must occupy 8 in. Print at 100% on the specified paper size; resizing
changes physical scale. The isometric illustration is not to scale.

If PDF tooling is unavailable, deliver the HTML with that limitation stated. Open it in an available
browser to inspect its layout badge and drawing, or state that visual/layout checking remains
unverified. Manual Chrome/Edge Print / Save as PDF is an alternative, using actual size and the
specified paper. Do not describe the layout audit as structural verification.

## Deliver and revise

Provide the HTML and any checked PDF, the count and nature of open items, the set's actual status,
and material assumptions or field checks. Briefly explain **Edit**, **Download project file**,
**Download this HTML with my edits**, and **Print / Save as PDF** as relevant. Keep the editable
project JSON and custom view with the project for later revisions; rebuild and recheck after edits.

The current kit has one field sheet per set and fixed 36 × 24 in paper. Larger or different layouts
require deliberate implementation and validation, not an unsupported promise in the deliverable.

The reusable engine, layout, editor, and styles are in `assets/kit/`; embedded Barlow fonts and their
license are in `assets/fonts/`. Keep these resources with the skill.
The built HTML carries a source and license note in its head and at the top of the embedded kit code. It
is not printed; leave it in place when editing a set.
