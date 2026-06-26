---
name: leaferjs
description: LeaferJS — Canvas 2D Engine. Lightweight and high-performance Canvas 2D graphics engine, supporting multiple platforms such as Web, Worker, Node.js, and Mini Programs.
---

# LeaferJS — Canvas 2D Engine

## Use Cases

Suitable for UI rendering, graphic editing, data visualization, game development, and other scenarios.

## Quick Start

```bash
npm install leafer-ui                         # ~70KB min+gzip
npm install leafer                             # 98KB + all plugins
npm install @leafer-ui/worker                  # Web Worker
npm install @leafer-ui/node skia-canvas        # Node.js
npm install @leafer-ui/miniapp                 # Mini-program (≥v3.6.0)
```

CDN: `<script src="https://unpkg.com/leafer-ui@2.1.2/dist/web.min.js"></script>`
(Global variable `LeaferUI`, Image/PointerEvent aliases `MyImage/MyPointerEvent`)

```ts
import { Leafer, Rect } from 'leafer-ui'
const leafer = new Leafer({ view: window })
leafer.add(new Rect({ x: 100, y: 100, width: 100, height: 100, fill: '#32cd79' }))
```

## Reference Index

| File | Coverage |
|------|----------|
| references/quick-start.md | Engine creation / configuration / viewport / framework integration (Vue/React/Nuxt/Next/SSR) |
| references/elements.md | All graphic elements + styles + export + remove/destroy + performance + animation |
| references/groups.md | Group/Box/Frame/App layers, editor |
| references/events.md | Events / PointerEvent / lifecycle / debugging / engine config |
| references/install.md | Multi-platform installation + FAQ + version management |