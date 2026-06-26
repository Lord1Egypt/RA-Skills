---
name: lark-cli-devhub-whiteboard
description: Use when creating or updating Feishu/Lark Whiteboards through lark-cli or feishu-cli for a development knowledge hub, including architecture maps, bug investigation paths, task maps, dependency maps, and project knowledge graphs.
metadata:
  requires:
    bins: ["lark-cli", "npx"]
---

# Lark CLI Dev Hub Whiteboard

Whiteboard is for human scanning and relationship maps. It is not the only AI-readable source of truth.

Discovery aliases: `feishu-cli whiteboard`, `飞书画板`, `lark-cli whiteboard`, `Lark Whiteboard`, `architecture diagram`, `knowledge graph`.

## Good Uses

- Architecture map with 3-7 zones.
- Bug diagnosis path.
- Release flow.
- Task dependency map.
- Project knowledge graph overview.
- Decision impact map.

## Required Pairing

Every durable Whiteboard should have a Base `Artifacts` record with:

- `Title`
- `Project`
- `Area`
- `Artifact Type = Whiteboard`
- `Source URL`
- `Summary`
- `AI Summary`
- `Search Keywords`

This lets future agents discover the map without needing to visually inspect it first.

## Rendering Rules

- Mermaid is good for simple flows, timelines, sequence diagrams, and mind maps.
- SVG or DSL is better for dense architecture and knowledge maps.
- Keep line count low. Prefer grouping and adjacency over all-to-all edges.
- Validate locally before writing to Feishu when possible.

## CLI Pattern

```bash
npx -y @larksuite/whiteboard-cli@^0.2.11 \
  -i diagram.mmd -o diagram.png -f mermaid

npx -y @larksuite/whiteboard-cli@^0.2.11 \
  -i diagram.mmd --to openapi --format json \
  | lark-cli whiteboard +update \
      --whiteboard-token "$WHITEBOARD_TOKEN" \
      --source - --input_format raw \
      --idempotent-token "$(date +%s)-devhub" \
      --overwrite --dry-run --as user
```

After a meaningful redraw, query or export the remote board once to confirm the write landed.

When official `lark-whiteboard` skill is installed, use it for exact query/update workflows.
