# Obsidian Canvas (JSON Canvas) Reference

Canvas files (`.canvas`) follow the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

---

## File Structure

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes`: Array of node objects (optional)
- `edges`: Array of edge objects connecting nodes (optional)

---

## Common Workflows

### Create a New Canvas

1. Create a `.canvas` file with `{"nodes": [], "edges": []}`.
2. Generate unique 16-character hex IDs for each node (e.g., `"6f0ad84f44ce9c17"`).
3. Add nodes with required fields: `id`, `type`, `x`, `y`, `width`, `height`.
4. Add edges referencing valid node IDs via `fromNode` and `toNode`.
5. **Validate**: Parse JSON; verify all `fromNode`/`toNode` values exist in nodes.

### Add a Node

1. Read and parse the existing `.canvas` file.
2. Generate a unique ID that does not collide with existing IDs.
3. Choose `x`, `y` to avoid overlapping (leave 50–100px spacing).
4. Append the node object to `nodes`.

---

## Node Types

### Generic Attributes

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique 16-char hex ID |
| `type` | Yes | string | `text`, `file`, `link`, or `group` |
| `x` | Yes | integer | X position (top-left corner) |
| `y` | Yes | integer | Y position (top-left corner) |
| `width` | Yes | integer | Width in pixels |
| `height` | Yes | integer | Height in pixels |
| `color` | No | canvasColor | Preset `"1"`–`"6"` or hex `"#FF0000"` |

### Text Node

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0, "y": 0, "width": 400, "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

Use `\n` for line breaks in JSON strings. Do **not** use `\\n`.

### File Node

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500, "y": 0, "width": 400, "height": 300,
  "file": "Attachments/diagram.png"
}
```

### Link Node

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000, "y": 0, "width": 400, "height": 200,
  "url": "https://obsidian.md"
}
```

### Group Node

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50, "y": -50, "width": 1000, "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

Groups are visual containers. Position child nodes inside the group's bounds.

---

## Edges

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "toNode": "a1b2c3d4e5f67890",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "leads to"
}
```

| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Unique identifier |
| `fromNode` | Yes | Source node ID |
| `toNode` | Yes | Target node ID |
| `fromSide` / `toSide` | No | `top`, `right`, `bottom`, `left` |
| `fromEnd` / `toEnd` | No | `none` or `arrow` (default `toEnd = "arrow"`) |
| `color` | No | Line color |
| `label` | No | Text label |

---

## Colors

| Preset | Color  |
|--------|--------|
| `"1"` | Red    |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green  |
| `"5"` | Cyan   |
| `"6"` | Purple |

---

## Layout Guidelines

- Coordinates can be negative (canvas extends infinitely).
- `x` increases right, `y` increases down.
- Space nodes 50–100px apart; leave 20–50px padding inside groups.
- Align to grid multiples of 10 or 20.

---

## Validation Checklist

1. All `id` values are unique across nodes and edges.
2. Every `fromNode`/`toNode` references an existing node ID.
3. Required type-specific fields present (`text`, `file`, or `url`).
4. `type` is one of: `text`, `file`, `link`, `group`.
5. `fromSide`/`toSide` is one of: `top`, `right`, `bottom`, `left`.
6. JSON is valid and parseable.
