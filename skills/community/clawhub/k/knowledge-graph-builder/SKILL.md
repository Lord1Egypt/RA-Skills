---
name: knowledge-graph-builder
version: 1.2.0
author: Milesnee
license: MIT
description: "Use when building, updating, or deploying an interactive knowledge graph from a structured knowledge vault. Scans INDEX.md + article card metadata (frame_analysis), extracts nodes + three edge types (explicit/concept/cluster), and generates a force-directed Canvas HTML graph with search, filter, and click-to-inspect. Supports custom category mappings, keyword lists, framework nodes, and manual cross-links via JSON config."
metadata:
  hermes:
    tags: [knowledge-graph, visualization, force-directed, canvas, knowledge-vault]
    related_skills: []
---

# Knowledge Graph Builder

## Overview

Transforms a structured knowledge vault into an interactive force-directed HTML graph. Scans three data layers — INDEX.md categories, article card metadata (frame_analysis blocks), and framework nodes — then builds a Canvas-based force-directed graph with 243+ nodes and 400+ edges.

**No external dependencies.** Pure Python 3.9+ stdlib. Output is a single self-contained HTML file (no CDN, no JS frameworks).

## When to Use

- User asks to "generate knowledge graph", "visualize connections", "update graph"
- After archiving new articles — rebuild the graph to include them
- User wants to see cross-domain relationships in their knowledge base
- Deploying the graph for online viewing (built-in HTTP server option)

**Don't use for:** Simple file listing, article reading, or single-article analysis (use `search_files` instead).

## Quick Start

```bash
# Default: scan current directory as vault root
python3 scripts/build_graph.py

# Custom vault path
python3 scripts/build_graph.py --vault /path/to/knowledge-vault

# Custom output + title
python3 scripts/build_graph.py --vault ~/my-vault --output ~/graph.html --title "My Knowledge"

# Dry-run (stats only, no HTML)
python3 scripts/build_graph.py --dry-run

# Custom config (category colors, keywords, framework nodes, manual links)
python3 scripts/build_graph.py --config my-config.json
```

## Vault Structure Expected

```
vault/
├── references/INDEX.md          # Category index (## headings with tables)
├── 03-sources/article-cards/    # *.md files with optional frame_analysis blocks
└── knowledge-graph-full.html    # Output (generated)
```

### INDEX.md Format

```markdown
## 🤖 AI Agent & 估值 (42篇)
| [file-slug](path/to/file.md) | 2026-07-25 | Brief summary text |
...

## 📚 书镜 & 认知 (31篇)
| [book-mirror-1](path) | 2026-01-15 | Summary |
...
```

### Article Card frame_analysis (optional, in article-cards/*.md)

```yaml
frame_analysis:
  layer: "L3"
  category: "宏观/地缘"
  core_insight: "Japan dependency loop + anti-hegemony instinct"
  concepts:
    - "地缘平衡"
    - "威慑=不用"
```

## Edge Types

| Type | Color | Width | Source | Description |
|------|-------|-------|--------|-------------|
| `explicit` | `#ef4444` red | 2.5px | MANUAL list in config | Hand-curated cross-domain links — the graph skeleton |
| `concept` | `#3b82f6` blue | 1.5px | Keyword co-occurrence | Auto-computed from 50+ keywords; ≤8 per keyword = full mesh, >8 = hub-spoke |
| `cluster` | `#2a2a35` dark | 0.8px | Same-category MST chain | Links items within a category in a chain to avoid O(n²) explosion |

## Configuration (JSON)

See `templates/config.example.json` for full template. Override any subset:

```json
{
  "cat_meta": {
    "🤖": {"layer": "L3", "color": "#f59e0b", "label": "AI Agent"}
  },
  "keywords": ["AI", "macro", "cognition", "data"],
  "framework_nodes": [
    {
      "id": "FW-1", "label": "My Framework", "layer": "L1",
      "color": "#6366f1", "category": "核心框架", "cat_label": "Core",
      "insight": "Key insight here", "concepts": ["concept-a"],
      "source": "MEMORY.md", "isFramework": true
    }
  ],
  "manual_links": [
    ["article-slug", "FW-1", "relationship label"]
  ]
}
```

**Adding explicit links:** When archiving a new article that relates to existing entries (complementary / contrasting / extending), add a tuple to `manual_links`. The script fuzzy-matches slugs against node IDs.

## Execution Steps

### Step 1: Update the index (if new articles archived)

```bash
# Run your vault's index generator first (vault-specific)
# For the default vault: cd /root/.openclaw/workspace && python3 scripts/memory/gen_references_index.py
```

**Completion criterion:** INDEX.md shows 0 uncategorized entries.

### Step 2: Build the graph

```bash
python3 ~/.hermes/skills/productivity/knowledge-graph-builder/scripts/build_graph.py --vault <vault-path>
```

**Completion criterion:** stdout shows node/edge counts with 0 errors.

### Step 3: Verify output

```python
import json, re
with open("knowledge-graph-full.html") as f:
    content = f.read()
m = re.search(r'const GRAPH=(.+?);', content)
g = json.loads(m.group(1))
print(f'Nodes: {len(g["nodes"])}, Edges: {len(g["edges"])}')
from collections import Counter
print('Layers:', dict(Counter(n["layer"] for n in g["nodes"])))
explicit = [e for e in g["edges"] if e["type"] == "explicit"]
print(f'Explicit edges: {len(explicit)}')
for e in explicit:
    s = next(n["label"] for n in g["nodes"] if n["id"] == e["source"])
    t = next(n["label"] for n in g["nodes"] if n["id"] == e["target"])
    print(f'  {s[:25]} → {t[:25]} | {e["label"]}')
```

**Completion criterion:** Node count > 0, explicit edges > 0, HTML file opens in browser.

### Step 4: Deploy for online viewing (optional)

```bash
cd <vault-path> && python3 -m http.server 8848 --bind 0.0.0.0
```

Use `background=true` in Hermes terminal for long-running server. Ensure firewall allows the port.

## HTML Features

- **Canvas 2D force-directed layout** — handles 250+ nodes smoothly
- **Category clustering** — nodes initialize in sector positions by category
- **Framework nodes** — glow + inner ring + always-visible label
- **Interaction:** search filter, layer toggles (L1/L2/L3), edge-type filters, click-for-details sidebar
- **Edge highlighting** — hover a node to highlight all its connections
- **Self-contained** — no CDN, no external JS, works offline

## Common Pitfalls

1. **Article-cards coverage gap.** `INDEX.md` only tracks `references/*.md` and `book-mirrors/*.md`, but articles with `frame_analysis` may only exist in `03-sources/article-cards/`. The script's Phase 2 adds these orphans — **do not remove this logic** or you lose your newest entries.

2. **Port conflict on HTTP deploy.** `OSError: Address already in use` means a zombie process holds the port. Kill it (`fuser -k <port>/tcp`) or use a different port.

3. **Firewall blocking external access.** Cloud servers need explicit `ufw allow <port>/tcp`. Check with `ss -tlnp | grep <port>`.

4. **f-string brace escaping.** The HTML template contains JS with `{` and `}`. The script uses raw strings + `.replace()` placeholders (`__TITLE__`, `__LEGEND__`, `__GRAPH_JSON__`) to avoid f-string brace hell. If editing the template, keep this pattern.

5. **Manual link fuzzy matching.** The MANUAL list matches patterns against node IDs with `in` (substring). Short patterns like `"AI"` will match too many nodes. Use specific substrings (≥8 chars recommended).

6. **Concept edge explosion.** Popular keywords (e.g. "AI") match 50+ nodes. The script limits to hub-spoke (8 connections) for keywords with >8 matches. If the graph is too dense, trim your keyword list.

## Verification Checklist

- [ ] Script runs with 0 errors (`--dry-run` first)
- [ ] Node count matches expectation (INDEX entries + article-cards extras + framework nodes)
- [ ] Explicit edges > 0 (MANUAL list matched successfully)
- [ ] HTML file opens in browser (force-directed layout renders)
- [ ] Click a node → sidebar shows connections
- [ ] Search filter works
- [ ] Layer toggle buttons filter correctly
