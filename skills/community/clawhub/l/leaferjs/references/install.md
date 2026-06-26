# Installation & FAQ

## Multi-Platform

| Package | Platform | Notes |
|---------|----------|-------|
| leafer-ui | web | 70KB min+gzip |
| @leafer-ui/worker | web worker | Background thread rendering |
| @leafer-ui/node | node | Server-side drawing (requires skia-canvas, 2.x only) |
| @leafer-ui/miniapp | WeChat mini-program | Base library ≥3.6.0 |

## leafer Full Bundle

`npm install leafer` — 98KB, includes leafer-ui + all @leafer-in/* plugins. Import sub-packages for smaller bundles.

## Worker Version

```js
// worker.js
importScripts('https://unpkg.com/@leafer-ui/worker@2.1.2/dist/worker.min.js')
const { Leafer, Rect } = LeaferUI
const leafer = new Leafer({ width: 800, height: 600 })
leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100))
leafer.export('jpg').then(r => self.postMessage(r.data))
```

## Node Version

```js
const { Leafer, Rect, useCanvas } = require('@leafer-ui/node')
const skia = require('skia-canvas')
useCanvas('skia', skia) // required
const leafer = new Leafer({ width: 800, height: 600 })
leafer.add(Rect.one({ fill: '#32cd79' }, 100, 100))
leafer.export('png').then(r => console.log(r.data))
```

## Mini-Program Version

```ts
import { Leafer, Rect } from '@leafer-ui/miniapp'
Page({
  onReady() { new Leafer({ view: 'leafer', eventer: this }).add(new Rect({ x:100, y:100, width:100, height:100, fill:'#32cd79' })) },
  receiveEvent() {},
})
```

Canvas wxml: `<canvas id="leafer" type="2d" catchtouchstart="receiveEvent" .../>`
iOS App structure requires additional config: `tree: { canvas: 'leafer-tree' }, sky: { canvas: 'leafer-sky' }`

## Browser Support

Chrome≥51, Firefox≥53, Safari≥10, Edge≥79. IE not supported.

## FAQ

**Version mismatch:** Main package + all plugins must match. Delete lock file and reinstall. `npm update leafer-ui @leafer-in/editor`

**SSR:** Nuxt/Next requires async `import('leafer-ui')` loading

**Reactivity:** Don't mount leafer elements to reactive data — it slows rendering

**Jank:** Parent container 100%+padding triggers constant resize; check framework reactivity binding

**Mini-program build:** Enable "JS to ES5" option. Occasional interaction failure onLoad → create with setTimeout delay

**Get version:** `import { version } from 'leafer-ui'` — current latest v2.1.2