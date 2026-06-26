---
name: figma
description: |
  Figma design asset reading, code generation, and MCP integration. Covers REST API direct calls and MCP Server capabilities for design-to-code workflows.

  **Use when**:
  (1) Reading Figma file structure, components, styles, variables
  (2) Generating frontend code from design files (React/Vue/HTML)
  (3) Writing back to Figma canvas via MCP Server (create/modify frames, components, variables)
  (4) Extracting design tokens (colors, spacing, typography) for code implementation
  (5) User mentions "Figma", "design file", "component library", "design to code", "UI implementation"
  (6) Integrating with Claude Code / Codex for Design-to-Code workflows
---

# Figma Skill

## Installation

### For OpenClaw agents (ClawHub)
```bash
clawhub install figma
```

### For Claude Code (MCP Server)
```bash
# Add Figma MCP (one-time, global)
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# Or install the official Figma plugin (includes Skills)
claude plugin install figma@claude-plugins-official
```

### For Codex CLI
```bash
codex mcp add figma --transport http https://mcp.figma.com/mcp
```

### Environment
Set `FIGMA_TOKEN` (Personal Access Token) in your environment or `.env` file.
Generate at: https://www.figma.com/settings → Account → Personal access tokens

---

## Quick Reference

### Two access methods

| Method | Use case | Auth |
|--------|----------|------|
| **REST API** (`scripts/figma_api.py`) | Read file structure, components, export images | `FIGMA_TOKEN` |
| **MCP Server** (`https://mcp.figma.com/mcp`) | Interactive design-to-code, write to canvas | OAuth (auto) |

---

## 1. REST API — Direct File Access

Use `scripts/figma_api.py` to query Figma files directly. Supports full URLs or file keys.

### Commands

```bash
# File structure
python3 scripts/figma_api.py pages <file_key_or_url>

# Frame tree (depth controls levels)
python3 scripts/figma_api.py tree <file_key> --node <page_id> --depth 3

# Published components (--group to aggregate by frame)
python3 scripts/figma_api.py components <file_key> --group

# Component sets
python3 scripts/figma_api.py component-sets <file_key>

# Styles
python3 scripts/figma_api.py styles <file_key>

# Export as PNG/SVG
python3 scripts/figma_api.py export <file_key> --nodes <id1>,<id2> --format png --scale 2

# Node JSON detail
python3 scripts/figma_api.py node <file_key> --node <node_id> --depth 4

# Current user info
python3 scripts/figma_api.py me
```

---

## 2. MCP Server — 14 Tools

### Read tools (any Figma plan)
| Tool | Purpose |
|------|---------|
| `get_design_context` | Design context → code (default React+Tailwind, customizable) |
| `get_variable_defs` | Variables and styles (colors, spacing, typography) |
| `get_metadata` | Sparse XML: layer IDs, names, types, positions, sizes |
| `get_screenshot` | Screenshot of selection |
| `get_code_connect_map` | Figma node → code component mapping (needs Code Connect) |
| `search_design_system` | Search library components, variables, styles |
| `whoami` | Authenticated user info |

### Write tools (beta free, needs Full seat + edit permission)
| Tool | Purpose |
|------|---------|
| `use_figma` | Execute Figma Plugin API JS: create/modify frames, components, variables, auto layout |
| `generate_figma_design` | Convert live browser UI → editable Figma layers |
| `create_new_file` | Create new file in Drafts |
| `generate_diagram` | Mermaid syntax → FigJam diagram |

### Helper tools
| Tool | Purpose |
|------|---------|
| `create_design_system_rules` | Generate design system rules file for AI code generation |
| `add_code_connect_map` | Add Figma node → code component mapping |
| `get_code_connect_suggestions` | Code Connect mapping suggestions |

### Write limitations
- 20KB response limit per call
- No image/asset import support
- Full seat required (Dev seat = read-only)
- Large changes: inspect first → incremental create/update → verify

---

## 3. Design-to-Code Workflow

### For Claude Code / Codex (via MCP)

**Step 1** — Provide the Figma frame URL in your prompt:
```
Using this Figma frame: https://www.figma.com/design/<key>?node-id=<id>
Generate React components using [your component library].
```

**Step 2** — For large pages, ask the agent to inspect first:
```
1. Use get_metadata on the frame to understand the structure
2. Use search_design_system to find matching library components
3. Use get_design_context on each section to generate code
```

**Step 3** — Write back to Figma (if editor permission):
```
Using this file: <url>, create a new page and build [description]
using existing components. Use auto layout.
```

### For OpenClaw agents (via REST API)

1. `figma_api.py pages <url>` → identify target page
2. `figma_api.py tree <key> --node <page_id>` → understand structure
3. `figma_api.py export <key> --nodes <frame_id>` → get screenshot
4. `figma_api.py node <key> --node <frame_id> --depth 4` → get component details
5. Generate code using the structural data + screenshot

### Best practices
- Always specify frontend framework and component library in prompts
- Large pages: `get_metadata` overview first, then `get_design_context` per section
- Use `get_screenshot` for layout-sensitive components
- Rate limit: space REST API calls ≥500ms apart
- Keep `depth` ≤ 4 to avoid timeouts on large files

---

## 4. Asset Registry

Register your Figma files in `references/omada-assets.md` for quick lookup.
See `references/guide-for-agents.md` for the complete agent operation manual.
See `references/guide-for-humans.md` for the human-facing usage guide.
