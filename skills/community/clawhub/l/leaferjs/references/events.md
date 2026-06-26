# Events & Debugging

## Listening

```ts
rect.on(PointerEvent.ENTER, fn)    // Listen
rect.on('pointer.enter', fn)       // String-based naming
rect.on_(type, fn, bind)           // With bind (returns event id)
rect.once(type, fn)                // One-time
rect.off('pointer.enter', fn)      // Remove
rect.emit('pointer.enter', data)   // Dispatch
```

## Common Events

| Event | Name | Description |
|-------|------|-------------|
| PointerEvent | pointer.* | DOWN/MOVE/UP/OVER/OUT/ENTER/LEAVE/TAP/DOUBLE_TAP/LONG_PRESS/LONG_TAP/CLICK/MENU |
| DragEvent | drag.* | Drag |
| DropEvent | drop.* | Drop |
| MoveEvent | move.* | Viewport pan |
| ZoomEvent | zoom.* | Viewport zoom |
| KeyEvent | key.* | Keyboard |
| ChildEvent | child.* | Child element add/remove |
| PropertyEvent | property.* | Property change |
| LeaferEvent | leaf.* | Engine lifecycle (READY/VIEW_READY/UPDATE_MODE) |
| RenderEvent | render.* | Rendering (BEFORE/END) |

## PointerEvent Features

- Multiple click types (tap/double_tap/long_press) only trigger the most specific match by default (`tapMore:true` triggers all)
- Event pairing: `down` guarantees a subsequent `up`
- Properties: `x`(world), `y`, `pointerType(mouse/pen/touch)`, `pressure(0~1)`, `left/middle/right/spaceKey`

Coordinate conversion: `getPagePoint()`, `getBoxPoint(relative?)`, `getInnerPoint(relative?)`

## Lifecycle

Element: `created` → `mounted` → `unmounted` (via event object or `on` listener)
Engine: `LeaferEvent.READY`(layout done) → `VIEW_READY`(first render done) → `UPDATE_MODE`

## Interaction Properties

| Property | Description |
|----------|-------------|
| hittable | pointer-events |
| hitFill | fill area (pixel = PNG pixel-level precision) |
| draggable | Allow dragging |
| editable | Allow editing (requires editor plugin) |
| cursor | CSS cursor name |

## Debugging

```ts
import { Debug } from 'leafer-ui'
Debug.enable = true
Debug.filter = 'RunTime'       // Print specific type
Debug.showRepaint = true       // Show repaint regions
```