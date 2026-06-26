---
name: onshape-featurescript
description">Generate Onshape FeatureScript code for custom CAD features and parametric parts. Specializes in dust collection fittings library (wyes, elbows, adapters, crosses). Use when user asks to: (1) create FS features (gears, fittings, brushes), (2) modify existing FS, (3) debug FS errors, (4) build libraries with consistent patterns (enums, shells, labels). Patterns for Z-axis fittings, wrapped labels, safe unions/shells. Triggers: 'Onshape FS for X', 'FeatureScript wye/elbow', 'dust fitting'.</description>
---

# Onshape FeatureScript Generator

## Quick Start

Analyze request → Match pattern → Gen FS code → Validate logic.

**Core Workflow**:
1. **Precondition**: Enums/lengths/reals w/ bounds.
2. **Body**: Sketches → Extrudes → Booleans → Shell → Wrap/Thicken labels.
3. **Pitfalls**: qOwnedByBody(finalBody), if/else (no ternary lengths), cylinder(coordSystem).

## Key Patterns (Memorize)
- **Enum + Cond Param**:
  ```
  export enum AlignmentStyle { Centered, Tangent, Offset };
  if (definition.alignment == AlignmentStyle.Offset) { isLength(def.offsetDistance...); }
  ```
- **Safe Shell Caps**:
  ```
  var capFaces = qFacesParallelToDirection(qOwnedByBody(finalBody, EntityType.FACE), vector(0,1,0));
  ```
- **Union Primary First**:
  ```
  qUnion([qCreatedBy(id+"inlet", EntityType.BODY), ...]);
  ```
- **Wrapped Label**: skText → opWrap → opThicken.

## Dust Fittings Lib
Z-axis: Inlet Z=0 (-Z), Outlet Z=trans (+Z), Branch +X.
See [FITTINGS.md](references/fittings.md) for full spec/pitfalls.

## Resources
- **API Patterns**: [PATTERNS.md](references/patterns.md)
- **Fonts**: AllertaStencil-Regular.ttf for labels.
- **Validate**: Test mentally; no runtime here.

Gen code → User pastes to Onshape FS editor.
