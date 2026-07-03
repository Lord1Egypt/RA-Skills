---
name: "power-cad-drafter"
description: "Auto-generate electrical CAD drawings from survey data and auto-audit against power codes"
---

# Power CAD Drafter

Auto-generate DXF construction drawings for 10kV and below power distribution projects, and auto-audit against the company design code and national standards.

## Trigger

- User provides survey data, hand-drawn sketches, or design task brief
- User requests electrical single-line diagrams, layout plans, or system diagrams
- User requests drawing review or verification

## Prerequisites

```bash
python3 -m pip install ezdxf pyyaml
```

Company code must exist: `workspace/电力行业施工图设计规范V1.0.md`

## Workflow

### 1. Parse Input Data
Extract structured survey data from user input or parse hand-drawn sketches via vision.

Recommended input format (YAML/JSON):
```yaml
project:
  name: "XX小区配电工程"
  type: "residential"
survey:
  building_floors: 18
  units_per_floor: 6
  total_area_sqm: 25000
  substation_dimensions: [8.5, 6.2]
```

### 2. Design Parameter Inference
Infer design parameters per the company code:

| Item | Input | Output Rule |
|------|-------|-------------|
| Load calculation | Area, units, load density | Demand factor method |
| Transformer | Load, location | Dry/oil, D,yn11, standard capacity |
| Main wiring | Load grade, transformer count | Single bus / sectionalized |
| Grounding | Substation location | TN-S (indoor), TN-C-S (outdoor) |
| Cable | Transformer capacity, routing | Ampacity + thermal + voltage drop |
| Room layout | Equipment count, dimensions | Aisle width, fire rating, noise |

### 3. Generate DXF Drawings
Run `scripts/dxf_generator.py` to produce:

| Drawing | Suffix | Content |
|---------|--------|---------|
| Single-line diagram | `_single_line.dxf` | 10kV and 0.4kV primary system |
| Layout plan | `_layout.dxf` | Equipment positioning, dimensions, aisles |
| Grounding plan | `_grounding.dxf` | Grounding electrodes, equipotential bonding |
| Cable routing | `_cable.dxf` | Trench/bridge paths, cable labels |

### 4. Auto-Audit
Run `scripts/audit_engine.py` to check against the code and produce a Markdown report.

Core checklist:
- Load grade matches power supply configuration
- Transformer capacity ≤ limits (dry ≤1250kVA public, oil ≤630kVA public)
- Wiring group D,yn11
- HV switchgear IP ≥ IP4X, five-prevention interlock
- LV breaker breaking capacity ≥ short-circuit current
- TN-S grounding mandatory for indoor substations
- Substation roof fire rating ≥ grade 2
- Aisle width ≥ 1.5m (fixed) / 1.8m (drawer)
- Bare conductor height ≥ 2.5m
- Cable sections ≥ minimums (service ≥10mm² copper, main ≥150mm²)
- Grounding resistance ≤ 4Ω (≥100kVA transformer)
- Meter height 0.8–1.8m
- Reactive compensation 20%–40% of transformer capacity

Report format:
```markdown
| Category | Item | Result | Design | Required | Clause | Remark |
|----------|------|--------|--------|----------|--------|--------|
```

## Deliverables

`project_name_cad_package.zip` containing:
- `drawings/` — DXF files (4 sheets)
- `design_params.json` — All inferred parameters
- `audit_report.md` — Audit report with pass/fail and corrective actions
- `equipment_list.csv` — Bill of materials

## Scripts

- `scripts/dxf_generator.py` — Core DXF drawing engine (single-line, layout, grounding, cable)
- `scripts/audit_engine.py` — Rule-based audit engine, loads design params and checks compliance
- `references/drawing_symbols.md` — Drawing legend and symbol standards per GB/T 4728
