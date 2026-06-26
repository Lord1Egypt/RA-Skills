---
name: kai-business-blueprint
description: Use when turning presales requirements, meeting notes, or solution materials into editable business capability blueprints, swimlane flows, and application architecture diagrams. Use when generating blueprint JSON, static HTML viewers, or exporting to SVG, draw.io, Excalidraw, or Mermaid formats. When no standard export template applies, default to free-flow output.
---

# Business Blueprint Skill

Use the Python scripts in this repository as the execution surface.

## Output Directory

All generated files (blueprint JSON, viewers, exports) go into `projects/workspace/` — not the repository root.

```bash
python scripts/business_blueprint/cli.py --plan projects/workspace/solution.blueprint.json --from "..."
python scripts/business_blueprint/cli.py --project projects/workspace/solution.blueprint.json
python scripts/business_blueprint/cli.py --export projects/workspace/solution.blueprint.json
```

## Industry Selection

Choose `--industry` from exactly one of: `"common"`, `"finance"`, `"manufacturing"`, `"retail"`. Select the closest match based on the user's domain and materials; do not invent other values.

| Industry | Hints content |
|----------|-------------|
| `common` | No hints — generic domains |
| `finance` | Risk control, credit, compliance, customer profile, etc. |
| `manufacturing` | Production planning, quality, warehouse, supply chain, etc. |
| `retail` | Store operations, membership, POS, order fulfillment, etc. |

## How to Generate a Blueprint

The AI agent is responsible for entity extraction. The Python tool handles JSON writing, visualization, and export.

### Step 1: Read industry hints

Read the seed template at `business_blueprint/templates/{industry}/seed.json` and get the `industryHints.checklist`.

### Step 2: Extract entities from source text

Using the user's source material AND the industry hints checklist, extract:
- **capabilities**: business capability areas (name, description)
- **actors**: roles/people involved (name)
- **flowSteps**: business process steps (name, actorId, capabilityIds, stepType)
- **systems**: IT systems that support capabilities
  - See `references/entities-schema.md` for all entity field definitions
  - See `references/systems-schema.md` for systems category/layer rules
  - See `scripts/business_blueprint/templates/common/seed.json` for field examples

**Domain-knowledge mode** (when seed has `meta.blueprintType: "domain-knowledge"`,
e.g. `cross-border-ecommerce`): entities go into `library.knowledge.*`
(painPoints / strategies / rules / metrics / practices / pitfalls), not the
architecture buckets above. The seed's `industryHints.knowledgeHints.namingHints`
section, when present, dictates content granularity:
- `strategy.name` must be a 4-10 字 product-grade noun phrase
  (e.g. "统一归因模型", "AIGC 素材工厂"), not an action ("优化素材") or a
  dimension ("测款节奏"). Reference the seed's `strategy_named_examples`.
- `painPoint.audience` and `strategy.audience` are free-string fields tagging
  the primary persona ("品牌方/DTC", "平台卖家", "代运营/服务商"). Multiple
  values comma-separated. No standalone persona entity is required.
- `metric.forecast: {direction, magnitude, unit}` is optional and used for
  commitments to the customer ("ROAS 提升 25%"). Keep `value`/`benchmarkContext`
  for current baseline; the two coexist as "now X, can reach Y".

These fields are pass-through under v2 minimal-validation: the validator does
not enforce them, but renderers and pitch flows consume them.

### Step 3: Write the blueprint JSON

Write the JSON file directly to the output path. Use this schema:

```json
{
  "version": "1.0",
  "meta": {
    "title": "...",
    "industry": "retail",
    "revisionId": "rev-YYYYMMDD-NN",
    "parentRevisionId": null,
    "lastModifiedAt": "ISO8601",
    "lastModifiedBy": "ai"
  },
  "context": {
    "goals": [],
    "scope": [],
    "assumptions": [],
    "constraints": [],
    "sourceRefs": [{"type": "inline-text", "excerpt": "..."}],
    "clarifyRequests": [],
    "clarifications": []
  },
  "library": {
    "capabilities": [
      {"id": "cap-xxx", "name": "...", "level": 1, "description": "...", "ownerActorIds": [], "supportingSystemIds": []}
    ],
    "actors": [
      {"id": "actor-xxx", "name": "..."}
    ],
    "flowSteps": [
      {"id": "flow-xxx", "name": "...", "actorId": "actor-xxx", "capabilityIds": ["cap-xxx"], "systemIds": [], "stepType": "task", "inputRefs": [], "outputRefs": []}
    ],
    "systems": [
      {"id": "sys-xxx", "kind": "system", "name": "...", "aliases": [], "description": "...", "resolution": {"status": "canonical", "canonicalName": "..."}, "capabilityIds": ["cap-xxx"]}
    ]
  },
  "relations": [
    {"id": "rel-xxx", "type": "supports", "from": "sys-xxx", "to": "cap-xxx", "label": "支撑"}
  ],
  "views": [],
  "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
  "artifacts": {}
}
```

### Step 4: Generate visualizations

```bash
python scripts/business_blueprint/cli.py --export <blueprint.json>
```

This generates SVG + HTML viewer by default. Use `--format drawio|excalidraw|mermaid` for other formats.

## Export View Selection Policy

Treat export view choice as a routing decision, not a styling preference.

- If a request matches a supported, standard export template, use that template.
- If there is no standard export template for the requested diagram, fall back to `freeflow`.
- Do **not** substitute `swimlane`, `matrix`, `product tree`, or other generic views just because they are available.
- When embedding a blueprint diagram into a report or ad hoc analysis, `freeflow` is the safe default unless the user explicitly asks for a supported standard template.

### Step 5: Generate downstream projection

```bash
python scripts/business_blueprint/cli.py --project <blueprint.json>
```

This generates `solution.projection.json`, the canonical machine projection consumed by downstream report/slide workflows.

## Workflow Decision Tree

```
User provides raw requirements / meeting notes?
  → AI agent reads hints, extracts entities, writes blueprint JSON
  → Optionally run --project for downstream machine handoff
  → Then run --export for visualization

User needs diagram files (SVG, draw.io, etc.)?
  → --export (default: SVG + HTML viewer)

User unsure about blueprint quality?
  → --validate

User wants downstream report / slide generation?
  → --project
```

## Commands

| Command | Description |
|---------|-------------|
| `--plan <path> --from <text>` | Generate empty blueprint JSON from source text (AI should prefer writing JSON directly) |
| `--project <path>` | Generate canonical projection JSON for downstream skills |
| `--export <path>` | Export SVG + HTML viewer (default), or use `--format` for other formats |
| `--validate <path>` | Validate a blueprint and print JSON results |

**Execution**: Run directly as scripts:
```bash
python scripts/business_blueprint/cli.py --plan ...
python scripts/business_blueprint/cli.py --export ...
```

## Export Formats

| Format | File | Use Case |
|--------|------|----------|
| `svg` (default) | `solution.exports/solution.svg` + HTML viewer | Quick preview, embedding |
| `drawio` | `solution.exports/solution.drawio` | Editable diagrams |
| `excalidraw` | `solution.exports/solution.excalidraw` | Whiteboard-style diagrams |
| `mermaid` | `solution.exports/solution.mermaid.md` | GitHub-native rendering |

## Collaboration Boundary

This skill produces **semantic intermediate artifacts**. Downstream skills consume them:

- `report-creator` consumes `solution.projection.json` → assembles reports
- `slide-creator` consumes `solution.projection.json` → assembles presentations
- Other skills may consume `relations` → generate PlantUML or other diagram syntax
- Downstream skills should **never directly edit** `solution.blueprint.json`
- `solution.handoff.json` is viewer-only metadata, not a downstream narrative input

## Sandbox Execution

When running in an isolated Python sandbox (Jupyter, notebook, cloud REPL) that auto-installs dependencies:

1. **The sandbox uses scripts directly.** Run execution scripts from the repository root:
   ```python
   import subprocess
   subprocess.run(["python", "scripts/business_blueprint/cli.py", "--export", "solution.blueprint.json"])
   ```
   - `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` — will raise NameError
   - `subprocess.run(["business-blueprint", ...])` — sandbox runs Python cells, not shell
   - `os.system()` — same reason

## Architecture Diagram Generation

When user requests an architecture diagram (keywords: "架构图", "architecture diagram", "--export", "diagram"):

1. Read `references/architecture-design-system.md` for the complete design system.
2. Read the appropriate template from `references/architecture-templates/` based on the user's domain:
   - AWS/Serverless/Lambda → `serverless.md`
   - Microservices/Kubernetes/微服务 → `microservices.md`
   - Other → use `serverless.md` as a structural reference
3. Read the blueprint JSON to extract entities and flow steps.
4. Generate a self-contained HTML file with inline SVG following the design system rules.
5. Write the output file to the same directory as the blueprint JSON.

If the request does not match one of the supported standard templates above, stay on the default `freeflow` export path. Do not switch to another generic view type as a fallback.
If a standard template would create a squeezed, clipped, or overcrowded diagram, stop using the fixed template geometry and fall back to `freeflow` or a wrapped multi-row layout.

### Route eligibility matrix

Use an explicit route contract before rendering:

| Route | Structural prerequisites | First fallback | Terminal behavior |
|------|---------------------------|----------------|-------------------|
| `freeflow` | Any valid blueprint with at least one renderable node or relation | None | If integrity still fails, export exits non-zero with a structural diagnostics payload |
| `architecture-template` | Recognizable L→R architecture shape, categorized systems, limited per-layer density, and no route-breaking overflow risk | `freeflow` | Same as above |
| `poster` | Clear layer/group structure with bounded peer density per row or wrapped-row support | wrapped poster or `freeflow` | Same as above |
| `swimlane` | Actor-owned flow steps with meaningful lane grouping | `freeflow` | Same as above |
| `hierarchy` | Stable tree/group relationship with low ambiguity in parent-child grouping | `freeflow` | Same as above |
| `evolution` | Ordered chronological or staged progression data | `freeflow` | Same as above |

Do not invent route heuristics ad hoc inside a renderer. Route eligibility must stay explicit and reviewable.

### Generation Rules
- Use dark mode by default (`#020617` bg + 40px grid). Only use light mode when the user explicitly asks for it.
- L→R data flow: Clients(左) → Frontend → Backend → Database(右)
- Map `systems[].category` to semantic colors from the design system
- Map `systems[].properties.type == "aws"` → AWS Region boundary box
- Map `systems[].properties.type == "k8s"` → Kubernetes Cluster boundary box
- Use `flowSteps[].seqIndex` for L→R ordering
- Component sizing: 0-1 cap = small(44px h), 2-4 = medium(80px h), 5+ = large(80px h)
- Layout must be content-driven. Never force every node in a layer into one fixed row if that creates toothpaste-style squeezing.
- When a layer has more than 3 peer nodes, or labels/features become tight, wrap into multiple rows or widen the canvas before shrinking the content.
- Render users/actors as actor labels, badges, or lane headers by default. Do not render them as ordinary system cards unless the user explicitly asks for that visual treatment.
- Legend must live in a bottom safe area and participate in canvas sizing. Never place the legend as a floating overlay in the top-right corner.
- Final SVG/HTML height must be derived from the bottom-most node, legend, summary cards, and footer plus padding. Do not use fixed-height wrappers or `overflow: hidden` that can clip the last row.
- Z-order: bg → grid → title → region → arrows → nodes → legend → cards → footer
- Component border: `rx="8"`, `stroke-width="2"`
- Region border: `rx="16"`, `stroke-dasharray="8,4"`, `opacity="0.4"`
- Geometry-sensitive integrity checks must use the numeric thresholds from `evals/export-integrity-thresholds.json`, not prose heuristics.

### Output
- Single HTML file: `{blueprint_stem}.html` alongside the blueprint JSON
- No external dependencies (except Google Fonts CDN for JetBrains Mono)
- Opens in any browser, printable to PDF

## Error Handling

- If `--validate` returns errors: fix structural issues before proceeding to `--export`.
- If `--validate` returns only warnings: proceed but note the warnings in any handoff.
- If Python version < 3.12: the package will refuse to install. Use `python3 -m business_blueprint.cli` with system Python as fallback.
- If a specialized route fails integrity: fall back to its configured fallback route.
- If `freeflow` also fails integrity: export exits non-zero with a structural diagnostics payload instead of emitting a silently broken artifact.

## Cross-Platform Scope

Phase 2 does not attempt full Windows terminal parity.

Known deferred cases:
- PowerShell pipe quirks beyond documented CLI contract tests
- console-default encoding issues outside explicit UTF-8 execution paths

Accepted workaround for encoding-sensitive runs:
# Use scripts directly (pure Skill, no package structure)
   subprocess.run(["python", "scripts/business_blueprint/cli.py", "--export", str(blueprint_path)])
- set `PYTHONIOENCODING=utf-8` where needed
