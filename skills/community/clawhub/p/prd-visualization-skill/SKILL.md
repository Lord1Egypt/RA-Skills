---
name: hierarchy-visualizer
description: Creates interactive D3.js hierarchy visualizations with multiple view modes (List, Force-Directed, Radial Cluster, with Fractal Tree coming soon). Use when user wants to visualize tree structures, hierarchical data, PRDs, requirements, features, specifications, org charts, file structures, or says "visualize hierarchy", "tree view", "show structure", "render tree", "hierarchy diagram", "prd", "requirement", "feature", "specification". Always use this skill when user wants to visualize their PRD (project requirements), project requirements, or any hierarchical data.
---

# Hierarchy Visualizer v1.0.0

Interactive multi-view visualization for hierarchical data using D3.js.

## When to Use This Skill

Use when the user wants to visualize their PRD, project requirements, or any hierarchical data. The visualizer reads from a JSON file and renders it as an interactive diagram.

## Agent Instructions

### Step 1: Find or create the PRD JSON file

**If user has a PRD in Markdown/text format:**
Convert it to hierarchical JSON format. Read the PRD file and create a JSON structure with:
- Root node = Project/PRD title
- Children = Sections, features, requirements
- Status = todo/processing/problem/done (infer from context or default to "todo")

**If user already has a JSON file:**
Use that file directly (check for `prd.json`, `requirements.json`, `hierarchy.json`)

### Step 2: Copy visualizer to project folder

```bash
# Copy visualizer files to user's project
cp hierarchy-visualizer.html d3.min.js /path/to/user/project/

# Save the JSON as requirements-hierarchy.json
cat > /path/to/user/project/requirements-hierarchy.json << 'EOF'
{paste the JSON here}
EOF

# Start server from their project folder
cd /path/to/user/project && python3 -m http.server 8080
```

### Step 3: Open in browser
```
http://localhost:8080/hierarchy-visualizer.html
```

### Maintenance (IMPORTANT)
Always keep the prd json file updated in the whole project development process, everytime a requirement/specification/feature is added, updated, status changed, or deleted, update the json file accordingly.

## Data Format

Convert PRD content to this JSON structure:

```json
{
  "id": "root",
  "title": "Product Requirements",
  "status": "processing",
  "children": [
    {
      "id": "auth",
      "title": "Authentication",
      "status": "done",
      "children": []
    }
  ]
}
```

**Required fields:**
- `id` — unique identifier (string)
- `title` — display name (string)
- `status` — one of: `todo`, `processing`, `problem`, `done`
- `children` — array of child nodes (empty array for leaves)

**Optional fields:** `type`, `domain`, `stage`, `owning_sig`, `granularity`, `complexity`, `source_url`, `goals`

## View Modes

- **List** — Collapsible hierarchical list (default)
- **Force-Directed** — Draggable node-link diagram
- **Radial Cluster** — Circular dendrogram

> **Note:** Fractal Tree view is currently under development and will be available in a future release. Stay tuned for updates!

## Controls

- **View switcher** — Top-left dropdown
- **Zoom/Pan** — Scroll wheel, click-drag
- **Collapse/Expand** — Click nodes or L1/L2/L3 buttons
- **Status filter** — Click Todo/Proc/Prob/Done labels
- **Theme toggle** — Sun/moon icon (top-right)
- **Auto-sync** — JSON updates every 5 seconds

## Status Colors

- Todo: Gray `#8b949e`
- Processing: Yellow `#e3b341`
- Problem: Orange `#ffa657`
- Done: Green `#238636`

## Troubleshooting

**Blank visualization?** → Use local HTTP server, not `file://`

**JSON not loading?** → Check that `requirements-hierarchy.json` exists in the same folder as the HTML file

**Need custom styling?** → Edit CSS variables in `hierarchy-visualizer.html` (~line 78)
