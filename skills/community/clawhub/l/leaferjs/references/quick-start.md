# Leafer Engine, Viewport & Framework Integration

## Creating an Engine

```ts
// view: window|div|canvas|id string (without #)
new Leafer({ view: window })                          // Full-screen responsive
new Leafer({ view: window, left: 100 })               // Left margin
new Leafer({ view: window, width: 600, height: 600 }) // Fixed dimensions
new Leafer({ view: window, grow: true })               // Auto-fit content
```

## Configuration

```ts
{ start: true, maxFPS: 60, usePartRender: true, usePartLayout: true,
  mobile: false, cursor: true, keyEvent: true,
  pointSnap: false, pixelSnap: false }
```

| Category | Description |
|----------|-------------|
| type | block(default)/viewport/design(0.01~256)/document(≥1)/custom |
| pointer | tapMore: false, preventDefaultMenu: boolean |
| zoom | min/max zoom range |
| move | holdSpaceKey, holdMiddleKey, scroll('limit') |

## Viewport Types

```ts
import '@leafer-in/viewport' // required
new Leafer({ type: 'design' })
```

| Type | Operations | Range | Use Case |
|------|------------|-------|----------|
| block | No viewport interaction | — | General |
| viewport | Scrollwheel pan + Ctrl zoom | Unlimited | General purpose |
| design | + Middle-click/Space drag | 0.01~256 | Editing |
| document | Constrained content area | ≥1 | Documents |

Manual: `leafer.zoomLayer.move(x,y)` / `leafer.zoomLayer.scaleOfWorld(center, scale)`

## Creating Elements

```ts
new Rect({ x:100, y:100, width:100, height:100, fill:'#32cd79' })  // Standard
Rect.one({ fill:'#32cd79' }, 100, 100)                             // Concise
leafer.add({ tag:'Rect', x:100, width:100, fill:'#32cd79' })       // tag
leafer.add(json)  // JSON import
```

## Framework Integration

**Vue 3 (onMounted):** `new Leafer({ view: 'leafer-view' })` + `<div id="leafer-view">`

**React (useEffect):** Create + `return () => leafer.destroy()`

**Nuxt (async mounted):** `const { Leafer } = await import('leafer-ui')`

**Next (use client):** `import('leafer-ui')` inside `useEffect` + cleanup destroy

SSR rule: Always async import inside mounted/useEffect to ensure Canvas environment exists