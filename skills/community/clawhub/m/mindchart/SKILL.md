---
name: mindchart
description: Create exquisite infographics from user-uploaded files or given text. Used when user requests to create an infographic.
requirements: Requires node or bun environment, install the following dependencies：@antv/infographic, opentype.js, sharp
---

Infographics transform data, information, and knowledge into perceptible visual language. They combine visual design with data visualization, using intuitive symbols to compress complex information, helping audiences quickly understand and remember key points.

Before starting the task, you need to understand the AntV Infographic syntax specification, including template list, data structure, theme, etc.

**Strictly follow the generation workflow without any deviation**

## Specifications

### AntV Infographic Syntax

AntV Infographic syntax is a custom DSL for describing infographic rendering configuration. It uses indentation to express structure, suitable for AI to directly generate and stream output. Core information includes:

1. template: Expresses information structure using templates.
2. data: Infographic data, containing `title`, `desc`, and main data fields.
3. theme: Theme configuration, containing `palette`, fonts, stylization, etc.

### Mandatory Syntax Rules

- The first line must be `infographic <template-name>`.
- Template list only contains the template name itself; when actually outputting, the first line must explicitly write the `infographic` prefix.
- Use `data` / `theme` blocks, with uniform two-space indentation within blocks.
- Key-value pairs use `key space value`; object arrays use `-` as item prefix.
- `icon` uses icon keywords, e.g., `star fill`, `mingcute/server-line`.
- `value` should preferably use pure numeric values; numeric units should preferably be expressed in `label` or `desc`.
- `palette` recommends using inline simple array syntax, e.g., `palette #4f46e5 #06b6d4 #10b981`.
- Color values in `palette` are bare values, no quotes, no commas.
- `data` should contain only one main data field matching the template, avoid mixing `lists`, `sequences`, `compares`, `values`, `root`, `nodes` simultaneously.

Main data field selection rules:

- `list-*` → `lists`
- `sequence-*` → `sequences`, optional `order asc|desc`
- `sequence-interaction-*` → `sequences` + `relations`
  - `sequences` represents swimlane list
  - Each swimlane must contain `label`
  - `children` of each swimlane represents node list
  - Each item under `children` must be written as an object entry and contain `label`
  - Nodes optionally have `id`, `icon`, `step`, `desc`, `value`
  - `step` is used to indicate time hierarchy; same `step` is at the same height
- `compare-*` → `compares`
  - `compare-binary-*` / `compare-hierarchy-left-right-*`
    - The first layer of `compares` must have exactly two root nodes, representing the two parties being compared
    - Both root nodes should contain `children`
    - The actual comparison items are written under their respective `children`
    - Each item under `children` must be written as an object entry and contain `label`
    - Even if each side has only 1 metric, write it as 1 object entry inside `children`
  - `compare-swot`
    - `compares` can directly contain multiple root nodes
    - Each root node optionally has `children`
  - `compare-quadrant-*`
    - `compares` directly contains 4 quadrant root nodes
- `hierarchy-structure` → `items`
- `hierarchy-*` → single `root`, recursively nested through `children`
- `relation-*` → `nodes` + `relations`
  - Simple relations can also directly use arrow syntax to express relationships
- `chart-*` → `values`
  - `chart-line-plain-text` / `chart-bar-plain-text` / `chart-column-simple` all use single ordered `values`
  - Each data point uses `label` for category, uses `value` for numeric value
  - Line chart order is expressed by the order of entries in `values`
- When structure cannot be clearly determined, use `items` as fallback

Theme rules:

- `theme` is used for custom themes, e.g., `palette`, `base`, `stylize`
- Use `theme.base.text.font-family` to specify font, e.g., `851tegakizatsu`
- Use `theme.stylize` to select built-in styles and pass parameters
  - `rough`: hand-drawn effect
  - `pattern`: pattern fill
  - `linear-gradient` / `radial-gradient`: gradient style
- Only output Infographic syntax itself, do not output JSON, explanatory text, or additional Markdown paragraphs

## Template Selection Guidelines

- Strict sequence, step progression, stage evolution → `sequence-*`
- Multi-role or multi-system interaction → `sequence-interaction-*`
- Parallel point enumeration → `list-row-*` / `list-column-*` / `list-grid-*`
- Two-party comparison, plan comparison, before/after comparison → `compare-binary-*`
  - First determine who the two parties are
  - Then expand `children` for each party respectively
- SWOT analysis → `compare-swot`
- Quadrant analysis → `compare-quadrant-*`
- Hierarchical tree structure → `hierarchy-tree-*`
- Statistical trends, single sequence changes → `chart-line-plain-text`
- Statistical comparison, single group numeric comparison → `chart-bar-plain-text` / `chart-column-simple`
- Node relationships, process dependencies → `relation-*`
- Word frequency theme display → `chart-wordcloud`
- Mind map → `hierarchy-mindmap-*`

## Output Format

Only output one `plain` code block, without any explanatory text:

```infographic
infographic list-row-horizontal-icon-arrow
data
  title Title
  desc Description
  lists
    - label Item
      value 12.5
      desc Description
      icon document text
theme
  palette #3b82f6 #8b5cf6 #f97316
```

## Generation Workflow

### Step 1: Understand User Requirements and Select Suitable Template

Deeply think and understand user requirements, select one appropriate template according to the `Template Selection Guidelines` above.

**Template directory: `mindchart/templates/`**

### Step 2: Generate Infographic Syntax File

Generate infographic syntax file according to template syntax and the `Specifications` above.

- **Syntax file format: `{title}.md`**
- Ensure the generated infographic displays with **white background and black text and icons**
- Ensure the length of `desc` field is less than 17 tokens

#### Self-Check Checklist

Before outputting, check the following:

- Is the first line `infographic <template-name>`?
- Is only one main data field matching the template used?
- Is `palette` using bare color values without quotes and commas?
- Are swimlane nodes of `sequence-interaction-*` all written as `children -> - label ...`?
- Do `compare-binary-*` / `compare-hierarchy-left-right-*` have only two root nodes, with content on both sides placed under their respective `children`?
- Does each item under `children` explicitly contain `label`?
- Does `chart-line-plain-text` use single ordered `values`?
- Is there no JSON, explanatory text, or extra code blocks in the output?

### Step 3: Generate SVG File

```bash
node mindchart/scripts/ifgc2svg {title}.md {title}.svg
```

### Step 4: Convert to PNG File

```bash
node mindchart/scripts/svg2png {title}.svg {title}.png
```

### Step 5: Return PNG/SVG File

- If user is using openclaw or other bot, send png and svg as images to the user
- In other cases, save svg and png to the specified directory or project directory
