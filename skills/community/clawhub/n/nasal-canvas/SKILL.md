---
name: nasal-canvas
description: Provides practical guidance for creating, populating, styling, transforming, updating, and troubleshooting FlightGear Canvas interfaces with Nasal, including native Canvas elements, canvas.draw helpers, maps, raster images, and SVG parsing.
---

# Nasal Canvas

FlightGear Canvas is a 2D, OpenGL-backed rendering system exposed to Nasal. A Canvas is an off-screen texture/rendering context; a placement makes that texture visible in the FlightGear scene. Its scene graph is hierarchical:

- A Canvas owns a root group.
- Groups contain child elements and other groups.
- Common element types are `group`, `text`, `path`, `image`, and `map`.
- Element properties control rendering and behavior through the FlightGear property tree.
- Canvas uses Nasal, not JavaScript.
- The SVG parser translates a supported subset of SVG/XML into Canvas elements; it is not a browser-grade SVG renderer.

When a task involves placing a Canvas in an aircraft or scene, consult the relevant FlightGear Canvas placement/how-to documentation and the current source API. Scenery-object placement has special requirements and uses the scenery object's `_module_id` in its load handler; do not assume ordinary placement parameters are sufficient.

## Choosing how to populate a Canvas

There are two main approaches:

1. **Load SVG** when the artwork is primarily static, is easier to author in a vector editor such as Inkscape, or needs named elements that Nasal can later modify.
2. **Build elements in Nasal** when geometry is dynamic, generated from simulation data, or benefits from programmatic control.
3. **Use `canvas.draw`** for common higher-level shapes, scales, marks, and transforms instead of manually assembling every primitive.
4. **Use raster images** for artwork that does not need vector-level dynamic editing. For frequent pixel changes, use image pixel operations rather than creating a very large number of path elements.

Choose based on maintainability and update cost. A large collection of individual vector elements may be slower than rendering a single image because elements need geometry processing and rendering when the Canvas updates.

## Creating and managing a Canvas

The usual workflow is:

1. Create the Canvas using the relevant Canvas/window or aircraft-instrument setup API.
2. Configure its dimensions, view, rendering options, and background as needed.
3. Create a root or named group.
4. Add child elements or parse an SVG into a group.
5. Retain handles to elements that will be updated later.
6. Attach a placement so the Canvas is visible.
7. Update only the parts that need to change, and delete objects when their lifecycle ends.

Useful Canvas-level operations documented in the source include:

- `createGroup([name])`: create a group under the Canvas.
- `setColorBackground(r, g, b, a)`: set the Canvas background.
- `set(setting, value)`: configure settings such as `name`, `size`, `view`, `mipmapping`, `additive-blend`, `coverage-samples`, `color-samples`, `freeze`, `render-always`, and `update`.
- `get(name)`: retrieve a Canvas by name.
- `getPath()`: obtain its property path for use as an image source.
- `parsesvg(group, file[, font-mapper])`: parse SVG into a target group.
- `del()`: delete the Canvas.

The source documentation marks some methods/settings as uncertain or incompletely documented (for example `wrapCanvas`, `getPath` details, and whether every Canvas setting can be changed after initialization). Do not invent behavior for these; check the current implementation when they matter.

## Shared Element behavior

Most Canvas element types inherit common Element operations.

### Visibility and lifecycle

- `getVisible()` returns visibility state.
- `setVisible([visible])`, `show()`, `hide()`, and `toggleVisibility()` control visibility.
- `update()` requests an update in the current frame; ordinarily changes are reflected in the next frame. Visibility changes are documented as taking effect in the current frame.
- `del()` deletes the element.

### Geometry and transforms

The documented element transform model has two transformation matrices: the first is applied before the second.

- `createTransform([matrix])` adds a transform; the optional matrix is a six-value affine transform `[a, b, c, d, e, f]`.
- `setRotation(x, y)` rotates around the element's configured center and uses the first transform.
- `setTranslation(x, y)` translates using the second transform.
- `setScale(x, y)` scales using the second transform.
- `getScale()` returns `[x, y]`.
- `setCenter(x, y)`, `getCenter()`, and `updateCenter()` manage the rotation center.
- `getBoundingBox()` returns `[minX, minY, maxX, maxY]`.

Rotation is around the local origin unless a center is established. For rotation around an arbitrary point, account for the center explicitly. SVG rotation centers authored in Inkscape may be imported and used by `setRotation`. Keep transform order in mind: for example, a roll rotation and pitch translation often need to be applied in a deliberate order.

### Draw order

Canvas normally uses element creation/storage order: later elements are drawn on top. The `z-index` property can explicitly control ordering; higher values draw later and cover lower values. When sibling paths are nested in separate groups and must be ordered relative to one another, set ordering on the relevant groups. Historical implementation caveats exist around adding elements after setting `z-index`; verify behavior against the FlightGear version in use.

### Blending

Element properties `blend-source`, `blend-destination`, and their `-rgb` / `-alpha` variants configure OpenGL blending. These specify how the source being drawn combines with the destination already present. Common factors include `zero`, `one`, `src-alpha`, `one-minus-src-alpha`, `dst-alpha`, `dst-color`, and related OpenGL factors. Separate RGB and alpha factors are supported.

Do not assume blending works for every element: the source documentation explicitly notes that blending does not work for paths, while text and images are confirmed to support it. Consult OpenGL blend-function documentation for exact equations and factor semantics.

### Clipping

The `clip` property clips an element and its descendants. It accepts automatic clipping or a rectangle form such as `rect(top, right, bottom, left)`. `clip-frame` selects the coordinate frame (`GLOBAL`, `PARENT`, or `LOCAL`).

Clipping can be relatively expensive because it changes OpenGL clip planes for rendered objects. Prefer geometry changes, scaling, or changing point coordinates when those approaches are suitable. The documentation warns that clipping in `PARENT` or `LOCAL` coordinates may behave incorrectly under rotation (moving/scaling rather than rotating with the element).

## Groups

Groups inherit Element behavior and provide hierarchical organization.

- `createChild(type[, name])` creates one child of type `text`, `group`, `path`, `image`, or `map`.
- `createChildren(type, count)` creates multiple children.
- `getChildren()` returns child elements.
- `getElementById(name)` retrieves the first matching child element by name/ID.
- `removeAllChildren()` removes all children.

Group properties include:

- `clip`: clipping bounds for the group and descendants.
- `clip-frame`: coordinate frame for clipping.
- `font`: default font for text descendants.
- `stroke` and `fill`: documented as group properties, but the supplied reference does not fully describe their behavior.

`setDouble(key, value)` is documented for character-related settings such as `character-size` and `character-aspect-ration`, but the source leaves their details incomplete. Preserve the spelling used by the API when referring to the property, and verify current implementation before relying on undocumented behavior.

## Text elements

Text inherits Element behavior. Typical operations:

- `setText(text)`: set displayed text.
- `enableUpdate()` followed by `updateText(text)`: update efficiently in a frequently executed loop.
- `setAlignment(alignment)`: choose text anchoring.
- `setFontSize(size, aspectRatio)`: set font size and character height/width ratio (default ratio is 1).
- `setFont(fontName)`: select a font from FlightGear's font search locations.
- `setColor(r, g, b[, a])`: set text color.
- `setColorFill(r, g, b[, a])`: set text background color.
- `setDrawMode(mode)`: combine modes such as text, bounding box, filled bounding box, and alignment marker.
- `setPadding(...)` and `setMaxWidth(...)`: control text bounds/width; consult the implementation for details not specified in the reference.

For continuously updated instruments, prefer `updateText()` after calling `enableUpdate()` once. It remembers the last string and writes the property only when the value changes, reducing unnecessary property-tree I/O. Do not mix `setText()` and `updateText()` on the same element: `updateText()` does not track changes made to the property string by other means.

Supported alignment values include the nine top/center/bottom × left/center/right combinations, baseline variants (`left-baseline`, `center-baseline`, `right-baseline`), and bottom-baseline variants.

## Path elements

Paths inherit Element behavior and represent ordered drawing commands. `moveTo` / `move` reposition the pen; line and curve commands draw from the current point. Command order is significant.

### Editing path geometry

- `reset()` clears path data.
- `pop_front()` / `pop_back()` remove the first/last segment.
- `getNumSegments()` returns the segment count.
- Absolute and relative line operations: `moveTo`, `move`, `lineTo`, `line`, `horizTo`, `horiz`, `vertTo`, `vert`.
- Quadratic curves: `quadTo`, `quad`, `squadTo`, `squad`.
- Cubic curves: `cubicTo`, `cubic`, `scubicTo`, `scubic`.
- Shapes: `rect`, `square`, `ellipse`, `circle`, and `close`.
- Arc operations include small/large and clockwise/counter-clockwise variants, with `...To` and relative forms.

`rect(x, y, w, h, cfg)` supports optional corner-radius settings such as `border-radius`, `border-top-radius`, `border-bottom-radius`, `border-bottom-right-radius`, and `border-left-radius`. `square` is a square shorthand. `ellipse` uses radii and optional center coordinates; `circle` is the equal-radii shorthand. The source identifies `square`, `ellipse`, and `circle` as additions introduced in later FlightGear releases, but this skill intentionally does not impose a minimum API version: check the target runtime when using newer conveniences.

### Styling paths

Path styling can be set through methods and properties:

- `setColor(r, g, b[, a])` / `set("stroke", color)` for the outline.
- `setColorFill(r, g, b[, a])` / `set("fill", color)` for filling.
- `setStrokeLineWidth(width)`.
- `setStrokeLineJoin("miter" | "round" | "bevel")`.
- `setStrokeLineCap("butt" | "round" | "square")`.
- `setStrokeDashArray(pattern)` where the vector alternates dash and gap lengths.

The Path properties documented include `fill`, `fill-opacity`, `fill-rule`, `stroke`, `stroke-opacity`, `stroke-width`, `stroke-dasharray`, `stroke-linecap`, and `stroke-linejoin`. Fill and stroke default to none; opacity defaults to fully opaque; fill-rule supports `pseudo-nonzero` and `evenodd`.

### Bulk path data and geographic paths

- `setData(cmds, points)` replaces path data using command IDs and a flat coordinate vector.
- `addSegment(cmd, coords)` appends one command with its required coordinates.
- `setDataGeo(cmds, points)` and `addSegmentGeo(cmd, coords)` are geographic equivalents.

The documented command families cover close, move, line, horizontal/vertical line, quadratic/cubic curves, smooth curves, and small/large clockwise/counter-clockwise arcs. Coordinate counts vary by command: close uses zero; move/line and smooth quadratic use two; horizontal/vertical use one; quadratic and smooth cubic use four; cubic and arc commands use six and five respectively. Use the constants exposed by `canvas.Path` rather than unexplained numeric command IDs where possible.

Geographic path operations require the path's parent to be a `map`. Geographic coordinates can use hemisphere-prefixed strings; south/west directions invert the sign.

## Map elements

A Map inherits Element behavior and is a geographic group whose positions are projected according to its configured projection. It can contain multiple layers, each represented by Canvas groups.

Key operations:

- `setController(controller)`: assign a controller derived from `Map.Controller`.
- `addLayer(factory, type_arg=nil, priority=nil, style=nil, opts=nil, visible=1)`: add a data/rendering layer.
- `getLayer(type_arg)`: retrieve a layer.
- `setRange(range)` / `getRange()`: set/read display range in nautical miles.
- `setPos(lat, lon, hdg=nil, range=nil, alt=nil)`: set map center and orientation/range/altitude.
- `getPos()`: retrieve position, heading, range, and altitude.
- `getLat()`, `getLon()`, `getHdg()`, `getAlt()`, `getRange()`, `getLatLon()`, and `getPosCoord()`: retrieve individual or combined state.
- `update([predicate])`: update all layers or only layers accepted by a predicate.
- `del()`: delete the map.

The map heading determines the map's up direction and may represent north, track, or heading, with true/magnetic interpretation depending on the aircraft. Altitude is documented in feet. `getPosCoord()` returns a reused mutable `geo.Coord` object; refresh it with its `update()` method before relying on its values, and do not assume a previously returned object is an immutable snapshot. `Element.setGeoPosition(lat, lon)` is intended for map elements whose parent is a map.

## Image elements

Images inherit Element behavior and support image-specific properties:

- `src`: image source. The documented source forms include FlightGear search-path files, `canvas://` references (including a Canvas texture by index), HTTP URLs, and a Canvas object's `getPath()`.
- `x`, `y`, and `size`: position and dimensions.
- `fill`: modulation/background color; white leaves the source image unchanged. Color forms include hex, `rgb(...)`, and `rgba(...)`.
- `slice`: optional nine-slice scaling. This keeps corners undistorted while stretching the edge and center regions; a `fill` option can request center filling.
- `outset`: lets drawing extend beyond the nominal image size without enlarging the bounding box, useful for visual effects such as shadows that should not affect event/distance calculations.
- `file`: deprecated legacy source property; use `src`.

For image data manipulation, the documented methods include:

- `setPixel(x, y, color)`: set one pixel.
- `fillRect([x, y, width, height], color)`: fill a rectangle using absolute pixel coordinates.
- `dirtyPixels()`: call after completing pixel edits so the changes are committed.
- `imageSize()`: retrieve raw image dimensions.

Pixel colors may be RGB/RGBA vectors with channel values from 0 to 1 or hexadecimal strings. Use pixel operations when many pixels need changing; they can be more efficient than overlaying hundreds of path elements.

## `canvas.draw` helper library

The basic `canvas.draw` library is part of FGDATA in the documented project history. It provides higher-level drawing functions and reusable styles. Every draw method takes a Canvas group (`cgroup`) as its first argument.

### Shapes and grids

- `draw.colors`: standard named colors such as white, black, red, green, blue, cyan, magenta, yellow, and orange.
- `circle(cgroup, radius, center_x=nil, center_y=nil)`.
- `ellipse(cgroup, radius_x, radius_y, center_x=nil, center_y=nil)`.
- `arc(cgroup, radius, center, from_deg=nil, to_deg=nil)`: arc angles use compass-rose degrees (0 north, 90 east); defaults to a full circle.
- `rectangle(cgroup, width, height, x=0, y=0, rounded=nil)`.
- `square(cgroup, length, center_x=0, center_y=0, cfg=nil)`.
- `deltoid(cgroup, dx, dy1, dy2, x=0, y=0)`: kite/arrow-head style geometry; negative `dy2` creates an arrowhead.
- `rhombus(cgroup, dx, dy, center_x=0, center_y=0)` / `diamond`.
- `grid(cgroup, [sizeX, sizeY], dx, dy, border=1)` or `grid(cgroup, nx, ny, dx, dy, border=1)`.

### Scale marks

Use `marksLinear(cgroup, orientation, num_marks, interval, style)` for linear scales such as speed tapes. Orientation accepts up/down/vertical/left/right/horizontal forms; the first character is evaluated. Use `marksCircular(cgroup, radius, interval, phi_start=0, phi_stop=360, style=nil)` for circular scales, with degrees measured from north.

`canvas.draw.marksStyle.new()` creates a style object. Its documented configuration methods include:

- `setMarkLength(...)`: marker length as a fraction of interval or radius.
- `setMarkOffset(...)`: marker alignment/direction (left/up/center/right/down and inward/outward constants).
- `setMarkWidth(...)`: line width in pixels.
- `setSubdivisions(...)`: number of subdivisions.
- `setSubdivisionLength(...)`: subdivision length relative to the main marker.

### Transform helpers

The `canvas.draw.transform` module manipulates existing Canvas elements. Its documented functions include:

- `move(elem, dx, dy)`, `rotate(elem, deg, center)`.
- `flipX(elem, xaxis=0)`, `flipY(elem, yaxis=0)`.
- `alignX(elem, ref, alignment)` and `alignY(elem, ref, alignment)`.
- `rotate180(elem, center=nil)`.
- `scaleX(elem, factor, ref)`, `scaleY(elem, factor, ref)`, and `resize(elem, [xFactor, yFactor], ref)`.

Alignment references can be another element or a numeric coordinate. Horizontal and vertical alignment strings describe which edges/centers/baselines should coincide. Scaling helpers accept a reference point to keep fixed while resizing. The transform chapter in the source is explicitly a draft; check the implementation when exact edge behavior matters.

## SVG workflow

`canvas.parsesvg(group, file[, options])` parses an SVG file into a target group. The optional options hash can include a `font-mapper` callback.

A practical workflow:

1. Create a Canvas and a target group.
2. Parse the SVG into that group.
3. Give important SVG objects stable, unique IDs in the SVG authoring tool.
4. Retrieve elements with `getElementById()`.
5. Store handles and update text, colors, transforms, or visibility from Nasal.

Example pattern:

```nasal
var instrument = my_canvas.createGroup();
canvas.parsesvg(instrument, "Aircraft/MyAircraft/Instruments/Display.svg");

var warning = instrument.getElementById("warningText");
warning.setText("CHECK SYSTEM");
warning.setColor(1, 0, 0);
```

The parser supports a limited subset of SVG, not the complete SVG standard. The source describes support for paths (including dashed paths), text, groups, and cloning, and notes support for circle/ellipse in later development. Do not assume support for gradients, arbitrary SVG shapes, embedded raster images, nested SVG/image references, or every Inkscape feature. If an element fails to appear:

- Check the FlightGear console for parser errors.
- Inspect the SVG for unsupported primitives/features.
- In Inkscape, convert unsupported basic shapes to paths (for example, simplify/convert shape objects to path geometry).
- Consult the current `Nasal/canvas/svg.nas` implementation before extending the parser or depending on a feature.

The parser maps SVG/XML into Canvas/OpenVG primitives; FlightGear Canvas does not simply display an SVG file as a browser would. The parser is Nasal code and can be extended by mapping additional XML tags to supported Canvas/OpenVG primitives.

### Font mapping

SVG text defaults to a FlightGear font (the source identifies Liberation Mono Bold). Pass a `font-mapper` function to `canvas.parsesvg` to map SVG `font-family` and `font-weight` values to font files. The callback receives family and weight and should return a font filename; if it returns no mapping, the default font is used. Font files must be in FlightGear's global font directory or the aircraft's font directory.

## Designing reusable instruments

For complex displays (PFD, ND, EICAS, HUD, etc.):

- Encapsulate each instrument instance in a Nasal hash/class rather than using dozens of global variables.
- Keep the parsed root/group and element handles as instance members.
- Use stable SVG IDs and a lookup table/hash to store handles.
- Separate elements needing special initialization (for example, `updateCenter()`) from ordinary handles.
- Avoid ID collisions within the lookup namespace; rename IDs or use nested hashes when necessary.
- This pattern supports multiple independent instances of the same instrument and makes code easier to maintain.

Retain handles during initialization rather than repeatedly searching the scene graph in update loops. Use `updateText()` for frequently refreshed text and update only dynamic elements.

## Troubleshooting and implementation discipline

- **Nothing appears:** verify Canvas creation, target group, placement, visibility, source path, and console output.
- **SVG object missing:** check parser-supported features; convert unsupported shapes to paths and avoid assuming gradients or `<image>` support.
- **Unexpected layering:** inspect creation order and `z-index`, including the groups containing paths.
- **Wrong rotation:** inspect the local center, `updateCenter()`, and transform order.
- **Clipping moves or scales unexpectedly:** check `clip-frame`; clipping in rotated local/parent frames has documented limitations.
- **Slow update loop:** avoid rewriting unchanged text with `setText()`; use `enableUpdate()` + `updateText()`. Avoid excessive individual vector elements when a raster image or `canvas.draw` helper is more suitable.
- **Pixel edits do not show:** call `dirtyPixels()` after `setPixel()` operations.
- **Map coordinates appear stale:** refresh the reused `geo.Coord` object returned by `getPosCoord()`.

The source reference contains incomplete entries and historical caveats. Treat question marks, draft sections, and explicitly uncertain behavior as unknown until checked against the current FlightGear source (`Nasal/canvas/api.nas`, `Nasal/canvas/svg.nas`, `Nasal/canvas/draw/transform.nas`) and SimGear Canvas implementation. Prefer current implementation over assumptions based on old examples.
