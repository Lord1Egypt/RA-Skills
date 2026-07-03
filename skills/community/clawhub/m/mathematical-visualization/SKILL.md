---
name: 数学可视化服务
description: 基于JSXGraph的MCP协议服务器，提供13种数学可视化工具，适用于教育数学、工程和科学应用。
version: 1.0.0
---

# 数学可视化服务

基于JSXGraph的MCP协议服务器，提供13种数学可视化工具，适用于教育数学、工程和科学应用。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Function Graph Tool — render single or multiple functions with JSXGraph.

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

Keywords: plot function, function graph, sketch curve, calculus visualization, compare functions | `scripts.tools.generate_function_graph` |
| Parametric Curve Tool — plot curves defined by x(t) and y(t) with JSXGraph.

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

Keywords: parametric plot, x of t, y of t, motion path, curve animation | `scripts.tools.generate_parametric_curve` |
| Generate interactive geometry diagrams using JSXGraph.
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

Keywords: geometry, triangle, polygon, angle, vector, construction, geometric diagram | `scripts.tools.generate_geometry_diagram` |
| Generate vector field visualizations using JSXGraph.
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

REMEMBER: Even constant numbers like 0, 1, -1 MUST be strings: "0", "1", "-1" | `scripts.tools.generate_vector_field` |
| Linear System Tool — graph linear equations and inequalities using JSXGraph.

Use when the prompt asks to solve or visualise systems of linear equations, highlight intersection points, or show feasible regions for inequalities/objectives.

Capabilities:
- Plot multiple lines defined in ax + by = c form with automatic intersection markers.
- Shade inequality regions, overlay objective functions, and mark optimal points.
- Add auxiliary points and configure axes, bounds, and styling.

Quick start example:
{ "equations": [{ "a": 1, "b": 1, "c": 5 }, { "a": 1, "b": -1, "c": 1 }] }

Keywords: linear system, intersection graph, inequality shading, objective line, simultaneous equations | `scripts.tools.generate_linear_system` |
| Function Transformation Tool — illustrate how a base function changes under common operations.

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

Keywords: transform function, translate graph, stretch function, reflect curve, composition | `scripts.tools.generate_function_transformation` |
| Quadratic Analysis Tool — visualize parabolas and their key features using JSXGraph.

Use when the prompt asks to analyse or sketch quadratic functions, compare parabolas, or explain vertex, intercepts, symmetry, or discriminant behavior.

Capabilities:
- Plot one or more quadratic functions with optional styling.
- Highlight vertices, intercepts, axis of symmetry, focus/directrix, and discriminant notes.
- Display vertex or factorized forms, tangent lines, shaded regions, and comparison layouts.

Quick start example:
{ "quadratics": [{ "a": 1, "b": 0, "c": 0 }] }

Keywords: quadratic graph, parabola analysis, vertex form, factor form, compare parabolas | `scripts.tools.generate_quadratic_analysis` |
| Exponential and Logarithmic Tool — plot growth, decay, and log curves with JSXGraph.

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

Keywords: exponential graph, logarithmic curve, growth rate, decay model, inverse functions | `scripts.tools.generate_exponential_logarithm` |
| Generate rational and irrational function visualizations using JSXGraph.
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
Examples: "1" not 1, "0" not 0, "x" not x, "2*x+1" not 2*x+1 | `scripts.tools.generate_rational_function` |
| Generate systems of equations visualization using JSXGraph. Solve and visualize linear and nonlinear equation systems, find intersection points, show solution sets, and analyze system properties. Supports implicit equations, parametric systems, numerical solutions, and advanced analysis including matrix representation and phase portraits. | `scripts.tools.generate_equation_system` |
| Generate conic sections and high-degree polynomials using JSXGraph.
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
- ✗ { type: 'para' } → ✓ Use 'parabola' | `scripts.tools.generate_conic_section` |
| Number Line Inequality Tool — illustrate solution sets on a one-dimensional axis with JSXGraph.

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

Keywords: number line, inequality graph, interval notation, solution set, one dimensional plot | `scripts.tools.generate_number_line_inequality` |
| Generate economic competition market analysis charts including MC (Marginal Cost), AC (Average Cost), AVC (Average Variable Cost) curves, price line, and profit/loss areas. Ideal for perfect competition market analysis. | `scripts.tools.generate_economics_competition` |
| Generate structural engineering shear force and bending moment diagrams. Displays beam with loads, support reactions, and resulting force diagrams. All calculations should be done externally - this tool only visualizes the results. | `scripts.tools.generate_structural_force` |
| Generate economics isoquant and isocost analysis charts.
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
- ✓ { isoquants: [{ Q: 100, points: [[1,4], [2,2]] }] } → Correct | `scripts.tools.generate_economics_isoquant` |
| Normal Distribution Tool — visualize probability density curves with JSXGraph.

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

Keywords: normal curve, bell curve, z score, probability shading, statistics | `scripts.tools.generate_statistics_normal` |
| Generate function transformation sequence visualizations. Shows how a base function is transformed through a series of translations, scalings, and reflections. Ideal for teaching transformation concepts. | `scripts.tools.generate_transform_sequence` |
| Generate geometric logo designs using conic sections, polygons, and curves. Combines multiple geometric shapes with customizable styles to create logos and emblems. | `scripts.tools.generate_logo_design` |
| Linear Feasible Region Tool — visualise constraint systems and objectives with JSXGraph.

Use when the prompt involves linear programming, feasible regions, constraint sets, or identifying optimal points for an objective.

Capabilities:
- Plot constraint lines and shade the feasible polygon.
- Highlight vertices, objective direction, and best point when an objective is supplied.
- Configure domain bounds, labels, and styling for instructional diagrams.

Quick start example:
{ "constraints": [{ "a": 1, "b": 1, "c": 10 }, { "a": 1, "b": 0, "c": 0, "type": ">=" }] }

Keywords: feasible region, linear programming, constraint graph, objective optimization, LP diagram | `scripts.tools.generate_linear_feasible` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.generate_function_graph
工具描述：Function Graph Tool — render single or multiple functions with JSXGraph.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|functions|array|false|[]|Array of mathematical functions to plot. Each function has an expression and optional styling. Can be empty if only plotting points.|
|points|array|false| |Optional points to plot on the graph. Each point MUST have both x and y coordinates (numbers). Example: [{x: 0, y: 0, name: "Origin"}, {x: 1, y: 1}]|
|showDerivative|boolean|false|false|Whether to show the derivative of the first function|
|showIntegral|boolean|false|false|Whether to show the integral area of the first function|
|integralBounds|array|false| |Bounds for integral area [a, b], required if showIntegral is true|
|tangentAt|number|false| |X coordinate to show tangent line at|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_parametric_curve
工具描述：Parametric Curve Tool — plot curves defined by x(t) and y(t) with JSXGraph.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|curves|array|false|[{xExpression=Math.cos(t), yExpression=Math.sin(t), tMin=0.0, tMax=6.283185307179586, color=#0066cc, strokeWidth=2.0, dash=0.0}]|Array of parametric curves to plot. Each curve is defined by x(t) and y(t) expressions. tMin and tMax MUST be numbers, not strings. Examples: [{xExpression: 'Math.cos(t)', yExpression: 'Math.sin(t)', tMin: 0, tMax: 6.283185307179586}] for circle, [{xExpression: 't', yExpression: 't^2', tMin: -5, tMax: 5}] for parabola.|
|showTrace|boolean|false|false|Whether to show animated trace point moving along the curve|
|traceSpeed|number|false|1.0|Speed of the trace animation (1 = normal speed)|
|points|array|false| |Optional points to plot on the graph|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_geometry_diagram
工具描述：Generate interactive geometry diagrams using JSXGraph.
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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|points|array|false|[]|Array of points to create. Points can be referenced by name in other elements.|
|lines|array|false| |Array of lines, segments, or rays connecting points|
|circles|array|false| |Array of circles defined by center and radius or through-point|
|polygons|array|false| |Array of polygons defined by their vertices|
|angles|array|false| |Array of angles to display and measure|
|showMeasurements|boolean|false|false|Whether to show measurements (distances, angles)|
|construction|object|false| |Geometric constructions like perpendiculars, parallels, midpoints, and angle bisectors|
|style|object|false| |Custom style configuration for the diagram.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_vector_field
工具描述：Generate vector field visualizations using JSXGraph.
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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|fieldFunction|object|true| |Vector field function F(x,y) = (dx, dy) - REQUIRED field. MUST be an object with 'dx' and 'dy' STRING expressions (both with quotes). Example: {"dx": "1", "dy": "9 + 9*y"} NOT {dx: 1, dy: ...}|
|density|number|false|10.0|Number of vectors to show in each direction (density of the field)|
|scale|number|false|0.8|Scale factor for vector lengths (0.1 to 2.0)|
|arrowStyle|object|false| |Styling options for the vector arrows|
|streamlines|array|false| |Optional streamlines (integral curves) to show the flow of the field. MUST be an array of objects, not a boolean. Example: [{startX: 0, startY: 0}, {startX: 1, startY: 1}] or omit entirely.|
|singularPoints|array|false| |Optional singular/critical points to highlight|
|colorByMagnitude|boolean|false|false|Whether to color vectors based on their magnitude|
|showMagnitudeLegend|boolean|false|false|Whether to show a legend for magnitude colors|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_linear_system
工具描述：Linear System Tool — graph linear equations and inequalities using JSXGraph.

Use when the prompt asks to solve or visualise systems of linear equations, highlight intersection points, or show feasible regions for inequalities/objectives.

Capabilities:
- Plot multiple lines defined in ax + by = c form with automatic intersection markers.
- Shade inequality regions, overlay objective functions, and mark optimal points.
- Add auxiliary points and configure axes, bounds, and styling.

Quick start example:
{ "equations": [{ "a": 1, "b": 1, "c": 5 }, { "a": 1, "b": -1, "c": 1 }] }

Keywords: linear system, intersection graph, inequality shading, objective line, simultaneous equations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|equations|array|false|[{a=1.0, b=1.0, c=5.0}, {a=1.0, b=-1.0, c=1.0}]|Array of linear equations to plot (ax + by = c form). Example: [{a: 1, b: 1, c: 5}, {a: 1, b: -1, c: 1}]|
|inequalities|array|false|[]|Array of linear inequalities to plot and shade. Example: [{a: 1, b: 1, c: 10, type: '<='}]|
|showIntersections|boolean|false|true|Whether to highlight intersection points|
|showFeasibleRegion|boolean|false|true|Whether to highlight the feasible region for inequalities|
|objectives|array|false| |Objective functions for linear programming|
|points|array|false| |Additional points to highlight|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_function_transformation
工具描述：Function Transformation Tool — illustrate how a base function changes under common operations.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|baseFunction|object|false|{expression=x^2, color=#0066cc, strokeWidth=2.0, name=f(x)}|The original function to transform|
|transformations|array|false|[{type=translate, parameters={h=1.0, k=0.0}, strokeWidth=2.0, dash=0.0}]|Array of transformations to apply and visualize. Each transformation MUST have a valid 'type' field. For stretching/shrinking, use type: 'scale' (not 'stretch' or 'verticalStretch'). For shifting, use type: 'translate' (not 'shift' or 'move'). Examples: [{type: 'translate', parameters: {h: 2, k: 1}}] for horizontal shift right 2 and vertical shift up 1, [{type: 'scale', parameters: {a: 2}}] for vertical stretch by factor 2, [{type: 'reflect', parameters: {axis: 'x'}}] for reflection across x-axis.|
|showSteps|boolean|false|false|Whether to show intermediate transformation steps|
|showVectors|boolean|false|false|Whether to show transformation vectors for translations|
|highlightPoints|array|false| |Points to highlight on base and transformed functions|
|animateTransformation|boolean|false|false|Whether to animate the transformation with a slider|
|compareMode|string|false|"overlay"|How to display the functions|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_quadratic_analysis
工具描述：Quadratic Analysis Tool — visualize parabolas and their key features using JSXGraph.

Use when the prompt asks to analyse or sketch quadratic functions, compare parabolas, or explain vertex, intercepts, symmetry, or discriminant behavior.

Capabilities:
- Plot one or more quadratic functions with optional styling.
- Highlight vertices, intercepts, axis of symmetry, focus/directrix, and discriminant notes.
- Display vertex or factorized forms, tangent lines, shaded regions, and comparison layouts.

Quick start example:
{ "quadratics": [{ "a": 1, "b": 0, "c": 0 }] }

Keywords: quadratic graph, parabola analysis, vertex form, factor form, compare parabolas
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|quadratics|array|false|[{a=1.0, b=0.0, c=0.0}]|Array of quadratic functions to analyze (ax^2 + bx + c form). Provide at least one or rely on the default parabola y = x^2.|
|showVertex|boolean|false|true|Whether to show and label the vertex|
|showAxisOfSymmetry|boolean|false|true|Whether to show the axis of symmetry|
|showRoots|boolean|false|true|Whether to show and label the roots/x-intercepts|
|showYIntercept|boolean|false|true|Whether to show the y-intercept|
|showFocusDirectrix|boolean|false|false|Whether to show the focus and directrix|
|showDiscriminant|boolean|false|false|Whether to display discriminant value and root nature|
|vertexForm|boolean|false|false|Whether to display the vertex form: a(x-h)^2 + k|
|factorizedForm|boolean|false|false|Whether to display the factorized form if applicable|
|tangentLines|array|false| |Points where to draw tangent lines|
|shadeRegion|object|false| |Region to shade relative to the parabola|
|compareMode|string|false|"overlay"|How to display multiple quadratics|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_exponential_logarithm
工具描述：Exponential and Logarithmic Tool — plot growth, decay, and log curves with JSXGraph.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|functions|array|false|[{type=exponential, base=2.718281828459045, coefficient=1.0, hShift=0.0, vShift=0.0}]|Array of exponential and logarithmic functions to plot. Each function MUST have 'type' field set to 'exponential' or 'logarithm' (not 'logarithmic'). The 'base' field MUST be a number (e.g., 2, 10, 2.718281828459045), not a string. Examples: [{type: 'exponential', base: 2}] for y=2^x, [{type: 'logarithm', base: 10}] for y=log₁₀(x), [{type: 'logarithm'}] for y=ln(x) (base defaults to e), [{type: 'exponential', base: 0.5}] for y=(0.5)^x (decay).|
|showAsymptotes|boolean|false|true|Whether to show horizontal/vertical asymptotes|
|showIntercepts|boolean|false|true|Whether to show and label x and y intercepts|
|showInverse|boolean|false|false|Whether to show the inverse function|
|showReflectionLine|boolean|false|false|Whether to show y=x line for inverse relationship|
|comparisonPoints|array|false| |Points to compare function values|
|growthDecayAnalysis|object|false| |Growth and decay analysis options|
|logarithmicScale|object|false| |Logarithmic scale options|
|specialPoints|array|false| |Special points to highlight (e.g., (0,1) for exponentials)|
|tangentAt|array|false| |X coordinates where to show tangent lines|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_rational_function
工具描述：Generate rational and irrational function visualizations using JSXGraph.
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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|rationalFunctions|array|false| |Array of rational functions (P(x)/Q(x)) to plot. Both 'numerator' and 'denominator' MUST be STRING expressions, not numbers. Example: [{numerator: 'x^2 - 1', denominator: 'x - 2'}] for (x²-1)/(x-2). Even for constants, use strings: [{numerator: '1', denominator: 'x'}] for 1/x.|
|irrationalFunctions|array|false| |Array of irrational functions (involving roots) to plot|
|showVerticalAsymptotes|boolean|false|true|Whether to show vertical asymptotes|
|showHorizontalAsymptotes|boolean|false|true|Whether to show horizontal asymptotes|
|showObliqueAsymptotes|boolean|false|true|Whether to show oblique/slant asymptotes|
|showHoles|boolean|false|true|Whether to show removable discontinuities (holes)|
|showIntercepts|boolean|false|true|Whether to show x and y intercepts|
|showCriticalPoints|boolean|false|false|Whether to show local maxima and minima|
|showDomainRestrictions|boolean|false|true|Whether to highlight domain restrictions for irrational functions|
|analyzeEndBehavior|boolean|false|false|Whether to show end behavior analysis|
|factorization|object|false| |Factorization and simplification options|
|partialFractions|boolean|false|false|Whether to show partial fraction decomposition|
|tangentLines|array|false| |X coordinates where to draw tangent lines|
|shadeRegions|array|false| |Regions to shade|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_equation_system
工具描述：Generate systems of equations visualization using JSXGraph. Solve and visualize linear and nonlinear equation systems, find intersection points, show solution sets, and analyze system properties. Supports implicit equations, parametric systems, numerical solutions, and advanced analysis including matrix representation and phase portraits.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|systems|array|false| |Array of equation systems to solve and visualize|
|individualEquations|array|false| |Individual equations to plot (not part of a system)|
|showIntersections|boolean|false|true|Whether to highlight intersection points (solutions)|
|showSolutionSet|boolean|false|true|Whether to display the solution set algebraically|
|numericalSolutions|object|false| |Numerical solution options|
|parameterAnimation|object|false| |Options for animating parametric equations|
|solutionRegions|array|false| |Regions defined by equation systems|
|linearAlgebraView|object|false| |Linear algebra analysis for linear systems|
|nonlinearAnalysis|object|false| |Nonlinear system analysis options|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_conic_section
工具描述：Generate conic sections and high-degree polynomials using JSXGraph.
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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|conics|array|false| |Array of standard conic sections to plot. Each conic MUST have a 'type' field set to 'circle', 'ellipse', 'parabola', or 'hyperbola'. Examples: [{type: 'circle', center: {x: 0, y: 0}, radius: 5}], [{type: 'parabola', vertex: {x: 0, y: 0}, p: 1}], [{type: 'ellipse', center: {x: 0, y: 0}, a: 4, b: 2}].|
|generalConics|array|false| |Conic sections in general form: Ax² + Bxy + Cy² + Dx + Ey + F = 0|
|polynomials|array|false| |High-degree polynomial functions to plot|
|points|array|false| |Optional points to plot on the graph|
|showFoci|boolean|false|true|Whether to show foci for conics|
|showDirectrix|boolean|false|false|Whether to show directrix for parabolas and general conics|
|showAsymptotes|boolean|false|true|Whether to show asymptotes for hyperbolas|
|showCenter|boolean|false|true|Whether to mark the center of conics|
|showVertices|boolean|false|true|Whether to mark vertices of conics|
|showEccentricity|boolean|false|false|Whether to display eccentricity values|
|showTangents|array|false| |Tangent lines to draw|
|showPolynomialRoots|boolean|false|true|Whether to mark roots of polynomials|
|showCriticalPoints|boolean|false|false|Whether to show critical points of polynomials|
|showInflectionPoints|boolean|false|false|Whether to show inflection points of polynomials|
|degreeAnalysis|boolean|false|false|Whether to show polynomial degree and leading coefficient analysis|
|intersectionAnalysis|object|false| |Intersection analysis options|
|polarForm|boolean|false|false|Whether to show polar form equations for conics|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|axisXTitle|string|false|"x"|Label for X axis|
|axisYTitle|string|false|"y"|Label for Y axis|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_number_line_inequality
工具描述：Number Line Inequality Tool — illustrate solution sets on a one-dimensional axis with JSXGraph.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|inequalities|array|false|[{expression=x > 0, color=#0066cc, strokeWidth=3.0, showEndpoints=true, endpointRadius=0.15}]|Array of inequalities to plot on the number line. Each inequality MUST have an 'expression' field. Examples: [{expression: 'x > 2'}] for (2, ∞), [{expression: '0 <= x <= 5'}] for [0, 5], [{expression: 'x <= 3'}, {expression: '4 <= x <= 5'}] for union of (-∞, 3] ∪ [4, 5]. DO NOT use 'start', 'end', 'includeStart', or 'includeEnd' fields.|
|numberLinePosition|number|false|0.0|Y coordinate position of the number line|
|tickMarks|boolean|false|true|Whether to show tick marks on the number line|
|tickInterval|number|false|1.0|Interval between tick marks|
|showNumbers|boolean|false|true|Whether to show numbers on tick marks|
|numberInterval|number|false|1.0|Interval between number labels|
|style|object|false| |Custom style configuration for the chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|title|string|false|""|Set the title of the math chart.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_economics_competition
工具描述：Generate economic competition market analysis charts including MC (Marginal Cost), AC (Average Cost), AVC (Average Variable Cost) curves, price line, and profit/loss areas. Ideal for perfect competition market analysis.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|curves|object|true| |Cost curves for the firm|
|priceLine|number|true| |Market price P (horizontal line)|
|quantityRange|array|true| |Quantity range [min, max] for the x-axis|
|labels|object|false| |Custom labels for curves and areas|
|showProfit|boolean|false|true|Whether to shade the profit/loss area|
|showEquilibrium|boolean|false|true|Whether to mark the equilibrium point(s)|
|showShutdownPoint|boolean|false|false|Whether to mark the shutdown point (where P = min AVC)|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|
|axisXTitle|string|false|"Quantity (Q)"|null|
|axisYTitle|string|false|"Price/Cost ($)"|null|

---

## scripts.tools.generate_structural_force
工具描述：Generate structural engineering shear force and bending moment diagrams. Displays beam with loads, support reactions, and resulting force diagrams. All calculations should be done externally - this tool only visualizes the results.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|length|number|true| |Beam length L in meters|
|loads|array|true| |Array of loads applied to the beam|
|reactions|array|true| |Support reactions (externally calculated, not solved by this tool)|
|shear|array|true| |Shear force curve as discrete points [x, V(x)]|
|moment|array|true| |Bending moment curve as discrete points [x, M(x)]|
|deflection|array|false| |Deflection curve as discrete points [x, y(x)] (optional)|
|labels|object|false| |Custom labels for diagrams|
|showValues|boolean|false|true|Whether to show numerical values on diagrams|
|showDiagrams|object|false| |Which diagrams to display|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_economics_isoquant
工具描述：Generate economics isoquant and isocost analysis charts.
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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|isoquants|array|true| |Array of isoquant curves with their output levels and points - REQUIRED. Each isoquant MUST have 'Q' (output level) and 'points' (array of [L, K] coordinates). Example: [{Q: 100, points: [[1, 4], [2, 2], [4, 1]]}, {Q: 200, points: [[2, 8], [4, 4], [8, 2]]}]|
|isocosts|array|false| |Optional array of isocost lines|
|optimum|object|false| |Optimal point where isoquant is tangent to isocost|
|labels|object|false| |Custom labels for axes and curves|
|showMarginalRate|boolean|false|false|Whether to show marginal rate of technical substitution (MRTS)|
|showTangent|boolean|false|false|Whether to show tangent line at optimum point|
|productionFunction|string|false| |Production function expression for display, e.g., 'Q = AK^αL^β'|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|
|axisXTitle|string|false|"Labor (L)"|null|
|axisYTitle|string|false|"Capital (K)"|null|

---

## scripts.tools.generate_statistics_normal
工具描述：Normal Distribution Tool — visualize probability density curves with JSXGraph.

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
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|mean|number|false|0.0|Mean (μ) of the normal distribution|
|stddev|number|false|1.0|Standard deviation (σ) of the normal distribution|
|range|array|false|[-4.0, 4.0]|Range [min, max] for plotting the distribution|
|shade|array|false| |Interval [a, b] to shade for probability calculation|
|showStandardScale|boolean|false|false|Whether to show z-score scale on additional axis|
|showProbability|boolean|false|true|Whether to display the shaded area probability|
|showCriticalValues|boolean|false|false|Whether to mark critical values (±1σ, ±2σ, ±3σ)|
|labels|object|false| |⚠️⚠️⚠️ CRITICAL: labels MUST be an object with STRING properties, NOT nested objects! ⚠️⚠️⚠️
Type: object with string values
Each property (distribution, probability, mean, stddev) MUST be a STRING.
❌ WRONG examples:
  - {distribution: {text: "formula"}} (nested object)
  - {mean: {symbol: "μ"}} (nested object)
✅ CORRECT examples:
  - {distribution: "$f(x) = ...$"} (string)
  - {mean: "μ", stddev: "σ"} (strings)
  - {probability: "P(X < a)"} (string)|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|
|axisXTitle|string|false|"x"|null|
|axisYTitle|string|false|"Probability Density"|null|

---

## scripts.tools.generate_transform_sequence
工具描述：Generate function transformation sequence visualizations. Shows how a base function is transformed through a series of translations, scalings, and reflections. Ideal for teaching transformation concepts.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|base|string|true| |Base function expression, e.g., 'x^2', 'Math.sin(x)'|
|transforms|array|true| |Array of transformations to apply in sequence|
|final|string|false| |Final function expression for verification (optional)|
|showSteps|boolean|false|true|Whether to show intermediate transformation steps|
|showAnimation|boolean|false|false|Whether to animate the transformation sequence|
|stepColors|array|false| |Colors for each transformation step|
|labels|object|false| |Custom labels for base and final functions|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|
|axisXTitle|string|false|"x"|null|
|axisYTitle|string|false|"y"|null|

---

## scripts.tools.generate_logo_design
工具描述：Generate geometric logo designs using conic sections, polygons, and curves. Combines multiple geometric shapes with customizable styles to create logos and emblems.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|paths|array|true| |Array of geometric shapes that compose the logo|
|style|object|false| |Style configuration including default path styles|
|pathStyles|array|false| |Individual styles for each path (overrides defaults)|
|showGrid|boolean|false|false|Whether to show grid (usually off for logos)|
|showAxis|boolean|false|false|Whether to show axes (usually off for logos)|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|true|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|

---

## scripts.tools.generate_linear_feasible
工具描述：Linear Feasible Region Tool — visualise constraint systems and objectives with JSXGraph.

Use when the prompt involves linear programming, feasible regions, constraint sets, or identifying optimal points for an objective.

Capabilities:
- Plot constraint lines and shade the feasible polygon.
- Highlight vertices, objective direction, and best point when an objective is supplied.
- Configure domain bounds, labels, and styling for instructional diagrams.

Quick start example:
{ "constraints": [{ "a": 1, "b": 1, "c": 10 }, { "a": 1, "b": 0, "c": 0, "type": ">=" }] }

Keywords: feasible region, linear programming, constraint graph, objective optimization, LP diagram
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|constraints|array|false|[{a=1.0, b=1.0, c=10.0, type=<=}, {a=1.0, b=0.0, c=0.0, type=>=}, {a=0.0, b=1.0, c=0.0, type=>=}]|Array of linear inequality constraints. Example: [{a: 1, b: 1, c: 10}, {a: 1, b: 0, c: 0, type: '>='}]|
|domain|array|false|[0.0, 20.0, 20.0, 0.0]|Clipping domain [xmin, xmax, ymin, ymax] for the feasible region|
|objectiveFunction|object|false| |Optional objective function for linear programming|
|showVertices|boolean|false|true|Whether to mark vertices of the feasible region|
|showOptimalPoint|boolean|false|true|Whether to mark the optimal point (if objective function provided)|
|interactive|boolean|false|false|⚠️ Rendering mode selection:

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

Use static mode unless you need dynamic updates.|
|feasibleRegionStyle|object|false| |Style for the feasible region|
|labels|object|false| |Custom labels|
|style|object|false| |Custom style configuration for the chart.|
|title|string|false|""|Set the title of the math chart.|
|width|number|false|800.0|Set the width of the math chart, default is 800.|
|height|number|false|600.0|Set the height of the math chart, default is 600.|
|boundingBox|array|false| |The bounding box for the chart. Default is [-10, 10, 10, -10].|
|keepAspectRatio|boolean|false|false|Whether to keep aspect ratio.|
|showCopyright|boolean|false|false|Whether to show JSXGraph copyright.|
|showNavigation|boolean|false|true|Whether to show navigation controls.|
|zoom|object|false| |Zoom configuration for the chart.|
|pan|object|false| |Pan configuration for the chart.|
|axisXTitle|string|false|"x"|null|
|axisYTitle|string|false|"y"|null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据