---
name: grasshopper-generator
description:
  "Generate Rhino 7 Grasshopper (.ghx) XML files from natural language descriptions or images.
  Build parametric definitions with native GH components, GhPython scripts, and wiring.
  Supports concept design: twisted towers, curved facades, Voronoi patterns, diagrids,
  parametric surfaces, mesh operations, and custom Python geometry.
  Triggers: grasshopper, generate ghx, parametric definition, GH file,
  grasshopper definition, 参数化, 生成gh文件, when user wants a .ghx file."
---

# Grasshopper Generator

Generate Rhino 7 Grasshopper (.ghx) files programmatically.

## Workflow

### 1. Analyze Input

**Image** → Identify form (tower/dome/surface/facade), key features (twist/array/voronoi/diagrid), proportions.
**Text** → Parse the same from description.

### 2. Design the Graph

```
Sliders → Geometry → Transforms → Booleans → Output
```

Component priority:
1. Native GH components (see `references/component_guids.json` for 152 known GUIDs)
2. GhPython Script for complex custom logic
3. Third-party plugins only when explicitly requested

Common patterns:

| Form | Key Components |
|------|---------------|
| Twisted tower | Rectangle → Rotate → Extrude → Series |
| Curved facade | Curve → Divide → Orient → Surface |
| Voronoi | Populate 2D → Voronoi → Boundary Surfaces |
| Diagrid | Hexagonal → Scale → Loft |
| Dome | Circle → Rotate → Sweep1 |
| Custom logic | GhPython Script |

### 3. Generate .ghx

```python
import sys; sys.path.insert(0, 'SKILL_DIR/scripts')
from ghx_generator import GHXGenerator

gen = GHXGenerator("Definition Name", "Description")
r = gen.add_slider("Radius", 20, 1, 100, x=50, y=50)
c = gen.add_component("Circle", inputs=["Base Plane", "Radius"], outputs=["Circle"], x=300, y=50)
gen.connect(r, "output", c, "Radius")
gen.save("output.ghx")
```

### 4. GhPython Fallback

For complex geometry not achievable with native components:

```python
py = gen.add_python("Custom", code, inputs=["x", "y"], outputs=["a"], x=300, y=200)
```

GhPython has full `Rhino.Geometry` API. Input variables available by name. Assign `a = result` for output.

### 5. Deliver

Save .ghx and send to user. Note adjustable parameters (sliders), definition purpose, and any plugin dependencies.

## File Locations

- **Generator:** `scripts/ghx_generator.py` — full API with `add_slider`, `add_component`, `add_python`, `connect`, `save`
- **GUID database:** `references/component_guids.json` — 152 authentic component GUIDs extracted from real .gh files
- **Reference template:** `references/template_voronoi.ghx` — real Grasshopper file for structural reference

## Notes

- Output is .ghx (XML), fully compatible with Rhino 7
- All GUIDs extracted from real Grasshopper installations
- For components not in the database, GhPython Script handles everything
- Supports wiring via `connect(source_ref, source_param, target_ref, target_param)`
