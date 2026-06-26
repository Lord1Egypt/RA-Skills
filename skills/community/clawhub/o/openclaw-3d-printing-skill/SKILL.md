---
name: parametric-3d-printing
description: Create parametric 3D-printable parts and enclosures with CadQuery, export STL or 3MF files, render review previews, and iterate on fit, tolerances, and printability. Use when the user wants a printable physical object such as a bracket, mount, enclosure, case, adapter, lid, organizer, fixture, or mechanical part; when they mention 3D printing, STL, 3MF, CadQuery, OpenSCAD, snap-fits, wall thickness, tolerances, screw bosses, or printer-specific constraints. Do not use for game assets, animation, sculpting, artistic rendering, photogrammetry, or editing an existing mesh without rebuilding it parametrically.
---

# Parametric 3D Printing

Design brackets, clips, cable guides, holders, mounts, adapters, enclosures, fixtures, and other functional 3D-printable parts with CadQuery. Generate clean STL or 3MF outputs, review fit and printability, and iterate quickly.

Use CadQuery as the default modeling path. Keep models parametric, dimensioned in millimeters, and easy to revise.

## Workflow

1. Clarify the object, the must-fit dimensions, and the attachment method.
2. Research exact dimensions for any real-world device or connector before modeling.
3. Build in phases:
   - base shape
   - functional features
   - finishing details
4. After each meaningful phase, export an STL, render a preview, and review it before moving on.
5. Deliver the final model with a short slicer recommendation.

Do not jump straight to a finished complex model unless the part is trivial.

## Gather requirements conversationally

Ask only what is needed to unblock the design. Prefer this order:

- what the part does
- critical dimensions
- how it mounts or mates
- printer, material, and nozzle assumptions
- any special constraints such as airflow, cable access, outdoor use, or weight

Use reasonable defaults when the user does not care:
- 0.4 mm nozzle
- PLA
- 0.2 mm layer height
- 0.3 mm fit clearance for typical FDM parts unless tighter or looser fit is needed

## Model rules

- Use millimeters only.
- Put editable dimensions at the top under a `PARAMETERS` section.
- Keep the build script readable and grouped by feature.
- Prefer bottom-on-bed geometry with `Z=0` at the print surface.
- Add clearances deliberately. Do not model nominal press fits with zero tolerance.
- For enclosures, shell inward when possible so outside dimensions stay stable.
- Apply large fillets and chamfers last.
- For parts with cavities, prefer direct 3MF export from CadQuery instead of STL-to-3MF conversion.

## Dimension research

When the part interfaces with a real product, search for exact dimensions first. Cross-check at least two sources when precision matters. Put sourced dimensions in comments near the parameters.

Examples:
- PCB size and hole spacing
- USB-C opening size
- charger puck diameter and thickness
- screw sizes and hole patterns
- cable bend clearance

## Preview and validation loop

Use the bundled scripts when present:

- `scripts/run_cadquery_model.py model.py --preview --strict`
- `scripts/preview.py model.stl preview.png --views multi`
- `scripts/stl_to_3mf.py model.stl`

Read `references/design-review.md` before final delivery or when a preview looks suspicious.

Always check:
- overall proportions
- flat printable base
- overhang risk
- thin walls or fragile features
- whether holes, cutouts, and bosses are where you expect
- watertight mesh status for exported STL files

## Suggested script shape

```python
import cadquery as cq

# PARAMETERS
width = 80.0
height = 30.0
depth = 20.0
wall = 2.0
clearance = 0.3

# MODEL
result = (
    cq.Workplane("XY")
    .box(width, depth, height, centered=(True, True, False))
)

# EXPORT
cq.exporters.export(result, "part.stl", tolerance=0.01, angularTolerance=0.1)
```

If the part has enclosed cavities and the environment supports it, also export `part.3mf` directly from CadQuery.

## Delivery format

Return:
- the main model file path
- preview image path if generated
- key dimensions
- one short print recipe
- any fit or support warnings

Keep print advice short. Example:

`Print settings: PLA, 0.2 mm layer, 3 walls, 20% gyroid, no supports. Orientation: flat back on the bed. Why: strongest layer direction for the bracket arms and no severe overhangs.`
