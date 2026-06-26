---
name: obsidian-viz
description: Generate Obsidian-compatible visualization files (Excalidraw / Mermaid / Canvas). Supports text descriptions and image inputs, outputs editable diagrams in Obsidian or standard formats.
---

# Obsidian Viz Skill

Generate Obsidian-compatible visualization files from text descriptions or image inputs.

## Processing Flow

### Step 0 - Input Type Detection

**If user sends an image**:
1. Load `modules/image-reader.md`
2. Execute image type recognition and content extraction
3. Output structured Markdown summary
4. If image contains diagrams, proceed to Step 1
5. If image is text/screenshot only, end process

**If user provides text description**:
- Proceed directly to Step 1

### Step 1 - Tool Selection

Load `modules/chart-router.md` and select the most appropriate tool based on content type:

- **Excalidraw**: Hand-drawn style, architecture diagrams, free layout, concept maps
- **Mermaid**: Technical documentation, flowcharts, sequence diagrams, state diagrams, ER diagrams
- **Canvas**: Large knowledge networks, interactive exploration, data visualization

### Step 2 - Format Specification Loading

Load the corresponding reference file based on the selected tool:

- `mermaid` → `references/mermaid.md`
- `excalidraw` → `references/excalidraw.md`
- `canvas` → `references/canvas.md`

**Important**: Must read the corresponding reference file before generating any content.

### Step 3 - Output Format Selection

**Standard Format** (when user explicitly requests "standard format" or "excalidraw.com"):
- Mermaid → `.mmd` file
- Excalidraw → `.excalidraw` file
- Canvas → `.html` file

**Obsidian Format** (default):
- Mermaid → `.md` file (with mermaid code block)
- Excalidraw → `.md` file (with Excalidraw JSON)
- Canvas → `.canvas` file

### Step 4 - Generate File

1. Strictly follow format specifications in reference file
2. Output to `~/.openclaw/workspace/outputs/<filename>.<ext>`
3. Explain to user how to open the file in Obsidian

## Usage Instructions

### Excalidraw Files

**Obsidian Mode** (`.md`):
- Place in any vault folder
- Obsidian automatically opens in canvas mode
- Requires Excalidraw plugin

**Standard Mode** (`.excalidraw`):
- Can be opened directly at excalidraw.com
- Supports import to any Excalidraw instance

### Mermaid Files

**Obsidian Mode** (`.md`):
- Place anywhere in vault
- Renders in normal preview mode
- Obsidian supports Mermaid by default

**Standard Mode** (`.mmd`):
- Can be opened in Mermaid-compatible editors
- Natively supported by GitHub, GitLab, etc.

### Canvas Files

**Obsidian Mode** (`.canvas`):
- Place anywhere in vault
- Double-click to interact in Canvas view
- Natively supported by Obsidian

**Standard Mode** (`.html`):
- Open in browser
- Supports interactive exploration

## Chart Type Quick Reference

| Need | Recommended Tool | Chart Type |
|------|---------|---------|
| Workflow / CI-CD | Excalidraw or Mermaid | flowchart |
| API calls / Message interaction | Mermaid | sequenceDiagram |
| Organization / System hierarchy | Excalidraw | hierarchy |
| Concept divergence / Brainstorming | Canvas or Excalidraw | mindmap |
| State machine / Lifecycle | Mermaid | stateDiagram-v2 |
| Project timeline | Excalidraw | timeline |
| A vs B comparison | Excalidraw | comparison |
| Priority matrix | Excalidraw | matrix |
| Large knowledge network | Canvas | free-layout |
| Animation demo | Excalidraw | animation mode |
| Database design | Mermaid | erDiagram |
| Class diagram / Object relationships | Mermaid | classDiagram |
| Project schedule | Mermaid | gantt |

## Notes

1. **Must load reference first**: Skipping this step will produce incorrectly formatted files
2. **Chinese support**: All tools natively support Chinese, no escaping needed
3. **File path**: Output files are uniformly placed in `~/.openclaw/workspace/outputs/` directory
4. **Fallback strategy**: If primary tool fails, automatically try alternative tool
5. **Node count limit**: For more than 30 nodes, recommend user to split or use Canvas
