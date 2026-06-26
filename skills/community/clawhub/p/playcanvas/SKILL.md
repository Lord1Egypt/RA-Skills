---
name: playcanvas
description: Comprehensive guide for PlayCanvas, the web-first 3D graphics platform including the Engine API, Editor, React wrapper, and Web Components. Use when building 3D web applications, games, or interactive experiences with PlayCanvas. 
---

# PlayCanvas

PlayCanvas is an open-source, web-first 3D graphics platform with an MIT-licensed JavaScript engine, a real-time collaborative Editor, a React wrapper, and Web Components.

## Covers

- Engine API and standalone usage
- Editor visual development
- PlayCanvas React declarative components
- Web Components HTML-based 3D
- Scripting and ECS architecture
- Graphics, materials, shaders
- Physics simulation
- Animation system
- Asset pipeline
- 2D and UI systems
- Performance optimization
- Publishing to web/mobile/desktop
- Gaussian Splatting
- PCUI framework

## Reference Files (30 files)

Docs in `references/` — load on demand:

| File | Covers |
|------|--------|
| `getting-started` | Overview, community, OSS |
| `editor` | Overview + press |
| `editor-interface` | Toolbar, Hierarchy, Inspector, Viewport, Launch, Settings |
| `editor-assets` | Assets panel | Panel, import pipeline, inspectors, store | pipeline |
| `editor-scenes` | Scenes, entities, components, templates/prefabs |
| `editor-scripting` | Editor scripting tools |
| `editor-publishing-web` | Web, mobile, ads |
| `editor-version-control` | Branches, checkpoints, merging |
| `editor-realtime-collaboration` | Collaboration |
| `editor-editor-api` | Editor extension API |
| `editor-engine-compatibility` | V1 vs V2 |
| `editor-faq` | FAQ |
| `editor-troubleshooting` | Brightness/darkness fixes |
| `editor-getting-started` | Tutorial |
| `engine-standalone` | Engine API, standalone, Node.js, migrations, browser support |
| `graphics` | Cameras, lighting, materials, shaders, particles, layers, batching |
| `physics` | Rigid body, collision, compound shapes, ammo.js API |
| `animation` | Anim component, state graphs, events, layer masking |
| `scripting` | ESM/Classic, lifecycle, attributes, events, debugging, migration |
| `ecs` | Entity-Component-System |
| `react` | React installation, scenes, assets, materials, physics, interactivity |
| `web-components` | HTML tags, installation, tag reference |
| `2D` | Sprites, 9-slicing, sprite editor, texture packing |
| `user-interface` | Screen/Element components, localization |
| `assets` | Asset registry, loading, preloading, formats |
| `optimization` | GPU profiling, load time, texture compression, device pixel ratio |
| `api` | REST API endpoints |
| `account-management` | Organizations, billing |
| `pcui` | PCUI UI framework |
| `gaussian-splatting` | 3D Gaussian Splatting |
| `glossary` | Terminology |
| `security` | Vulnerability reporting

## Key APIs

### Core Engine
```js
import * as pc from 'playcanvas';

const app = new pc.Application(canvas);
app.start();
```

### Entity & Component
```js
const entity = new pc.Entity('myEntity');
entity.addComponent('camera', { fov: 60 });
entity.addComponent('script');
entity.script.create('myScript', { attributes: { speed: 10 } });
app.root.addChild(entity);
```

### Asset Loading
```js
app.assets.loadFromUrl('model.glb', 'container', (err, asset) => {
  const entity = asset.resource.instantiateRenderEntity();
  app.root.addChild(entity);
});
```

### Input
```js
if (app.keyboard.isPressed(pc.KEY_SPACE)) { /* jump */ }
if (app.mouse.isPressed(pc.MOUSEBUTTON_LEFT)) { /* click */ }
```

