# Theme System: Light & Dark

## Overview

Since v0.5.0, all visual exports support two color themes: `light` (default) and `dark`.
Themes are applied consistently across SVG, HTML viewer, and all specialized export views.

## CLI Usage

```bash
# Light theme (default)
business-blueprint --html output.html --from solution.blueprint.json

# Dark theme
business-blueprint --html output.html --theme dark --from solution.blueprint.json

# Export all formats in dark theme
business-blueprint --export solution.blueprint.json --theme dark
```

## Color Palettes

### Light Theme (`C_LIGHT`)

| Token | Value | Purpose |
|-------|-------|---------|
| `bg` | `#F8FAFC` | Page background |
| `canvas` | `#FFFFFF` | Card/panel surface |
| `text_main` | `#0F172A` | Primary text |
| `text_sub` | `#64748B` | Secondary text |
| `cap_fill` | `#E8F5F5` | Capability node fill |
| `cap_stroke` | `#0B6E6E` | Capability node stroke |
| `sys_fill` | `#EFF6FF` | System node fill (default) |
| `sys_stroke` | `#3B82F6` | System node stroke (default) |
| `actor_fill` | `#FFF7ED` | Actor node fill |
| `actor_stroke` | `#F97316` | Actor node stroke |
| `flow_fill` | `#FEFCE8` | Flow step fill |
| `flow_stroke` | `#CA8A04` | Flow step stroke |
| `arrow` | `#0B6E6E` | Primary arrow color |

### Dark Theme (`C_DARK`)

| Token | Value | Purpose |
|-------|-------|---------|
| `bg` | `#020617` | Page background (Slate-950) |
| `canvas` | `#0F172A` | Card/panel surface (Slate-900) |
| `text_main` | `#E2E8F0` | Primary text |
| `text_sub` | `#94A3B8` | Secondary text |
| `cap_fill` | `#064E3B` | Capability node fill |
| `cap_stroke` | `#34D399` | Capability node stroke |
| `sys_fill` | `#1E3A5F` | System node fill (default) |
| `sys_stroke` | `#60A5FA` | System node stroke (default) |
| `actor_fill` | `#451A03` | Actor node fill |
| `actor_stroke` | `#FB923C` | Actor node stroke |
| `flow_fill` | `#422006` | Flow step fill |
| `flow_stroke` | `#FBBF24` | Flow step stroke |
| `arrow` | `#34D399` | Primary arrow color |

### Dark Theme Extras

- **40px grid pattern**: Subtle grid overlay on dark backgrounds
- **HTML grid**: CSS `background-size: 40px 40px` with `rgba(255,255,255,0.03)` lines
- **SVG grid**: `<pattern id="grid">` with `#1E293B` stroke

## Semantic Colors (System Nodes)

System nodes are colored by their `category` field. When no category is set,
the default `sys_fill`/`sys_stroke` is used.

| Category | Aliases | Light Color | Dark Color |
|----------|---------|-------------|------------|
| `frontend` | web, mobile, ui | `#0891B2` (Cyan) | `#22D3EE` |
| `backend` | api, service, microservice | `#10B981` (Emerald) | `#34D399` |
| `database` | storage | `#8B5CF6` (Violet) | `#A78BFA` |
| `cloud` | infra, infrastructure, devops | `#F59E0B` (Amber) | `#FBBF24` |
| `security` | auth | `#F43F5E` (Rose) | `#FB7185` |
| `external` | third-party, third_party, saas | `#64748B` (Slate) | `#94A3B8` |

### Example Blueprint

```json
{
  "systems": [
    {"id": "sys-web", "name": "Web App", "category": "frontend", "capabilityIds": ["c1"]},
    {"id": "sys-api", "name": "API Gateway", "category": "backend", "capabilityIds": ["c1"]},
    {"id": "sys-db", "name": "PostgreSQL", "category": "database", "capabilityIds": ["c2"]}
  ]
}
```

## Implementation Details

### Theme Resolution

- `export_svg.py`: `_resolve_theme("dark")` returns `C_DARK` dict
- `export_html.py`: Same function imported from `export_svg`
- All `_build_*_svg()` functions accept `colors` parameter
- All `export_*_svg()` functions accept `theme` parameter (string)

### Function Signatures

```python
def export_svg(blueprint: dict, target: Path, theme: str = "light") -> None
def export_html_viewer(blueprint: dict, target: Path, theme: str = "light") -> None
def export_capability_map_svg(blueprint: dict, target: Path, theme: str = "light") -> None
def export_swimlane_flow_svg(blueprint: dict, target: Path, theme: str = "light") -> None
def export_product_tree_svg(blueprint: dict, target: Path, theme: str = "light") -> None
def export_matrix_svg(blueprint: dict, target: Path, theme: str = "light") -> None
```

### Summary Cards

All SVG exports include 5 summary cards at the bottom:
1. **SYSTEMS** - Count of system entities
2. **CAPABILITIES** - Count of capability entities
3. **ACTORS** - Count of actor entities
4. **FLOW STEPS** - Count of flow step entities
5. **COVERAGE** - % of systems with capability mappings

HTML viewer includes the same cards as a responsive grid between tabs and SVG views.
