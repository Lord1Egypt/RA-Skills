---
name: paper-design
description: Design UI screens in Paper — a professional design tool running locally on macOS. Create artboards, write HTML into designs, take screenshots, and iterate visually.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎨","homepage":"https://paper.design","requires":{"bins":["curl","python3"]},"os":["darwin"]}}
---

# Paper Design — MCP Bridge Skill

Paper is a professional design tool (like Figma) that runs locally on macOS. This skill connects to Paper's MCP server via HTTP, giving you full design capabilities.

**Prerequisite:** Paper must be open with a design file loaded. If Paper is not running, tell the user to open it first.

## How to Use Paper

All Paper operations go through the `paper.sh` script in this skill's directory:

```bash
exec {baseDir}/paper.sh <tool_name> '<json_arguments>'
```

**Important:** Always quote JSON arguments with single quotes to prevent shell expansion.

## Quick Start

```bash
# 1. Check what's on the canvas
exec {baseDir}/paper.sh get_basic_info

# 2. Create a new mobile artboard
exec {baseDir}/paper.sh create_artboard '{"name":"Home Screen","styles":{"width":"390px","height":"844px","display":"flex","flexDirection":"column","backgroundColor":"#FAFAFA"}}'

# 3. Add content (one visual group at a time)
exec {baseDir}/paper.sh write_html '{"html":"<div layer-name=\"Header\" style=\"display:flex;padding:60px 20px 20px;align-items:center\"><span style=\"font-family:Inter Tight;font-size:28px;font-weight:700;color:#1A1A1A\">Home</span></div>","targetNodeId":"ARTBOARD_ID","mode":"insert-children"}'

# 4. Take a screenshot to review
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}'
# → saves to /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg

# 5. View the screenshot
image /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg

# 6. When done, release the working indicator
exec {baseDir}/paper.sh finish_working_on_nodes
```

## Tool Reference

### Reading the Canvas

| Command | Purpose |
|---------|---------|
| `paper.sh get_basic_info` | File name, page, artboards, fonts in use |
| `paper.sh get_selection` | Currently selected nodes on canvas |
| `paper.sh get_node_info '{"nodeId":"ID"}'` | Size, visibility, parent, children, text |
| `paper.sh get_children '{"nodeId":"ID"}'` | Direct children with IDs and types |
| `paper.sh get_tree_summary '{"nodeId":"ID"}'` | Compact hierarchy overview (cheap) |
| `paper.sh get_tree_summary '{"nodeId":"ID","depth":5}'` | Deeper hierarchy |
| `paper.sh get_computed_styles '{"nodeIds":["ID1","ID2"]}'` | CSS styles for nodes |
| `paper.sh get_jsx '{"nodeId":"ID"}'` | JSX code (for dev handoff) |
| `paper.sh get_font_family_info '{"familyNames":["Inter","DM Sans"]}'` | Font availability + weights |

### Visual Review

```bash
# Screenshot an artboard or node
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}'

# Higher resolution (for reading small text)
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID","scale":2}'

# Save to specific path
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}' --save /tmp/my-review.jpg

# Then view the screenshot with the image tool
image /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg
```

### Creating Designs

```bash
# Create artboard (mobile)
exec {baseDir}/paper.sh create_artboard '{"name":"Screen Name","styles":{"width":"390px","height":"844px","display":"flex","flexDirection":"column","backgroundColor":"#FFFFFF"}}'

# Create artboard (desktop)
exec {baseDir}/paper.sh create_artboard '{"name":"Dashboard","styles":{"width":"1440px","height":"900px","display":"flex","flexDirection":"column","backgroundColor":"#F5F5F5"}}'

# Create related artboard (positioned next to existing)
exec {baseDir}/paper.sh create_artboard '{"name":"Screen V2","relatedNodeId":"EXISTING_ID","styles":{"width":"390px","height":"844px"}}'
```

### Writing HTML into Designs

```bash
# Add elements as children of a node
exec {baseDir}/paper.sh write_html '{"html":"<div style=\"...\">content</div>","targetNodeId":"PARENT_ID","mode":"insert-children"}'

# Replace an existing node
exec {baseDir}/paper.sh write_html '{"html":"<div style=\"...\">new content</div>","targetNodeId":"OLD_NODE_ID","mode":"replace"}'
```

**HTML Rules (critical):**
- Always use inline styles (`style="..."`)
- Use `display: flex` for ALL layouts — no grid, no inline, no tables
- Use padding and gap for spacing — NO margins
- No emojis as icons — use SVG paths
- Set `layer-name="Semantic Name"` on key elements
- Google Fonts available via `font-family: "Font Name"`
- Font sizes MUST use `px` units
- Use `border-box` sizing assumptions

### Modifying Existing Designs

```bash
# Update styles on nodes
exec {baseDir}/paper.sh update_styles '{"updates":[{"nodeIds":["ID1","ID2"],"styles":{"backgroundColor":"#FF0000","padding":"20px"}}]}'

# Change text content
exec {baseDir}/paper.sh set_text_content '{"updates":[{"nodeId":"TEXT_ID","textContent":"New text here"}]}'

# Duplicate nodes (efficient for repeated elements)
exec {baseDir}/paper.sh duplicate_nodes '{"nodes":[{"id":"SOURCE_ID"}]}'
# With specific parent:
exec {baseDir}/paper.sh duplicate_nodes '{"nodes":[{"id":"SOURCE_ID","parentId":"TARGET_PARENT"}]}'

# Delete nodes
exec {baseDir}/paper.sh delete_nodes '{"nodeIds":["ID1","ID2"]}'

# Rename layers
exec {baseDir}/paper.sh rename_nodes '{"updates":[{"nodeId":"ID","name":"Header"}]}'
```

### Finishing Up

```bash
# ALWAYS call when done with an artboard — releases the working indicator
exec {baseDir}/paper.sh finish_working_on_nodes
```

## Design Workflow (Mandatory)

1. **Start** — `get_basic_info` to see what's on the canvas
2. **Check fonts** — `get_font_family_info` before writing any typography
3. **Design brief** — Before writing HTML, decide: color palette (5-6 hex), type choices, spacing rhythm, visual direction
4. **Build incrementally** — ONE visual group per `write_html` call (header, row, button group — not an entire screen)
5. **Review every 2-3 changes** — `get_screenshot` → `image` → critique spacing, typography, contrast, alignment, clipping
6. **Fix issues** before moving on
7. **Finish** — `finish_working_on_nodes` when done

## Review Checkpoints (every 2-3 modifications)

After a screenshot, evaluate:
- **Spacing** — Uneven gaps? Cramped? Clear rhythm?
- **Typography** — Readable? Strong hierarchy?
- **Contrast** — Low contrast text? Elements blending?
- **Alignment** — Consistent vertical/horizontal lanes?
- **Clipping** — Content cut off at edges?

## Default Artboard Sizes

| Device | Width | Height |
|--------|-------|--------|
| Mobile (iPhone) | 390px | 844px |
| Tablet (iPad) | 768px | 1024px |
| Desktop | 1440px | 900px |

## Troubleshooting

- **"Paper is not running"** — Open the Paper app on macOS first
- **"Failed to initialize MCP session"** — Paper needs a design file open (not just the app)
- **Empty response** — The node ID may be wrong; use `get_basic_info` to find valid IDs
- **Session expired** — The script auto-retries with a fresh session; if persistent, delete `/tmp/paper-mcp-session`
