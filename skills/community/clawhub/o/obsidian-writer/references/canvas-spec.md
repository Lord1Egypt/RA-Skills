# JSON Canvas Spec 1.0

Source: https://jsoncanvas.org/spec/1.0/ (2024-03-11, MIT License)
GitHub: https://github.com/obsidianmd/jsoncanvas

## Top Level

```json
{
  "nodes": [],
  "edges": []
}
```

Both arrays are optional.

## Nodes

Placed in ascending z-index order (first = bottom, last = top).

### Generic Node Attributes (all types)

| Attribute | Required | Type    | Description |
|-----------|----------|---------|-------------|
| id        | yes      | string  | Unique ID |
| type      | yes      | string  | `text`, `file`, `link`, `group` |
| x         | yes      | integer | X position in pixels |
| y         | yes      | integer | Y position in pixels |
| width     | yes      | integer | Width in pixels |
| height    | yes      | integer | Height in pixels |
| color     | no       | string  | Preset `"1"`-`"6"` or hex `"#RRGGBB"` |

### Text Node

| Attribute | Required | Type   | Description |
|-----------|----------|--------|-------------|
| text      | yes      | string | Markdown content |

### File Node

| Attribute | Required | Type   | Description |
|-----------|----------|--------|-------------|
| file      | yes      | string | Path to file within vault |
| subpath   | no       | string | Link to heading/block, starts with `#` |

### Link Node

| Attribute | Required | Type   | Description |
|-----------|----------|--------|-------------|
| url       | yes      | string | URL |

### Group Node

| Attribute       | Required | Type   | Description |
|-----------------|----------|--------|-------------|
| label           | no       | string | Text label |
| background      | no       | string | Path to background image |
| backgroundStyle | no       | string | `cover`, `ratio`, `repeat` |

Group contains nodes whose bounds intersect with it (implicit, no `children` field).

## Edges

| Attribute | Required | Type   | Description |
|-----------|----------|--------|-------------|
| id        | yes      | string | Unique ID |
| fromNode  | yes      | string | Source node id |
| fromSide  | no       | string | `top`, `right`, `bottom`, `left` |
| fromEnd   | no       | string | `none` (default), `arrow` |
| toNode    | yes      | string | Target node id |
| toSide    | no       | string | `top`, `right`, `bottom`, `left` |
| toEnd     | no       | string | `none`, `arrow` (default) |
| color     | no       | string | Preset or hex |
| label     | no       | string | Edge label text |

## Color Presets

| Value | Color  |
|-------|--------|
| "1"   | Red    |
| "2"   | Orange |
| "3"   | Yellow |
| "4"   | Green  |
| "5"   | Cyan   |
| "6"   | Purple |

Exact RGB values are implementation-defined.

## Complete Example

```json
{
  "nodes": [
    {
      "id": "intro",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 200,
      "text": "# Welcome\n\nThis is a canvas example.",
      "color": "5"
    },
    {
      "id": "ref-note",
      "type": "file",
      "x": 500,
      "y": 0,
      "width": 400,
      "height": 400,
      "file": "03-resources/example-note.md"
    },
    {
      "id": "web",
      "type": "link",
      "x": 0,
      "y": 300,
      "width": 400,
      "height": 300,
      "url": "https://jsoncanvas.org"
    },
    {
      "id": "container",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 1000,
      "height": 700,
      "label": "Overview",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "intro",
      "fromSide": "right",
      "toNode": "ref-note",
      "toSide": "left",
      "label": "see also"
    },
    {
      "id": "e2",
      "fromNode": "intro",
      "fromSide": "bottom",
      "toNode": "web",
      "toSide": "top",
      "toEnd": "arrow",
      "color": "2"
    }
  ]
}
```
