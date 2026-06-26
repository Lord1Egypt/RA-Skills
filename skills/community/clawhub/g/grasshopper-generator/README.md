# Grasshopper Generator

An OpenClaw skill that generates Rhino 7 Grasshopper (.ghx) files from natural language descriptions or images.

## What It Does

- Generates valid `.ghx` (XML) files compatible with Rhino 7 Grasshopper
- Supports 152 authentic native Grasshopper components with real GUIDs
- GhPython Script components for custom geometry logic
- Automatic wiring between components
- Built-in validation to ensure generated files are structurally correct

## Quick Start

### As an OpenClaw Skill

Install the `.skill` file and use it via your agent:

```
> Generate a parametric twisted tower Grasshopper definition
```

### Standalone Python Library

```python
from ghx_generator import GHXGenerator

gen = GHXGenerator("My Definition", "Description")

# Add a slider
radius = gen.add_slider("Radius", 20, 1, 100, x=50, y=50)

# Add a native component
circle = gen.add_component("Circle", inputs=["Base Plane", "Radius"],
                           outputs=["Circle"], x=300, y=50)

# Wire them
gen.connect(radius, "output", circle, "Radius")

# Save
gen.save("output.ghx")
```

### CLI

```bash
# Generate demo file
python scripts/ghx_generator.py

# Custom output
python scripts/ghx_generator.py -o my_definition.ghx

# List all known components
python scripts/ghx_generator.py --list

# Validate a .ghx file
python scripts/ghx_generator.py --validate myfile.ghx
```

## Components Database

152 authentic component GUIDs extracted from real Grasshopper installations, organized by category:

| Category | Examples |
|----------|---------|
| Params | Number Slider, Panel, Point, Curve |
| Math | Addition, Multiplication, Division |
| Vector | Unit X/Y/Z, Construct Point, Planes |
| Curve | Line, Circle, Rectangle, Divide Curve, Voronoi |
| Surface | Loft, Extrude, Boundary Surfaces, Sweep1 |
| Transform | Move, Rotate, Scale, Mirror, Orient |
| Intersect | Solid Union, Solid Difference |
| Mesh | Mesh Brep, Mesh Join |
| Script | GhPython Script |

For components not in the database, use GhPython Script — it has full `Rhino.Geometry` API access.

## File Structure

```
grasshopper-generator/
├── SKILL.md                    # Skill definition and workflow
├── scripts/
│   └── ghx_generator.py        # Core generator with CLI
└── references/
    ├── component_guids.json    # 152 authentic component GUIDs
    └── template_voronoi.ghx    # Reference template from real GH file
```

## GhPython Example

```python
py = gen.add_python("Twisted Tower", """
import Rhino.Geometry as rg
import math

pts = []
for i in range(floors):
    t = i / max(floors - 1, 1)
    angle = math.radians(twist * t)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = height * t
    pts.append(rg.Point3d(x, y, z))

a = rg.NurbsCurve.CreateInterpolated(pts, 3)
""", inputs=["radius", "height", "twist", "floors"],
    outputs=["a"], x=300, y=200)
```

## License

MIT
