---
name: openscad-automation
description: "Direct OpenSCAD scripting and rendering automation for OpenClaw - create, render, and export 3D models via CLI"
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["openscad"] },
        "notes": "OpenSCAD must be installed separately - download from https://openscad.org (Windows/macOS/Linux)"
      }
  }
---

# OpenSCAD Automation Skill

**Version:** 1.1.0  
**Author:** Klepeto 🦞  
**Description:** Direct OpenSCAD scripting, rendering automation, and library integration

---

## What is OpenSCAD?

**OpenSCAD** is a free, open-source "Programmer's Solid 3D CAD Modeller". Instead of interactive modeling like Fusion 360 or Tinkercad, you write code that describes objects. The script is compiled into a 3D model.

### Why OpenSCAD?

- 📐 **Parametric designs** - Change one variable, entire model updates
- 🔧 **Precise dimensions** - Perfect for mechanical parts, enclosures, adapters
- 📦 **Version control friendly** - `.scad` files are plain text, diffable in Git
- ⚙️ **Mathematical shapes** - Gears, threads, spirals, organic forms via code
- 🎨 **Generative art** - Algorithms creating complex patterns
- 🔄 **Reusable libraries** - Import community libraries for common parts

### When to Use OpenSCAD vs Other CAD

| Use OpenSCAD | Use Fusion 360 / Tinkercad |
|--------------|---------------------------|
| Parametric designs | Organic, freeform shapes |
| Precise mechanical parts | Quick prototyping |
| Mathematical surfaces | Visual, interactive design |
| Batch generation | One-off models |
| Version-controlled designs | Visual iteration |

**Get OpenSCAD:** https://openscad.org (Windows, macOS, Linux)

---

## Installation

### Windows

1. **Install OpenSCAD:** Download from https://openscad.org
   - Default location: `????\OpenSCAD\openscad.exe`
2. **OpenClaw Workspace:** `????\.openclaw\workspace`

### macOS

```bash
brew install openscad
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install openscad

# Fedora
sudo dnf install openscad
```

**OpenClaw Path:** `~/.openclaw/workspace`

### Verify Installation

```bash
# Windows PowerShell
& "????\OpenSCAD\openscad.exe" --version

# macOS/Linux
openscad --version
```

**Expected output:** `OpenSCAD version 2021.01` (or newer)

---

## Capabilities

- ✅ Write `.scad` files directly to workspace
- ✅ Render to STL (3D printing)
- ✅ Render to PNG (previews)
- ✅ Render to SVG (2D projections)
- ✅ Execute OpenSCAD CLI with proper PowerShell syntax
- ✅ Provide parametric templates
- ✅ Batch render multiple variants
- ✅ Use community libraries (BOSL, NopSCADlib, etc.)
- ✅ Generate customizers with `//` comments

---

## Language Reference

### Basic Syntax

```openscad
// Variables
width = 50;
height = 30;
depth = 20;

// Primitive solids
cube([width, height, depth], center = true);
sphere(r = 10);
cylinder(h = 30, r = 5);

// Transformations
translate([x, y, z]) { ... }
rotate([x, y, z]) { ... }  // degrees
scale([x, y, z]) { ... }

// Boolean operations
union() { ... }      // combine
difference() { ... } // subtract
intersection() { ... } // keep overlap
```

### Special Variables (Resolution)

```openscad
$fn = 100;    // Number of fragments (circles)
$fa = 5;      // Minimum angle
$fs = 0.5;    // Minimum size
```

**Tip:** Higher `$fn` = smoother curves, slower render. Default is 12.

### Control Flow

```openscad
// Conditionals
if (width > 50) {
    cube(20);
} else {
    sphere(10);
}

// Loops
for (i = [0:5]) {
    translate([i * 10, 0, 0])
        cube(5);
}

// List comprehensions
sizes = [for (i = [1:10]) i * 2];
```

### Modules and Functions

```openscad
// Module (creates geometry)
module box(w, h, d) {
    cube([w, h, d], center = true);
}

box(50, 30, 20);

// Function (returns value)
function diameter(pitch, teeth) = pitch * teeth / PI;

gear_d = diameter(2, 20);
```

### Import/Export

```openscad
// Import STL, OFF, AMF, 3MF
import("part.stl");

// Import DXF, SVG (2D)
import("profile.dxf");

// Export via CLI (not in script)
// & openscad.exe -o output.stl input.scad
```

### Modifier Characters

```openscad
* cube(10);    // Disable (comment out)
! sphere(10);  // Show only (root)
# cylinder(10); // Highlight (debug, red)
% cube(10);    // Background (transparent)
```

---

## Cheat Sheet (Quick Reference)

### 2D Primitives
```openscad
circle(r = 10 | d = 20);
square(size = 10, center = true);
square([w, h], center = true);
polygon([[x1,y1], [x2,y2], ...]);
text("Hello", size = 10, font = "Arial");
```

### 3D Primitives
```openscad
sphere(r = 10 | d = 20);
cube(size = 10, center = true);
cube([w, d, h], center = true);
cylinder(h = 30, r = 5 | d = 10, center = true);
cylinder(h = 30, r1 = 5, r2 = 3, center = true); // cone
polyhedron(points = [...], faces = [...]);
```

### Extrusions
```openscad
linear_extrude(height = 10, twist = 45, slices = 20) {
    circle(10);
}

rotate_extrude(angle = 360) {
    translate([10, 0]) circle(2);
}
```

### Transformations
```openscad
translate([x, y, z]) { ... }
rotate([x, y, z]) { ... }  // degrees around each axis
rotate(a, [x, y, z]) { ... }  // rotate a degrees around vector
scale([x, y, z]) { ... }
resize([x, y, z], auto = true) { ... }
mirror([x, y, z]) { ... }
color("red") { ... }
color("#FF0000") { ... }
color([1, 0, 0, 1]) { ... }  // RGBA 0-1
```

### Boolean Operations
```openscad
union() {
    cube(10);
    sphere(10);
}

difference() {
    cube(20);
    sphere(10);  // subtracted from cube
}

intersection() {
    cube(20);
    sphere(10);  // only overlapping volume
}
```

### Mathematical Functions
```openscad
abs(x)      // absolute value
sin(x)      // sine (degrees)
cos(x)      // cosine
tan(x)      // tangent
acos(x)     // arccosine
asin(x)     // arcsine
atan2(y, x) // arctangent
floor(x)    // round down
ceil(x)     // round up
round(x)    // round nearest
sqrt(x)     // square root
pow(x, y)   // x^y
ln(x)       // natural log
log(x)      // base-10 log
min(a, b)   // minimum
max(a, b)   // maximum
norm(v)     // vector norm
cross(a, b) // cross product
```

### String Functions
```openscad
str("Value: ", 42)      // concatenate
chr(65)                  // character from code (A)
ord("A")                 // code from character (65)
len("hello")             // length (5)
```

### Type Tests
```openscad
is_undef(x)    // is undefined
is_bool(x)     // is boolean
is_num(x)      // is number
is_string(x)   // is string
is_list(x)     // is list/vector
is_function(x) // is function
```

---

## Command-Line Usage

### Render to STL (3D Printing)
```powershell
& "????\OpenSCAD\openscad.exe" -o "output.stl" "model.scad"
```

### Render to PNG (Preview)
```powershell
& "????\OpenSCAD\openscad.exe" -o "preview.png" --imgsize 1024,1024 "model.scad"
```

### Render to SVG (2D Projection)
```powershell
& "????\OpenSCAD\openscad.exe" -o "output.svg" --projection both "model.scad"
```

### With Parameters
```powershell
& "????\OpenSCAD\openscad.exe" -o "out.stl" -D "width=50" -D "height=30" "parametric.scad"
```

### Open in GUI
```powershell
& "????\OpenSCAD\openscad.exe" "model.scad"
```

### Common CLI Options

| Option | Description |
|--------|-------------|
| `-o <file>` | Output file (STL, PNG, SVG, etc.) |
| `-D <var name="val">` | Set variable before rendering |
| `--imgsize W,H` | PNG image size |
| `--projection [both]` | SVG projection type |
| `--render` | Force full CGAL render |
| `--enable <feature>` | Enable experimental features |
| `--viewall` | Fit model in view (PNG) |
| `--colorscheme <name>` | Color theme (starnight, beforedawn, etc.) |

---

## Community Libraries

OpenSCAD has a rich ecosystem of community libraries. Import them with `use <library.scad>` or `include <library.scad>`.

### General Purpose Libraries

#### BOSL2 (Belfry OpenSCAD Library v2)
**Best for:** Everyday modeling helpers, shapes, masks

```openscad
use <BOSL2/std.scad>
use <BOSL2/rounding.scad>

rounded_cube([50,30,20], r=5);
```

- **GitHub:** https://github.com/BelfrySCAD/BOSL2
- **Wiki:** https://github.com/BelfrySCAD/BOSL2/wiki
- **License:** BSD-2-Clause

#### NopSCADlib
**Best for:** 3D printer parts, electronics enclosures, hardware

```openscad
use <NopSCADlib/screws.scad>
use <NopSCADlib/enclosures.scad>

screw_hole(3);  // M3 screw hole
```

- **GitHub:** https://github.com/nophead/NopSCADlib
- **License:** GPL-3.0-or-later

#### UB.scad
**Best for:** 3D printing workflow, mechanical parts, view helpers

```openscad
use <UB.scad/UB.scad>

view_rotate();  // Animation helpers
```

- **GitHub:** https://github.com/UBaer21/UB.scad
- **License:** CC0-1.0

#### dotSCAD
**Best for:** Mathematical modeling, reduced complexity

```openscad
use <dotSCAD/modeling.scad>
use <dotSCAD/math.scad>
```

- **GitHub:** https://github.com/JustinSDK/dotSCAD
- **Docs:** https://openhome.cc/eGossip/OpenSCAD/
- **License:** LGPL-3.0-only

### Specialized Libraries

#### threads.scad
**Best for:** Metric threads, bolts, nuts, augers

```openscad
use <threads.scad>

metric_bolt(d=10, pitch=1.5, length=50);
metric_nut(d=10);
```

- **GitHub:** https://github.com/rcolyer/threads-scad
- **License:** CC0-1.0

#### Round-Anything
**Best for:** Filleted/rounded parts, ergonomic design

```openscad
use <round-anything.scad>

round_anything(pts, radius);
```

- **GitHub:** https://github.com/Irev-Dev/Round-Anything
- **Docs:** https://learn.cadhub.xyz/docs/round-anything/overview/
- **License:** MIT

#### YAPP Box
**Best for:** Electronics project boxes with PCB mount

```openscad
use <YAPP_Box.scad>

// Define PCB dimensions, generate enclosure
```

- **GitHub:** https://github.com/mrWheel/YAPP_Box
- **License:** MIT

#### Board Game Toolkit
**Best for:** Board game organizers, boxes, inserts

```openscad
use <boardgame_toolkit.scad>

box_with_lid(w, h, d);
```

- **GitHub:** https://github.com/pinkfish/openscad_boardgame_toolkit
- **License:** Apache 2.0

#### STEMFIE
**Best for:** Educational construction sets, compatible parts

```openscad
use <stemfie.scad>

stemfie_beam(length);
stemfie_plate(width, height);
```

- **GitHub:** https://github.com/Cantareus/Stemfie_OpenSCAD
- **Project:** https://www.stemfie.org/
- **License:** GPL-3.0-or-later

### Installing Libraries

1. **Download** `.scad` files from GitHub
2. **Place** in your OpenSCAD libraries folder:
   - **Windows:** `????\Documents\OpenSCAD\libraries\`
   - **macOS:** `~/Documents/OpenSCAD/libraries/`
   - **Linux:** `~/.local/share/OpenSCAD/libraries/`
3. **Import** in your scripts:
   ```openscad
   use <BOSL2/std.scad>
   ```

---

## Templates

### Basic Cube
```openscad
// cube.scad
cube([20, 20, 20], center = true);
```

### Parametric Box with Lid
```openscad
// box_with_lid.scad
width = 80;
height = 60;
depth = 40;
wall = 2;
lip = 1;

// Box base
difference() {
    cube([width, height, depth], center = true);
    translate([0, 0, lip])
        cube([width - wall*2, height - wall*2, depth], center = true);
}

// Lid
translate([0, 0, depth/2 + lip])
    cube([width, height, 5], center = true);
```

### Gear (Simple)
```openscad
// gear.scad
$fn = 100;
teeth = 20;
module_gear = 2;  // module (tooth size)

pitch_diameter = teeth * module_gear;
outer_diameter = pitch_diameter + 2 * module_gear;

difference() {
    cylinder(h = 10, d = outer_diameter);
    cylinder(h = 12, d = pitch_diameter * 0.4);  // shaft hole
}
```

### Enclosure with Screw Bosses
```openscad
// enclosure.scad
use <NopSCADlib/screws.scad>

width = 100;
height = 80;
depth = 30;
wall = 2;

// Outer box
difference() {
    cube([width, height, depth], center = true);
    translate([0, 0, 1])
        cube([width - wall*2, height - wall*2, depth], center = true);
}

// Screw bosses (M3)
boss_positions = [[-40, -30], [40, -30], [-40, 30], [40, 30]];
for (pos = boss_positions) {
    translate([pos[0], pos[1], -depth/2])
        screw_hole(3, l = depth);
}
```

### Phone Stand
```openscad
// phone_stand.scad
$fn = 100;

// Base
cube([80, 60, 5], center = true);

// Back support (angled)
rotate([20, 0, 0])
    translate([0, -20, 30])
        cube([60, 10, 50], center = true);

// Front lip
translate([0, 25, 10])
    cube([60, 5, 15], center = true);
```

---

## Workflow

### 1. Design
Tell the agent what you want:
> "Create a parametric phone stand adjustable for 60-80mm phones"

Agent writes `.scad` file to workspace.

### 2. Preview
```powershell
& "????\OpenSCAD\openscad.exe" -o "preview.png" --imgsize 1024,1024 "design.scad"
```

### 3. Export for Printing
```powershell
& "????\OpenSCAD\openscad.exe" -o "design.stl" "design.scad"
```

### 4. Iterate
> "Make the angle 15° instead of 20°, add cable slot"

Agent modifies parameters, re-render.

---

## Tips & Best Practices

### Performance
- **Use `$fn` wisely:** 50-100 for visible curves, 12-24 for hidden features
- **Simplify early:** Remove unnecessary details before final render
- **Test small:** Preview with low resolution, render high-res only when ready

### Design
- **`center = true`:** Makes positioning easier
- **Use variables:** All dimensions as variables for easy tweaking
- **Comment parameters:** `// [10:100:10]` creates Customizer sliders
- **Modular design:** Break complex models into modules

### 3D Printing
- **Wall thickness:** Minimum 2-3x nozzle diameter (0.8-1.2mm for 0.4mm nozzle)
- **Tolerances:** Add 0.2-0.3mm clearance for moving parts
- **Orientation:** Design for optimal print orientation (minimize supports)
- **Export as STL:** Binary STL is smaller than ASCII

### Debugging
```openscad
// Highlight problematic part
# translate([0, 0, 10])
    cube(20);

// Disable temporarily
* sphere(10);

// Show only this part
! cylinder(20);

// Debug output
echo("Width =", width);
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Unexpected token` | PowerShell syntax | Use `&` before quoted path |
| `File not found` | Wrong path | Check relative path from workspace |
| `CGAL error` | Non-manifold geometry | Check for holes, intersections, inverted normals |
| `No top level object` | Empty script | Add at least one primitive |
| `Too many points` | Excessive `$fn` | Reduce resolution |
| `Import failed` | Missing file | Verify file exists and path is correct |
| `Circular dependency` | Modules calling each other | Restructure code |

---

## Learning Resources

### Official Documentation
- **Website:** https://openscad.org
- **User Manual:** https://en.wikibooks.org/wiki/OpenSCAD_User_Manual
- **Language Reference:** https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language_Reference
- **Cheat Sheet:** https://openscad.org/cheatsheet/index.html

### Tutorials
- **Wikibooks Tutorial:** https://en.wikibooks.org/wiki/OpenSCAD_Tutorial
  - Chapter 1: Getting started
  - Chapter 2: Scaling and parameterizing
  - Chapter 3: Combining objects
  - Chapter 4: Modules
  - Chapter 5: Libraries
  - Chapter 6: Control flow
  - Chapter 7: Loops and patterns
  - Chapter 8: Extrusion
  - Chapter 9: Math and geometry

### Community
- **Forum:** https://forum.openscad.org
- **GitHub:** https://github.com/openscad/openscad
- **Thingiverse:** Search "OpenSCAD" for examples
- **Printables:** Parametric models section

---

## Integration with Other Tools

### Fusion 360
- **OpenSCAD:** Parametric, mathematical, programmatic
- **Fusion 360:** Interactive, visual, assemblies
- **Workflow:** Export STL from OpenSCAD → Import to Fusion 360 for assembly

### Slicers (PrusaSlicer, Cura)
- **Direct STL import** from OpenSCAD output
- **Parametric workflow:** Adjust OpenSCAD variables → Re-slice → Print

### Git / Version Control
- `.scad` files are **plain text** - perfect for Git
- Track design iterations
- Branch for variants
- Diff to see what changed

---

*Created: 2026-05-24 | Updated: 2026-05-24 (v1.1.0 - Added full documentation, libraries, cheat sheet)*  
**Klepeto 🦞**
