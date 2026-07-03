from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def generate_function_graph(
    functions: Optional[null] = [],
    points: Optional[null] = None,
    showDerivative: Optional[bool] = False,
    showIntegral: Optional[bool] = False,
    integralBounds: Optional[null] = None,
    tangentAt: Optional[float] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Function Graph Tool — render single or multiple functions with JSXGraph.

Use when the problem asks to plot or sketch y = f(x), compare curves, or show calculus features such as tangents, derivatives, or integrals.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- points[].x, points[].y, domain[], integralBounds[]: MUST be NUMBERS (no quotes)
- expression: MUST be STRING (with quotes)

Capabilities:
- Plot one or many expressions with custom colors, labels, and domains.
- Include points, tangent lines, derivative traces, and shaded integral bands.
- Configure axes, bounding boxes, themes, zooming, and panning.

Examples:

1. Plot a single function:
{ "functions": [{ "expression": "x^2" }] }

2. Function with domain and open endpoints (for piecewise functions):
{ "functions": [
  { "expression": "x^2", "domain": [-3, 2], "leftOpen": true, "rightOpen": false }
] }
// leftOpen=true draws a hollow circle at x=-3, rightOpen=false draws a filled circle at x=2

3. Function with custom points (filled or open circles):
{ "functions": [{ "expression": "x^2" }],
  "points": [
    { "x": 0, "y": 0, "name": "Origin", "fillColor": "red" },
    { "x": 2, "y": 4, "fillColor": "white", "strokeColor": "blue" }  // open circle
  ] }

4. Multiple functions with custom colors:
{ "functions": [
  { "expression": "x^2", "color": "blue", "name": "f(x)" },
  { "expression": "x^3", "color": "red", "name": "g(x)" }
] }

Common mistakes to AVOID:
- ✗ { points: [{ x: "Math.PI", y: "0" }] } → ✓ { points: [{ x: 3.14159, y: 0 }] }
- ✗ { points: [{ x: 1, y: 2, name: 1 }] } → ✓ { points: [{ x: 1, y: 2, name: "Point 1" }] }
- ✗ { points: [{ name: 'A' }] } → ✓ Missing x and y coordinates
- ✗ { points: [{ x: 1 }] } → ✓ Missing y coordinate
- ✗ { points: [{ y: 2 }] } → ✓ Missing x coordinate
- ✗ { domain: ["0", "10"] } → ✓ { domain: [0, 10] }

Keywords: plot function, function graph, sketch curve, calculus visualization, compare functions
    
    Args:
        functions: Array of mathematical functions to plot. Each function has an expression and optional styling. Can be empty if only plotting points.
        points: Optional points to plot on the graph. Each point MUST have both x and y coordinates (numbers). Example: [{x: 0, y: 0, name: "Origin"}, {x: 1, y: 1}]
        showDerivative: Whether to show the derivative of the first function
        showIntegral: Whether to show the integral area of the first function
        integralBounds: Bounds for integral area [a, b], required if showIntegral is true
        tangentAt: X coordinate to show tangent line at
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "functions": functions,
        "points": points,
        "showDerivative": showDerivative,
        "showIntegral": showIntegral,
        "integralBounds": integralBounds,
        "tangentAt": tangentAt,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_function_graph", arguments)

def generate_parametric_curve(
    curves: Optional[null] = [{xExpression=Math.cos(t), yExpression=Math.sin(t), tMin=0.0, tMax=6.283185307179586, color=#0066cc, strokeWidth=2.0, dash=0.0}],
    showTrace: Optional[bool] = False,
    traceSpeed: Optional[float] = 1.0,
    points: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Parametric Curve Tool — plot curves defined by x(t) and y(t) with JSXGraph.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- tMin, tMax, points[].x, points[].y: MUST be NUMBERS (no quotes)
- xExpression, yExpression: MUST be STRINGS (with quotes)

Use when the prompt describes parameterized motion, circles, cycloids, Lissajous patterns, or any curve specified as functions of t.

Capabilities:
- Draw one or multiple parametric curves with custom domains and styling.
- Enable animated tracing to illustrate movement along the path.
- Overlay reference points and adjust axes, bounding boxes, and themes.

Examples:

1. Circle (unit circle):
{ "curves": [{ "xExpression": "Math.cos(t)", "yExpression": "Math.sin(t)", "tMin": 0, "tMax": 6.283185307179586 }] }

2. Parabola in parametric form:
{ "curves": [{ "xExpression": "t", "yExpression": "t^2", "tMin": -5, "tMax": 5 }] }

3. Curve with points (x = 5sin(t), 0 ≤ t ≤ π/6):
{ "curves": [{ "xExpression": "5 * Math.sin(t)", "yExpression": "t", "tMin": 0, "tMax": 0.5236 }],
  "points": [{ "x": 0, "y": 0 }, { "x": 2.5, "y": 0.5236 }] }

Common mistakes to AVOID:
- ✗ { tMax: "Math.PI/6" } → ✓ { tMax: 0.5236 }
- ✗ { tMax: "2*Math.PI" } → ✓ { tMax: 6.2832 }
- ✗ { tMin: "0" } → ✓ { tMin: 0 }
- ✗ { points: [{x: "2.5", y: "0.5236"}] } → ✓ { points: [{x: 2.5, y: 0.5236}] }

Keywords: parametric plot, x of t, y of t, motion path, curve animation
    
    Args:
        curves: Array of parametric curves to plot. Each curve is defined by x(t) and y(t) expressions. tMin and tMax MUST be numbers, not strings. Examples: [{xExpression: 'Math.cos(t)', yExpression: 'Math.sin(t)', tMin: 0, tMax: 6.283185307179586}] for circle, [{xExpression: 't', yExpression: 't^2', tMin: -5, tMax: 5}] for parabola.
        showTrace: Whether to show animated trace point moving along the curve
        traceSpeed: Speed of the trace animation (1 = normal speed)
        points: Optional points to plot on the graph
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "curves": curves,
        "showTrace": showTrace,
        "traceSpeed": traceSpeed,
        "points": points,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_parametric_curve", arguments)

def generate_geometry_diagram(
    points: Optional[null] = [],
    lines: Optional[null] = None,
    circles: Optional[null] = None,
    polygons: Optional[null] = None,
    angles: Optional[null] = None,
    showMeasurements: Optional[bool] = False,
    construction: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate interactive geometry diagrams using JSXGraph.
Create points, lines, circles, polygons, angles, vectors, and geometric constructions.
Perfect for visualizing geometric concepts, theorems, and constructions like triangles, perpendiculars, angle bisectors, vectors, etc.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- points[].x, points[].y: MUST be NUMBERS (no quotes)
- lines[].point1, lines[].point2: MUST be STRINGS (point names with quotes), NOT coordinate arrays
- lines[].type: 'line' | 'segment' | 'ray' | 'vector'
- polygons[].vertices: REQUIRED array of STRINGS (point names), minimum 3 elements
- angles[].point1, vertex, point2: MUST be STRINGS (point names with quotes)
- angles[].label: boolean (true/false) OR string (custom text like 'α', '∠ABC')

Examples:

1. Triangle with labeled vertices:
{ "points": [
    { "x": 0, "y": 0, "name": "A" },
    { "x": 3, "y": 0, "name": "B" },
    { "x": 1.5, "y": 2.6, "name": "C" }
  ],
  "lines": [
    { "point1": "A", "point2": "B" },
    { "point1": "B", "point2": "C" },
    { "point1": "C", "point2": "A" }
  ],
  "polygons": [{ "vertices": ["A", "B", "C"], "fillOpacity": 0.2 }]
}

2. Square with custom angle label:
{ "points": [
    { "x": 0, "y": 0, "name": "P1" },
    { "x": 2, "y": 0, "name": "P2" },
    { "x": 2, "y": 2, "name": "P3" },
    { "x": 0, "y": 2, "name": "P4" }
  ],
  "polygons": [{ "vertices": ["P1", "P2", "P3", "P4"] }],
  "angles": [{ "point1": "P1", "vertex": "P2", "point2": "P3", "label": "90°" }]
}

3. Vector diagram:
{ "points": [
    { "x": 0, "y": 0, "name": "O" },
    { "x": 3, "y": 2, "name": "A" },
    { "x": -1, "y": 3, "name": "B" }
  ],
  "lines": [
    { "point1": "O", "point2": "A", "type": "vector", "name": "v1", "color": "#ff0000" },
    { "point1": "O", "point2": "B", "type": "vector", "name": "v2", "color": "#0000ff" }
  ]
}

Common mistakes to AVOID:
- ✗ { lines: [{ point1: [0, 0], point2: [3, 0] }] } → ✓ Define points first, then reference by name
- ✗ { polygons: [{ fillColor: "blue" }] } → ✓ { polygons: [{ vertices: ["A", "B", "C"], fillColor: "blue" }] }
- ✗ { points: [{ x: "0", y: "0" }] } → ✓ { points: [{ x: 0, y: 0 }] }
- ✗ { lines: [{ point1: {x: 0, y: 0}, point2: "B" }] } → ✓ Use point names for both

REMEMBER: Always define points first, then reference them by name (string) in lines, polygons, angles!

Keywords: geometry, triangle, polygon, angle, vector, construction, geometric diagram
    
    Args:
        points: Array of points to create. Points can be referenced by name in other elements.
        lines: Array of lines, segments, or rays connecting points
        circles: Array of circles defined by center and radius or through-point
        polygons: Array of polygons defined by their vertices
        angles: Array of angles to display and measure
        showMeasurements: Whether to show measurements (distances, angles)
        construction: Geometric constructions like perpendiculars, parallels, midpoints, and angle bisectors
        style: Custom style configuration for the diagram.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "points": points,
        "lines": lines,
        "circles": circles,
        "polygons": polygons,
        "angles": angles,
        "showMeasurements": showMeasurements,
        "construction": construction,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_geometry_diagram", arguments)

def generate_vector_field(
    fieldFunction: null,
    density: Optional[float] = 10.0,
    scale: Optional[float] = 0.8,
    arrowStyle: Optional[null] = None,
    streamlines: Optional[null] = None,
    singularPoints: Optional[null] = None,
    colorByMagnitude: Optional[bool] = False,
    showMagnitudeLegend: Optional[bool] = False,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate vector field visualizations using JSXGraph.
Display 2D vector fields with arrows showing direction and magnitude at each point.
Supports streamlines, singular points, and color-coded magnitudes.
Ideal for visualizing gradient fields, flow fields, electromagnetic fields, etc.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- fieldFunction.dx, fieldFunction.dy: MUST be STRINGS (with quotes), even for constants like '1' or '0'
- startX, startY: MUST be NUMBERS (no quotes)

Examples:

1. Circular vector field F(x,y) = (-y, x):
{ "fieldFunction": { "dx": "-y", "dy": "x" } }

2. Direction field for y' = 9 + 9y:
{ "fieldFunction": { "dx": "1", "dy": "9 + 9*y" },
  "streamlines": [{ "startX": 0, "startY": -1 }, { "startX": 0, "startY": 0 }] }

3. Radial field F(x,y) = (x, y):
{ "fieldFunction": { "dx": "x", "dy": "y" } }

4. Gradient field ∇f where f(x,y) = x² + y²:
{ "fieldFunction": { "dx": "2*x", "dy": "2*y" } }

Common mistakes to AVOID:
- ✗ { fieldFunction: { dx: 1, dy: "9 + 9*y" } } → ✓ { fieldFunction: { "dx": "1", "dy": "9 + 9*y" } }
- ✗ { fieldFunction: { dx: 0, dy: 1 } } → ✓ { fieldFunction: { "dx": "0", "dy": "1" } }
- ✗ { fieldFunction: "x^2 + y^2" } → ✓ { fieldFunction: { "dx": "2*x", "dy": "2*y" } }
- ✗ { streamlines: true } → ✓ { streamlines: [{ startX: 0, startY: 0 }] } or omit
- ✗ Missing fieldFunction → ✓ Always include fieldFunction

REMEMBER: Even constant numbers like 0, 1, -1 MUST be strings: "0", "1", "-1"
    
    Args:
        fieldFunction: Vector field function F(x,y) = (dx, dy) - REQUIRED field. MUST be an object with 'dx' and 'dy' STRING expressions (both with quotes). Example: {"dx": "1", "dy": "9 + 9*y"} NOT {dx: 1, dy: ...}
        density: Number of vectors to show in each direction (density of the field)
        scale: Scale factor for vector lengths (0.1 to 2.0)
        arrowStyle: Styling options for the vector arrows
        streamlines: Optional streamlines (integral curves) to show the flow of the field. MUST be an array of objects, not a boolean. Example: [{startX: 0, startY: 0}, {startX: 1, startY: 1}] or omit entirely.
        singularPoints: Optional singular/critical points to highlight
        colorByMagnitude: Whether to color vectors based on their magnitude
        showMagnitudeLegend: Whether to show a legend for magnitude colors
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "fieldFunction": fieldFunction,
        "density": density,
        "scale": scale,
        "arrowStyle": arrowStyle,
        "streamlines": streamlines,
        "singularPoints": singularPoints,
        "colorByMagnitude": colorByMagnitude,
        "showMagnitudeLegend": showMagnitudeLegend,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_vector_field", arguments)

def generate_linear_system(
    equations: Optional[null] = [{a=1.0, b=1.0, c=5.0}, {a=1.0, b=-1.0, c=1.0}],
    inequalities: Optional[null] = [],
    showIntersections: Optional[bool] = True,
    showFeasibleRegion: Optional[bool] = True,
    objectives: Optional[null] = None,
    points: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Linear System Tool — graph linear equations and inequalities using JSXGraph.

Use when the prompt asks to solve or visualise systems of linear equations, highlight intersection points, or show feasible regions for inequalities/objectives.

Capabilities:
- Plot multiple lines defined in ax + by = c form with automatic intersection markers.
- Shade inequality regions, overlay objective functions, and mark optimal points.
- Add auxiliary points and configure axes, bounds, and styling.

Quick start example:
{ "equations": [{ "a": 1, "b": 1, "c": 5 }, { "a": 1, "b": -1, "c": 1 }] }

Keywords: linear system, intersection graph, inequality shading, objective line, simultaneous equations
    
    Args:
        equations: Array of linear equations to plot (ax + by = c form). Example: [{a: 1, b: 1, c: 5}, {a: 1, b: -1, c: 1}]
        inequalities: Array of linear inequalities to plot and shade. Example: [{a: 1, b: 1, c: 10, type: '<='}]
        showIntersections: Whether to highlight intersection points
        showFeasibleRegion: Whether to highlight the feasible region for inequalities
        objectives: Objective functions for linear programming
        points: Additional points to highlight
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "equations": equations,
        "inequalities": inequalities,
        "showIntersections": showIntersections,
        "showFeasibleRegion": showFeasibleRegion,
        "objectives": objectives,
        "points": points,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_linear_system", arguments)

def generate_function_transformation(
    baseFunction: Optional[null] = {expression=x^2, color=#0066cc, strokeWidth=2.0, name=f(x)},
    transformations: Optional[null] = [{type=translate, parameters={h=1.0, k=0.0}, strokeWidth=2.0, dash=0.0}],
    showSteps: Optional[bool] = False,
    showVectors: Optional[bool] = False,
    highlightPoints: Optional[null] = None,
    animateTransformation: Optional[bool] = False,
    compareMode: Optional[str] = "overlay",
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Function Transformation Tool — illustrate how a base function changes under common operations.

Use when the question mentions translations, stretches, reflections, absolute values, inverses, or composite functions based on an original curve.

Capabilities:
- Render a base function alongside any number of transformed variants.
- Support translation, scaling, reflection, absolute value, inverse, and composition scenarios.
- Highlight key points, vectors, animations, and comparison layouts.

IMPORTANT: transformation 'type' MUST be one of: 'translate', 'scale', 'reflect', 'absolute', 'inverse', 'composite'.

Examples:

1. Horizontal shift (translation):
{ "baseFunction": { "expression": "x^2" }, "transformations": [{ "type": "translate", "parameters": { "h": 2, "k": 1 } }] }

2. Vertical stretch (scaling):
{ "baseFunction": { "expression": "Math.sin(x)" }, "transformations": [{ "type": "scale", "parameters": { "a": 2 } }] }

3. Horizontal compression:
{ "baseFunction": { "expression": "x^2" }, "transformations": [{ "type": "scale", "parameters": { "b": 2 } }] }

4. Reflection across x-axis:
{ "baseFunction": { "expression": "x^2" }, "transformations": [{ "type": "reflect", "parameters": { "axis": "x" } }] }

5. Reflection across y=x (inverse function):
{ "baseFunction": { "expression": "x^3" }, "transformations": [{ "type": "reflect", "parameters": { "axis": "y=x" } }] }

6. Multiple transformations:
{ "baseFunction": { "expression": "x^2" }, "transformations": [
  { "type": "translate", "parameters": { "h": 1 } },
  { "type": "scale", "parameters": { "a": 2 } }
] }

Common mistakes:
- ✗ { type: 'stretch' } → ✓ { type: 'scale' }
- ✗ { type: 'verticalStretch' } → ✓ { type: 'scale', parameters: { a: 2 } }
- ✗ { type: 'horizontalStretch' } → ✓ { type: 'scale', parameters: { b: 0.5 } }
- ✗ { type: 'shift' } → ✓ { type: 'translate' }
- ✗ { type: 'move' } → ✓ { type: 'translate' }

Keywords: transform function, translate graph, stretch function, reflect curve, composition
    
    Args:
        baseFunction: The original function to transform
        transformations: Array of transformations to apply and visualize. Each transformation MUST have a valid 'type' field. For stretching/shrinking, use type: 'scale' (not 'stretch' or 'verticalStretch'). For shifting, use type: 'translate' (not 'shift' or 'move'). Examples: [{type: 'translate', parameters: {h: 2, k: 1}}] for horizontal shift right 2 and vertical shift up 1, [{type: 'scale', parameters: {a: 2}}] for vertical stretch by factor 2, [{type: 'reflect', parameters: {axis: 'x'}}] for reflection across x-axis.
        showSteps: Whether to show intermediate transformation steps
        showVectors: Whether to show transformation vectors for translations
        highlightPoints: Points to highlight on base and transformed functions
        animateTransformation: Whether to animate the transformation with a slider
        compareMode: How to display the functions
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "baseFunction": baseFunction,
        "transformations": transformations,
        "showSteps": showSteps,
        "showVectors": showVectors,
        "highlightPoints": highlightPoints,
        "animateTransformation": animateTransformation,
        "compareMode": compareMode,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_function_transformation", arguments)

def generate_quadratic_analysis(
    quadratics: Optional[null] = [{a=1.0, b=0.0, c=0.0}],
    showVertex: Optional[bool] = True,
    showAxisOfSymmetry: Optional[bool] = True,
    showRoots: Optional[bool] = True,
    showYIntercept: Optional[bool] = True,
    showFocusDirectrix: Optional[bool] = False,
    showDiscriminant: Optional[bool] = False,
    vertexForm: Optional[bool] = False,
    factorizedForm: Optional[bool] = False,
    tangentLines: Optional[null] = None,
    shadeRegion: Optional[null] = None,
    compareMode: Optional[str] = "overlay",
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Quadratic Analysis Tool — visualize parabolas and their key features using JSXGraph.

Use when the prompt asks to analyse or sketch quadratic functions, compare parabolas, or explain vertex, intercepts, symmetry, or discriminant behavior.

Capabilities:
- Plot one or more quadratic functions with optional styling.
- Highlight vertices, intercepts, axis of symmetry, focus/directrix, and discriminant notes.
- Display vertex or factorized forms, tangent lines, shaded regions, and comparison layouts.

Quick start example:
{ "quadratics": [{ "a": 1, "b": 0, "c": 0 }] }

Keywords: quadratic graph, parabola analysis, vertex form, factor form, compare parabolas
    
    Args:
        quadratics: Array of quadratic functions to analyze (ax^2 + bx + c form). Provide at least one or rely on the default parabola y = x^2.
        showVertex: Whether to show and label the vertex
        showAxisOfSymmetry: Whether to show the axis of symmetry
        showRoots: Whether to show and label the roots/x-intercepts
        showYIntercept: Whether to show the y-intercept
        showFocusDirectrix: Whether to show the focus and directrix
        showDiscriminant: Whether to display discriminant value and root nature
        vertexForm: Whether to display the vertex form: a(x-h)^2 + k
        factorizedForm: Whether to display the factorized form if applicable
        tangentLines: Points where to draw tangent lines
        shadeRegion: Region to shade relative to the parabola
        compareMode: How to display multiple quadratics
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "quadratics": quadratics,
        "showVertex": showVertex,
        "showAxisOfSymmetry": showAxisOfSymmetry,
        "showRoots": showRoots,
        "showYIntercept": showYIntercept,
        "showFocusDirectrix": showFocusDirectrix,
        "showDiscriminant": showDiscriminant,
        "vertexForm": vertexForm,
        "factorizedForm": factorizedForm,
        "tangentLines": tangentLines,
        "shadeRegion": shadeRegion,
        "compareMode": compareMode,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_quadratic_analysis", arguments)

def generate_exponential_logarithm(
    functions: Optional[null] = [{type=exponential, base=2.718281828459045, coefficient=1.0, hShift=0.0, vShift=0.0}],
    showAsymptotes: Optional[bool] = True,
    showIntercepts: Optional[bool] = True,
    showInverse: Optional[bool] = False,
    showReflectionLine: Optional[bool] = False,
    comparisonPoints: Optional[null] = None,
    growthDecayAnalysis: Optional[null] = None,
    logarithmicScale: Optional[null] = None,
    specialPoints: Optional[null] = None,
    tangentAt: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Exponential and Logarithmic Tool — plot growth, decay, and log curves with JSXGraph.

Use when the problem references exponential or logarithmic expressions, asymptotes, inverse relationships, or needs comparisons between bases.

Capabilities:
- Plot exponential or logarithmic functions, optionally mixing multiple curves.
- Display asymptotes, intercepts, inverse reflections, and logarithmic scales.
- Highlight comparison points, tangent lines, and growth or decay analysis blocks.

IMPORTANT:
- type: MUST be 'exponential' or 'logarithm' (NOT 'logarithmic', 'exp', 'log')
- base: MUST be a NUMBER like 2, 10, or 2.718281828459045 (NOT string 'e' or 'E')
- For natural log (ln), use type: 'logarithm' and omit base (defaults to e)
- For natural exponential (e^x), use type: 'exponential' and omit base

Examples:

1. Natural logarithm y = ln(x):
{ "functions": [{ "type": "logarithm" }] }

2. Common logarithm y = log₁₀(x):
{ "functions": [{ "type": "logarithm", "base": 10 }] }

3. Exponential growth y = 2^x:
{ "functions": [{ "type": "exponential", "base": 2 }] }

4. Natural exponential y = e^x:
{ "functions": [{ "type": "exponential" }] }

5. Exponential decay y = (0.5)^x:
{ "functions": [{ "type": "exponential", "base": 0.5 }] }

6. Compare ln(x) with log₂(x):
{ "functions": [
  { "type": "logarithm", "name": "ln(x)", "color": "blue" },
  { "type": "logarithm", "base": 2, "name": "log₂(x)", "color": "red" }
] }

7. Logarithm with special points and asymptote:
{ "functions": [{ "type": "logarithm", "base": 10 }],
  "showAsymptotes": true,
  "specialPoints": [{ "x": 1, "y": 0, "label": "(1, 0)" }, { "x": 10, "y": 1, "label": "(10, 1)" }] }

Common mistakes to avoid:
- ✗ { type: 'logarithmic' } → ✓ { type: 'logarithm' }
- ✗ { base: 'e' } → ✓ { base: 2.718281828459045 } or omit base
- ✗ { base: 'E' } → ✓ omit base (defaults to e)
- ✗ { expression: 'ln(x)' } → ✓ { type: 'logarithm' } (simpler)

Keywords: exponential graph, logarithmic curve, growth rate, decay model, inverse functions
    
    Args:
        functions: Array of exponential and logarithmic functions to plot. Each function MUST have 'type' field set to 'exponential' or 'logarithm' (not 'logarithmic'). The 'base' field MUST be a number (e.g., 2, 10, 2.718281828459045), not a string. Examples: [{type: 'exponential', base: 2}] for y=2^x, [{type: 'logarithm', base: 10}] for y=log₁₀(x), [{type: 'logarithm'}] for y=ln(x) (base defaults to e), [{type: 'exponential', base: 0.5}] for y=(0.5)^x (decay).
        showAsymptotes: Whether to show horizontal/vertical asymptotes
        showIntercepts: Whether to show and label x and y intercepts
        showInverse: Whether to show the inverse function
        showReflectionLine: Whether to show y=x line for inverse relationship
        comparisonPoints: Points to compare function values
        growthDecayAnalysis: Growth and decay analysis options
        logarithmicScale: Logarithmic scale options
        specialPoints: Special points to highlight (e.g., (0,1) for exponentials)
        tangentAt: X coordinates where to show tangent lines
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "functions": functions,
        "showAsymptotes": showAsymptotes,
        "showIntercepts": showIntercepts,
        "showInverse": showInverse,
        "showReflectionLine": showReflectionLine,
        "comparisonPoints": comparisonPoints,
        "growthDecayAnalysis": growthDecayAnalysis,
        "logarithmicScale": logarithmicScale,
        "specialPoints": specialPoints,
        "tangentAt": tangentAt,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_exponential_logarithm", arguments)

def generate_rational_function(
    rationalFunctions: Optional[null] = None,
    irrationalFunctions: Optional[null] = None,
    showVerticalAsymptotes: Optional[bool] = True,
    showHorizontalAsymptotes: Optional[bool] = True,
    showObliqueAsymptotes: Optional[bool] = True,
    showHoles: Optional[bool] = True,
    showIntercepts: Optional[bool] = True,
    showCriticalPoints: Optional[bool] = False,
    showDomainRestrictions: Optional[bool] = True,
    analyzeEndBehavior: Optional[bool] = False,
    factorization: Optional[null] = None,
    partialFractions: Optional[bool] = False,
    tangentLines: Optional[null] = None,
    shadeRegions: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate rational and irrational function visualizations using JSXGraph.
Plot rational functions with asymptotes (vertical, horizontal, oblique), holes, intercepts, and critical points.
Visualize irrational functions with domain restrictions.
Supports factorization, partial fractions, and end behavior analysis.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- numerator, denominator: MUST be STRINGS (with quotes), even for constants like '1' or '0'
- expression: MUST be STRING (with quotes)

Examples:

1. Simple rational function f(x) = 1/x:
{ "rationalFunctions": [{ "numerator": "1", "denominator": "x" }] }

2. Rational function f(x) = (x² - 1)/(x - 2):
{ "rationalFunctions": [{ "numerator": "x^2 - 1", "denominator": "x - 2" }] }

3. Multiple rational functions:
{ "rationalFunctions": [
  { "numerator": "x + 1", "denominator": "x^2 - 4", "color": "blue" },
  { "numerator": "x^2", "denominator": "x - 1", "color": "red" }
] }

4. Irrational function f(x) = √x:
{ "irrationalFunctions": [{ "expression": "Math.sqrt(x)", "domain": [0, 10] }] }

Common mistakes to AVOID:
- ✗ { "numerator": 1, "denominator": "x" } → ✓ { "numerator": "1", "denominator": "x" }
- ✗ { "numerator": 0 } → ✓ { "numerator": "0", "denominator": "1" }
- ✗ { "numerator": 2, "denominator": 3 } → ✓ { "numerator": "2", "denominator": "3" }
- ✗ { numerator: 2*x } → ✓ { "numerator": "2*x", "denominator": "1" }
- ✗ { numerator: x } → ✓ { "numerator": "x", "denominator": "1" }
- ✗ Missing denominator → ✓ Always include both numerator AND denominator

REMEMBER: ALL expressions MUST be strings with quotes, including simple numbers!
Examples: "1" not 1, "0" not 0, "x" not x, "2*x+1" not 2*x+1
    
    Args:
        rationalFunctions: Array of rational functions (P(x)/Q(x)) to plot. Both 'numerator' and 'denominator' MUST be STRING expressions, not numbers. Example: [{numerator: 'x^2 - 1', denominator: 'x - 2'}] for (x²-1)/(x-2). Even for constants, use strings: [{numerator: '1', denominator: 'x'}] for 1/x.
        irrationalFunctions: Array of irrational functions (involving roots) to plot
        showVerticalAsymptotes: Whether to show vertical asymptotes
        showHorizontalAsymptotes: Whether to show horizontal asymptotes
        showObliqueAsymptotes: Whether to show oblique/slant asymptotes
        showHoles: Whether to show removable discontinuities (holes)
        showIntercepts: Whether to show x and y intercepts
        showCriticalPoints: Whether to show local maxima and minima
        showDomainRestrictions: Whether to highlight domain restrictions for irrational functions
        analyzeEndBehavior: Whether to show end behavior analysis
        factorization: Factorization and simplification options
        partialFractions: Whether to show partial fraction decomposition
        tangentLines: X coordinates where to draw tangent lines
        shadeRegions: Regions to shade
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "rationalFunctions": rationalFunctions,
        "irrationalFunctions": irrationalFunctions,
        "showVerticalAsymptotes": showVerticalAsymptotes,
        "showHorizontalAsymptotes": showHorizontalAsymptotes,
        "showObliqueAsymptotes": showObliqueAsymptotes,
        "showHoles": showHoles,
        "showIntercepts": showIntercepts,
        "showCriticalPoints": showCriticalPoints,
        "showDomainRestrictions": showDomainRestrictions,
        "analyzeEndBehavior": analyzeEndBehavior,
        "factorization": factorization,
        "partialFractions": partialFractions,
        "tangentLines": tangentLines,
        "shadeRegions": shadeRegions,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_rational_function", arguments)

def generate_equation_system(
    systems: Optional[null] = None,
    individualEquations: Optional[null] = None,
    showIntersections: Optional[bool] = True,
    showSolutionSet: Optional[bool] = True,
    numericalSolutions: Optional[null] = None,
    parameterAnimation: Optional[null] = None,
    solutionRegions: Optional[null] = None,
    linearAlgebraView: Optional[null] = None,
    nonlinearAnalysis: Optional[null] = None,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate systems of equations visualization using JSXGraph. Solve and visualize linear and nonlinear equation systems, find intersection points, show solution sets, and analyze system properties. Supports implicit equations, parametric systems, numerical solutions, and advanced analysis including matrix representation and phase portraits.
    
    Args:
        systems: Array of equation systems to solve and visualize
        individualEquations: Individual equations to plot (not part of a system)
        showIntersections: Whether to highlight intersection points (solutions)
        showSolutionSet: Whether to display the solution set algebraically
        numericalSolutions: Numerical solution options
        parameterAnimation: Options for animating parametric equations
        solutionRegions: Regions defined by equation systems
        linearAlgebraView: Linear algebra analysis for linear systems
        nonlinearAnalysis: Nonlinear system analysis options
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "systems": systems,
        "individualEquations": individualEquations,
        "showIntersections": showIntersections,
        "showSolutionSet": showSolutionSet,
        "numericalSolutions": numericalSolutions,
        "parameterAnimation": parameterAnimation,
        "solutionRegions": solutionRegions,
        "linearAlgebraView": linearAlgebraView,
        "nonlinearAnalysis": nonlinearAnalysis,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_equation_system", arguments)

def generate_conic_section(
    conics: Optional[null] = None,
    generalConics: Optional[null] = None,
    polynomials: Optional[null] = None,
    points: Optional[null] = None,
    showFoci: Optional[bool] = True,
    showDirectrix: Optional[bool] = False,
    showAsymptotes: Optional[bool] = True,
    showCenter: Optional[bool] = True,
    showVertices: Optional[bool] = True,
    showEccentricity: Optional[bool] = False,
    showTangents: Optional[null] = None,
    showPolynomialRoots: Optional[bool] = True,
    showCriticalPoints: Optional[bool] = False,
    showInflectionPoints: Optional[bool] = False,
    degreeAnalysis: Optional[bool] = False,
    intersectionAnalysis: Optional[null] = None,
    polarForm: Optional[bool] = False,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate conic sections and high-degree polynomials using JSXGraph.
Visualize circles, ellipses, parabolas, hyperbolas with their foci, directrices, vertices, and asymptotes.
Plot polynomials with roots, critical points, and inflection points.
Supports general conic equations, rotated conics, and intersection analysis.

IMPORTANT: Each conic in the 'conics' array MUST have a 'type' field.

Examples:

1. Circle with radius 5:
{ "conics": [{ "type": "circle", "center": { "x": 0, "y": 0 }, "radius": 5 }] }

2. Parabola y² = 4px:
{ "conics": [{ "type": "parabola", "vertex": { "x": 0, "y": 0 }, "p": 1 }] }

3. Ellipse with semi-axes a=4, b=2:
{ "conics": [{ "type": "ellipse", "center": { "x": 0, "y": 0 }, "a": 4, "b": 2 }] }

4. Hyperbola:
{ "conics": [{ "type": "hyperbola", "center": { "x": 0, "y": 0 }, "a": 3, "b": 2 }] }

5. General conic Ax² + Bxy + Cy² + Dx + Ey + F = 0:
{ "generalConics": [{ "A": 1, "B": 0, "C": 1, "D": 0, "E": 0, "F": -25 }] }

Common mistakes:
- ✗ { conics: [{ radius: 5 }] } → ✓ Missing 'type' field
- ✗ { type: 'circular' } → ✓ Use 'circle'
- ✗ { type: 'para' } → ✓ Use 'parabola'
    
    Args:
        conics: Array of standard conic sections to plot. Each conic MUST have a 'type' field set to 'circle', 'ellipse', 'parabola', or 'hyperbola'. Examples: [{type: 'circle', center: {x: 0, y: 0}, radius: 5}], [{type: 'parabola', vertex: {x: 0, y: 0}, p: 1}], [{type: 'ellipse', center: {x: 0, y: 0}, a: 4, b: 2}].
        generalConics: Conic sections in general form: Ax² + Bxy + Cy² + Dx + Ey + F = 0
        polynomials: High-degree polynomial functions to plot
        points: Optional points to plot on the graph
        showFoci: Whether to show foci for conics
        showDirectrix: Whether to show directrix for parabolas and general conics
        showAsymptotes: Whether to show asymptotes for hyperbolas
        showCenter: Whether to mark the center of conics
        showVertices: Whether to mark vertices of conics
        showEccentricity: Whether to display eccentricity values
        showTangents: Tangent lines to draw
        showPolynomialRoots: Whether to mark roots of polynomials
        showCriticalPoints: Whether to show critical points of polynomials
        showInflectionPoints: Whether to show inflection points of polynomials
        degreeAnalysis: Whether to show polynomial degree and leading coefficient analysis
        intersectionAnalysis: Intersection analysis options
        polarForm: Whether to show polar form equations for conics
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        axisXTitle: Label for X axis
        axisYTitle: Label for Y axis
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "conics": conics,
        "generalConics": generalConics,
        "polynomials": polynomials,
        "points": points,
        "showFoci": showFoci,
        "showDirectrix": showDirectrix,
        "showAsymptotes": showAsymptotes,
        "showCenter": showCenter,
        "showVertices": showVertices,
        "showEccentricity": showEccentricity,
        "showTangents": showTangents,
        "showPolynomialRoots": showPolynomialRoots,
        "showCriticalPoints": showCriticalPoints,
        "showInflectionPoints": showInflectionPoints,
        "degreeAnalysis": degreeAnalysis,
        "intersectionAnalysis": intersectionAnalysis,
        "polarForm": polarForm,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_conic_section", arguments)

def generate_number_line_inequality(
    inequalities: Optional[null] = [{expression=x > 0, color=#0066cc, strokeWidth=3.0, showEndpoints=true, endpointRadius=0.15}],
    numberLinePosition: Optional[float] = 0.0,
    tickMarks: Optional[bool] = True,
    tickInterval: Optional[float] = 1.0,
    showNumbers: Optional[bool] = True,
    numberInterval: Optional[float] = 1.0,
    style: Optional[null] = None,
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    title: Optional[str] = "",
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Number Line Inequality Tool — illustrate solution sets on a one-dimensional axis with JSXGraph.

Use when the task asks to plot inequality solutions, show interval notation, or visualise unions/intersections on a number line.

Capabilities:
- Display one or many inequalities with open or closed endpoints and custom styling.
- Adjust tick spacing, numeric labels, and the vertical placement of the line.
- Combine multiple segments to showcase compound inequalities or piecewise regions.

IMPORTANT: Each inequality MUST have an 'expression' field (string). DO NOT use 'start/end' or 'includeStart/End' fields.

Examples:

1. Single inequality (x ≤ 3):
{ "inequalities": [{ "expression": "x <= 3" }] }

2. Union of intervals (x ≤ 3 or 4 ≤ x ≤ 5):
{ "inequalities": [
  { "expression": "x <= 3", "color": "blue" },
  { "expression": "4 <= x <= 5", "color": "blue" }
] }

3. Compound inequality with custom range:
{ "inequalities": [{ "expression": "-2 < x < 3" }], "boundingBox": [-5, 1, 5, -1] }

4. Multiple separate regions:
{ "inequalities": [
  { "expression": "x < -1", "color": "red" },
  { "expression": "2 <= x <= 4", "color": "green" },
  { "expression": "x > 6", "color": "blue" }
] }

Expression format guide:
- 'x > 2' → (2, ∞) open endpoint at 2
- 'x >= 2' → [2, ∞) closed endpoint at 2
- 'x <= 3' → (-∞, 3] closed endpoint at 3
- '2 < x < 5' → (2, 5) both open
- '2 <= x <= 5' → [2, 5] both closed
- '2 <= x < 5' → [2, 5) left closed, right open

Keywords: number line, inequality graph, interval notation, solution set, one dimensional plot
    
    Args:
        inequalities: Array of inequalities to plot on the number line. Each inequality MUST have an 'expression' field. Examples: [{expression: 'x > 2'}] for (2, ∞), [{expression: '0 <= x <= 5'}] for [0, 5], [{expression: 'x <= 3'}, {expression: '4 <= x <= 5'}] for union of (-∞, 3] ∪ [4, 5]. DO NOT use 'start', 'end', 'includeStart', or 'includeEnd' fields.
        numberLinePosition: Y coordinate position of the number line
        tickMarks: Whether to show tick marks on the number line
        tickInterval: Interval between tick marks
        showNumbers: Whether to show numbers on tick marks
        numberInterval: Interval between number labels
        style: Custom style configuration for the chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        title: Set the title of the math chart.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "inequalities": inequalities,
        "numberLinePosition": numberLinePosition,
        "tickMarks": tickMarks,
        "tickInterval": tickInterval,
        "showNumbers": showNumbers,
        "numberInterval": numberInterval,
        "style": style,
        "width": width,
        "height": height,
        "title": title,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_number_line_inequality", arguments)

def generate_economics_competition(
    curves: null,
    priceLine: float,
    quantityRange: null,
    labels: Optional[null] = None,
    showProfit: Optional[bool] = True,
    showEquilibrium: Optional[bool] = True,
    showShutdownPoint: Optional[bool] = False,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None,
    axisXTitle: Optional[str] = "Quantity (Q)",
    axisYTitle: Optional[str] = "Price/Cost ($)"
) -> Dict[str, Any]:
    """
    Generate economic competition market analysis charts including MC (Marginal Cost), AC (Average Cost), AVC (Average Variable Cost) curves, price line, and profit/loss areas. Ideal for perfect competition market analysis.
    
    Args:
        curves: Cost curves for the firm
        priceLine: Market price P (horizontal line)
        quantityRange: Quantity range [min, max] for the x-axis
        labels: Custom labels for curves and areas
        showProfit: Whether to shade the profit/loss area
        showEquilibrium: Whether to mark the equilibrium point(s)
        showShutdownPoint: Whether to mark the shutdown point (where P = min AVC)
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
        axisXTitle: null
        axisYTitle: null
    
    Returns:
        
    """
    arguments = {
        "curves": curves,
        "priceLine": priceLine,
        "quantityRange": quantityRange,
        "labels": labels,
        "showProfit": showProfit,
        "showEquilibrium": showEquilibrium,
        "showShutdownPoint": showShutdownPoint,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle
    }
    
    return call_api("1777316659751939", "generate_economics_competition", arguments)

def generate_structural_force(
    length: float,
    loads: null,
    reactions: null,
    shear: null,
    moment: null,
    deflection: Optional[null] = None,
    labels: Optional[null] = None,
    showValues: Optional[bool] = True,
    showDiagrams: Optional[null] = None,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate structural engineering shear force and bending moment diagrams. Displays beam with loads, support reactions, and resulting force diagrams. All calculations should be done externally - this tool only visualizes the results.
    
    Args:
        length: Beam length L in meters
        loads: Array of loads applied to the beam
        reactions: Support reactions (externally calculated, not solved by this tool)
        shear: Shear force curve as discrete points [x, V(x)]
        moment: Bending moment curve as discrete points [x, M(x)]
        deflection: Deflection curve as discrete points [x, y(x)] (optional)
        labels: Custom labels for diagrams
        showValues: Whether to show numerical values on diagrams
        showDiagrams: Which diagrams to display
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "length": length,
        "loads": loads,
        "reactions": reactions,
        "shear": shear,
        "moment": moment,
        "deflection": deflection,
        "labels": labels,
        "showValues": showValues,
        "showDiagrams": showDiagrams,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_structural_force", arguments)

def generate_economics_isoquant(
    isoquants: null,
    isocosts: Optional[null] = None,
    optimum: Optional[null] = None,
    labels: Optional[null] = None,
    showMarginalRate: Optional[bool] = False,
    showTangent: Optional[bool] = False,
    productionFunction: Optional[str] = None,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None,
    axisXTitle: Optional[str] = "Labor (L)",
    axisYTitle: Optional[str] = "Capital (K)"
) -> Dict[str, Any]:
    """
    Generate economics isoquant and isocost analysis charts.
Displays isoquant curves (equal output), isocost lines (equal cost), and optimal production points.
Ideal for production theory and cost minimization analysis.

IMPORTANT: 'isoquants' is a REQUIRED field. Each isoquant MUST have 'Q' and 'points' properties.

Examples:

1. Basic isoquant analysis:
{ "isoquants": [
  { "Q": 100, "points": [[1, 4], [2, 2], [4, 1]] }
] }

2. Multiple isoquants with isocost:
{ "isoquants": [
    { "Q": 100, "points": [[1, 4], [2, 2], [4, 1]] },
    { "Q": 200, "points": [[2, 8], [4, 4], [8, 2]] }
  ],
  "isocosts": [{ "C": 100, "slope": -1 }]
}

3. With optimal point:
{ "isoquants": [{ "Q": 100, "points": [[1, 4], [2, 2], [4, 1]] }],
  "optimum": { "K": 2, "L": 2 }
}

Common mistakes:
- ✗ { isoquants: [{ Q: 100 }] } → ✓ Missing 'points' array
- ✗ { isoquants: [{ points: [[1,2]] }] } → ✓ Missing 'Q' value
- ✗ { isoquants: [] } → ✓ Array cannot be empty, must have at least one isoquant
- ✓ { isoquants: [{ Q: 100, points: [[1,4], [2,2]] }] } → Correct
    
    Args:
        isoquants: Array of isoquant curves with their output levels and points - REQUIRED. Each isoquant MUST have 'Q' (output level) and 'points' (array of [L, K] coordinates). Example: [{Q: 100, points: [[1, 4], [2, 2], [4, 1]]}, {Q: 200, points: [[2, 8], [4, 4], [8, 2]]}]
        isocosts: Optional array of isocost lines
        optimum: Optimal point where isoquant is tangent to isocost
        labels: Custom labels for axes and curves
        showMarginalRate: Whether to show marginal rate of technical substitution (MRTS)
        showTangent: Whether to show tangent line at optimum point
        productionFunction: Production function expression for display, e.g., 'Q = AK^αL^β'
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
        axisXTitle: null
        axisYTitle: null
    
    Returns:
        
    """
    arguments = {
        "isoquants": isoquants,
        "isocosts": isocosts,
        "optimum": optimum,
        "labels": labels,
        "showMarginalRate": showMarginalRate,
        "showTangent": showTangent,
        "productionFunction": productionFunction,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle
    }
    
    return call_api("1777316659751939", "generate_economics_isoquant", arguments)

def generate_statistics_normal(
    mean: Optional[float] = 0.0,
    stddev: Optional[float] = 1.0,
    range: Optional[null] = [-4.0, 4.0],
    shade: Optional[null] = None,
    showStandardScale: Optional[bool] = False,
    showProbability: Optional[bool] = True,
    showCriticalValues: Optional[bool] = False,
    labels: Optional[null] = None,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None,
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "Probability Density"
) -> Dict[str, Any]:
    """
    Normal Distribution Tool — visualize probability density curves with JSXGraph.

Use when the prompt references a normal distribution, z-scores, shaded probability intervals, or hypothesis-testing thresholds.

⚠️⚠️⚠️ CRITICAL TYPE REQUIREMENTS ⚠️⚠️⚠️
- mean, stddev, range[], shade[]: MUST be NUMBERS (no quotes)
- labels properties (distribution, probability, mean, stddev): MUST be STRINGS (with quotes), NOT objects

Capabilities:
- Render the bell curve with configurable mean, standard deviation, and plotting range.
- Shade intervals, annotate standard scores, and display probability labels.
- Customize labels, styles, and auxiliary axes for teaching or analysis.

Examples:

1. Standard normal distribution N(0,1):
{ }  // produces N(0, 1) with default settings

2. Custom normal with shaded area:
{ "mean": 5, "stddev": 2, "shade": [3, 7] }

3. With custom labels:
{ "mean": 0, "stddev": 1,
  "labels": { "mean": "μ", "stddev": "σ", "probability": "P(a ≤ X ≤ b)" } }

Common mistakes to AVOID:
- ✗ { labels: { mean: {symbol: "μ"} } } → ✓ { labels: { mean: "μ" } }
- ✗ { labels: { distribution: {text: "f(x)"} } } → ✓ { labels: { distribution: "f(x) = ..." } }
- ✗ { mean: "5" } → ✓ { mean: 5 }
- ✗ { shade: ["1", "2"] } → ✓ { shade: [1, 2] }

REMEMBER: labels properties are STRINGS, not objects!

Keywords: normal curve, bell curve, z score, probability shading, statistics
    
    Args:
        mean: Mean (μ) of the normal distribution
        stddev: Standard deviation (σ) of the normal distribution
        range: Range [min, max] for plotting the distribution
        shade: Interval [a, b] to shade for probability calculation
        showStandardScale: Whether to show z-score scale on additional axis
        showProbability: Whether to display the shaded area probability
        showCriticalValues: Whether to mark critical values (±1σ, ±2σ, ±3σ)
        labels: ⚠️⚠️⚠️ CRITICAL: labels MUST be an object with STRING properties, NOT nested objects! ⚠️⚠️⚠️
Type: object with string values
Each property (distribution, probability, mean, stddev) MUST be a STRING.
❌ WRONG examples:
  - {distribution: {text: "formula"}} (nested object)
  - {mean: {symbol: "μ"}} (nested object)
✅ CORRECT examples:
  - {distribution: "$f(x) = ...$"} (string)
  - {mean: "μ", stddev: "σ"} (strings)
  - {probability: "P(X < a)"} (string)
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
        axisXTitle: null
        axisYTitle: null
    
    Returns:
        
    """
    arguments = {
        "mean": mean,
        "stddev": stddev,
        "range": range,
        "shade": shade,
        "showStandardScale": showStandardScale,
        "showProbability": showProbability,
        "showCriticalValues": showCriticalValues,
        "labels": labels,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle
    }
    
    return call_api("1777316659751939", "generate_statistics_normal", arguments)

def generate_transform_sequence(
    base: str,
    transforms: null,
    final: Optional[str] = None,
    showSteps: Optional[bool] = True,
    showAnimation: Optional[bool] = False,
    stepColors: Optional[null] = None,
    labels: Optional[null] = None,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None,
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y"
) -> Dict[str, Any]:
    """
    Generate function transformation sequence visualizations. Shows how a base function is transformed through a series of translations, scalings, and reflections. Ideal for teaching transformation concepts.
    
    Args:
        base: Base function expression, e.g., 'x^2', 'Math.sin(x)'
        transforms: Array of transformations to apply in sequence
        final: Final function expression for verification (optional)
        showSteps: Whether to show intermediate transformation steps
        showAnimation: Whether to animate the transformation sequence
        stepColors: Colors for each transformation step
        labels: Custom labels for base and final functions
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
        axisXTitle: null
        axisYTitle: null
    
    Returns:
        
    """
    arguments = {
        "base": base,
        "transforms": transforms,
        "final": final,
        "showSteps": showSteps,
        "showAnimation": showAnimation,
        "stepColors": stepColors,
        "labels": labels,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle
    }
    
    return call_api("1777316659751939", "generate_transform_sequence", arguments)

def generate_logo_design(
    paths: null,
    style: Optional[null] = None,
    pathStyles: Optional[null] = None,
    showGrid: Optional[bool] = False,
    showAxis: Optional[bool] = False,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = True,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None
) -> Dict[str, Any]:
    """
    Generate geometric logo designs using conic sections, polygons, and curves. Combines multiple geometric shapes with customizable styles to create logos and emblems.
    
    Args:
        paths: Array of geometric shapes that compose the logo
        style: Style configuration including default path styles
        pathStyles: Individual styles for each path (overrides defaults)
        showGrid: Whether to show grid (usually off for logos)
        showAxis: Whether to show axes (usually off for logos)
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
    
    Returns:
        
    """
    arguments = {
        "paths": paths,
        "style": style,
        "pathStyles": pathStyles,
        "showGrid": showGrid,
        "showAxis": showAxis,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan
    }
    
    return call_api("1777316659751939", "generate_logo_design", arguments)

def generate_linear_feasible(
    constraints: Optional[null] = [{a=1.0, b=1.0, c=10.0, type=<=}, {a=1.0, b=0.0, c=0.0, type=>=}, {a=0.0, b=1.0, c=0.0, type=>=}],
    domain: Optional[null] = [0.0, 20.0, 20.0, 0.0],
    objectiveFunction: Optional[null] = None,
    showVertices: Optional[bool] = True,
    showOptimalPoint: Optional[bool] = True,
    interactive: Optional[bool] = False,
    feasibleRegionStyle: Optional[null] = None,
    labels: Optional[null] = None,
    style: Optional[null] = None,
    title: Optional[str] = "",
    width: Optional[float] = 800.0,
    height: Optional[float] = 600.0,
    boundingBox: Optional[null] = None,
    keepAspectRatio: Optional[bool] = False,
    showCopyright: Optional[bool] = False,
    showNavigation: Optional[bool] = True,
    zoom: Optional[null] = None,
    pan: Optional[null] = None,
    axisXTitle: Optional[str] = "x",
    axisYTitle: Optional[str] = "y"
) -> Dict[str, Any]:
    """
    Linear Feasible Region Tool — visualise constraint systems and objectives with JSXGraph.

Use when the prompt involves linear programming, feasible regions, constraint sets, or identifying optimal points for an objective.

Capabilities:
- Plot constraint lines and shade the feasible polygon.
- Highlight vertices, objective direction, and best point when an objective is supplied.
- Configure domain bounds, labels, and styling for instructional diagrams.

Quick start example:
{ "constraints": [{ "a": 1, "b": 1, "c": 10 }, { "a": 1, "b": 0, "c": 0, "type": ">=" }] }

Keywords: feasible region, linear programming, constraint graph, objective optimization, LP diagram
    
    Args:
        constraints: Array of linear inequality constraints. Example: [{a: 1, b: 1, c: 10}, {a: 1, b: 0, c: 0, type: '>='}]
        domain: Clipping domain [xmin, xmax, ymin, ymax] for the feasible region
        objectiveFunction: Optional objective function for linear programming
        showVertices: Whether to mark vertices of the feasible region
        showOptimalPoint: Whether to mark the optimal point (if objective function provided)
        interactive: ⚠️ Rendering mode selection:

false (default) - STATIC mode:
  • Vertices pre-calculated on server
  • Generated code is simple and fast
  • Recommended for most use cases (diagrams, homework)
  • ~30 lines of generated code

true - INTERACTIVE mode:
  • Vertices calculated dynamically in browser
  • Supports draggable constraint lines (future)
  • More code, slightly slower initial render
  • ~120 lines of generated code

Use static mode unless you need dynamic updates.
        feasibleRegionStyle: Style for the feasible region
        labels: Custom labels
        style: Custom style configuration for the chart.
        title: Set the title of the math chart.
        width: Set the width of the math chart, default is 800.
        height: Set the height of the math chart, default is 600.
        boundingBox: The bounding box for the chart. Default is [-10, 10, 10, -10].
        keepAspectRatio: Whether to keep aspect ratio.
        showCopyright: Whether to show JSXGraph copyright.
        showNavigation: Whether to show navigation controls.
        zoom: Zoom configuration for the chart.
        pan: Pan configuration for the chart.
        axisXTitle: null
        axisYTitle: null
    
    Returns:
        
    """
    arguments = {
        "constraints": constraints,
        "domain": domain,
        "objectiveFunction": objectiveFunction,
        "showVertices": showVertices,
        "showOptimalPoint": showOptimalPoint,
        "interactive": interactive,
        "feasibleRegionStyle": feasibleRegionStyle,
        "labels": labels,
        "style": style,
        "title": title,
        "width": width,
        "height": height,
        "boundingBox": boundingBox,
        "keepAspectRatio": keepAspectRatio,
        "showCopyright": showCopyright,
        "showNavigation": showNavigation,
        "zoom": zoom,
        "pan": pan,
        "axisXTitle": axisXTitle,
        "axisYTitle": axisYTitle
    }
    
    return call_api("1777316659751939", "generate_linear_feasible", arguments)

