# Group / Box / Frame / App

## Group

No visual style. Child elements are positioned relative to the group. Supports nesting.

```ts
const group = new Group({ x: 100, y: 100 })
group.add([rect, ellipse])
leafer.add(group)
```

## Box — Container with Visual Style

Similar to HTML5 DIV. Supports Group functionality + Rect visual styles.

```ts
const box = new Box({ width: 100, height: 100, fill: '#FF4B4B' })
box.add(circle)
```

## Frame — Artboard

Inherits from Box, defaults to white background and clips content beyond its dimensions. Similar to an HTML page, suitable for design software.

```ts
new Frame({ width: 100, height: 100 })  // Clips child elements
```

## App — Layered Application Structure

Optional, used for scenarios requiring layered rendering (e.g., graphic editors). App can host multiple Leafer engine layers working together.

```ts
const app = new App({
  view: window, fill: '#333',
  tree: { type: 'design' },   // tree layer — main content
  sky: {}                      // sky layer — changeable layer (editor, etc.)
})
app.tree.add(contents)
app.sky.add(app.editor = new Editor())
```

### Layer Naming

| Layer | Role | Use Case |
|-------|------|----------|
| ground? | Ground layer (background) | Grid, background image (optional) |
| tree | Tree structure (main content) | Equivalent to HTML body |
| sky | Sky layer (changeable layer) | Graphic editor UI |

### Editor Quick Config

```ts
const app = new App({ view: window, editor: {} })
// Auto-creates tree layer + sky layer + app.editor instance
```

### Manual App Layer Creation

```ts
const app = new App({ view: window })
app.add(app.tree = new Leafer({ type: 'design' }))
app.add(app.sky = new Leafer())
```