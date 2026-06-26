# ProseMirror Block & Mark Reference

Documents are made of blocks. Each block is ProseMirror JSON with a `type`, optional `attrs`, and optional `content` (array of child nodes).

## Block Types

### Paragraph
```json
{ "type": "paragraph", "content": [{ "type": "text", "text": "Hello world" }] }
```

### Heading (levels 1-6)
```json
{ "type": "heading", "attrs": { "level": 2 }, "content": [{ "type": "text", "text": "Section Title" }] }
```

### Bullet List
```json
{ "type": "bulletList", "content": [
  { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "First" }] }] },
  { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Second" }] }] }
] }
```

### Ordered List
```json
{ "type": "orderedList", "content": [
  { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Step one" }] }] },
  { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Step two" }] }] }
] }
```

### Task List
```json
{ "type": "taskList", "content": [
  { "type": "taskItem", "attrs": { "checked": false }, "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Todo" }] }] },
  { "type": "taskItem", "attrs": { "checked": true }, "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Done" }] }] }
] }
```

### Blockquote
```json
{ "type": "blockquote", "content": [
  { "type": "paragraph", "content": [{ "type": "text", "text": "A quote." }] }
] }
```

### Code Block
```json
{ "type": "codeBlock", "attrs": { "language": "python" }, "content": [{ "type": "text", "text": "def hello():\n    print('hi')" }] }
```

### Table
```json
{ "type": "table", "content": [
  { "type": "tableRow", "content": [
    { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Name" }] }] },
    { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Role" }] }] }
  ] },
  { "type": "tableRow", "content": [
    { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Alice" }] }] },
    { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Engineer" }] }] }
  ] }
] }
```

### Callout (variants: info, warning, error, success)
```json
{ "type": "callout", "attrs": { "variant": "warning", "emoji": "Warning" }, "content": [{ "type": "text", "text": "Be careful!" }] }
```

### Toggle (collapsible)
```json
{ "type": "toggle", "attrs": { "summary": "Click to expand", "open": false }, "content": [
  { "type": "paragraph", "content": [{ "type": "text", "text": "Hidden content." }] }
] }
```

### Image
```json
{ "type": "image", "attrs": { "src": "https://example.com/photo.jpg", "alt": "Description" } }
```

### Horizontal Rule
```json
{ "type": "horizontalRule" }
```

## Mark Types (Inline Formatting)

Marks are applied to text nodes via the `marks` array.

### Bold
```json
{ "type": "text", "text": "bold", "marks": [{ "type": "bold" }] }
```

### Italic
```json
{ "type": "text", "text": "italic", "marks": [{ "type": "italic" }] }
```

### Strikethrough
```json
{ "type": "text", "text": "removed", "marks": [{ "type": "strike" }] }
```

### Inline Code
```json
{ "type": "text", "text": "const x = 1", "marks": [{ "type": "code" }] }
```

### Underline
```json
{ "type": "text", "text": "underlined", "marks": [{ "type": "underline" }] }
```

### Link
```json
{ "type": "text", "text": "click here", "marks": [{ "type": "link", "attrs": { "href": "https://example.com" } }] }
```

### Highlight
```json
{ "type": "text", "text": "highlighted", "marks": [{ "type": "highlight", "attrs": { "color": "#fef08a" } }] }
```

### Text Color
```json
{ "type": "text", "text": "red text", "marks": [{ "type": "textStyle", "attrs": { "color": "#ef4444" } }] }
```

### Multiple Marks (composable)
```json
{ "type": "text", "text": "important", "marks": [{ "type": "bold" }, { "type": "italic" }] }
```

## Formatting with format-by-match

Use `POST /sessions/:id/blocks/:block_id/format-by-match` to format existing text:

| Action | Body |
|--------|------|
| Bold a word | `{ "text": "important", "mark": "bold" }` |
| Italicize | `{ "text": "see above", "mark": "italic" }` |
| Add link | `{ "text": "click here", "mark": "link", "attrs": { "href": "https://example.com" } }` |
| Highlight | `{ "text": "key point", "mark": "highlight", "attrs": { "color": "#fef08a" } }` |
| Color text | `{ "text": "error", "mark": "textStyle", "attrs": { "color": "#ef4444" } }` |
| Remove mark | `{ "text": "plain now", "mark": "bold", "remove": true }` |
| 2nd occurrence | `{ "text": "item", "mark": "bold", "occurrence": 2 }` |
