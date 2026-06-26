# Web Components

## Components
PlayCanvas Web Components are a powerful set of custom HTML elements that make it incredibly easy to embed interactive 3D content directly into your web pages. Built on modern web standards, these components bridge the gap between traditional web development and 3D graphics, allowing you to create immersive experiences with simple HTML markup.
## What Are Web Components?
Web Components are reusable custom HTML elements that encapsulate complex functionality behind a simple, declarative interface. PlayCanvas Web Components wrap the full power of the PlayCanvas Engine in easy-to-use HTML tags, making 3D development accessible to web developers of all skill levels.
```html
<!-- Create a 3D scene with just HTML -->
<pc-app>
  <pc-scene>
    <pc-entity name="camera" position="0 0 3">
      <pc-camera></pc-camera>
    </pc-entity>
    <pc-entity name="light" rotation="45 45 0">
      <pc-light></pc-light>
    </pc-entity>
    <pc-entity name="ball">
      <pc-render type="sphere"></pc-render>
    </pc-entity>
  </pc-scene>
</pc-app>
```
### Zero JavaScript Required
Create interactive 3D scenes using only HTML markup - no complex JavaScript setup or engine initialization needed.
### Highly Customizable
Full access to PlayCanvas Engine features through intuitive HTML attributes.
### Performance Optimized
Leverages the same high-performance PlayCanvas Engine used by thousands of web applications.
## Browser Support
PlayCanvas Web Components work in all modern browsers that support:
- WebGL 2.0 and/or WebGPU
- ES6 Modules
- Custom Elements v1
## Open Source & MIT Licensed
The Web Components are completely open source and available on GitHub under the MIT license.
## Components Getting Started
Before you begin, make sure you have [Node.js](https://nodejs.org/) 18 or later installed.
## Installing from NPM
```bash
npm install playcanvas @playcanvas/web-components --save-dev
```
In your HTML, add an import map so the Web Components can find the PlayCanvas Engine:
```html
<script type="importmap">
{
  "imports": {
    "playcanvas": "/node_modules/playcanvas/build/playcanvas.mjs"
  }
}
</script>
<script type="module" src="/node_modules/@playcanvas/web-components/dist/pwc.mjs"></script>
```
## Using a CDN
```html
<script type="importmap">
{
  "imports": {
    "playcanvas": "https://cdn.jsdelivr.net/npm/playcanvas@latest/build/playcanvas.mjs"
  }
}
</script>
<script type="module" src="https://cdn.jsdelivr.net/npm/@playcanvas/web-components@latest/dist/pwc.mjs"></script>
```
## Boilerplate HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>My PlayCanvas Web Components App</title>
  <script type="importmap">
    { "imports": { "playcanvas": "https://cdn.jsdelivr.net/npm/playcanvas@latest/build/playcanvas.mjs" } }
  </script>
  <script type="module" src="https://cdn.jsdelivr.net/npm/@playcanvas/web-components@latest/dist/pwc.mjs"></script>
  <style>
    body { margin: 0; overflow: hidden; }
  </style>
</head>
<body>
  <!-- Your PlayCanvas Web Components elements go here -->
</body>
</html>
```
## Components Tags
All available PlayCanvas Web Components custom HTML elements:
| Tag | Description |
|-----|-------------|
| `<pc-app>` | Root element of your application |
| `<pc-asset>` | Defines an asset to be loaded |
| `<pc-camera>` | Camera used to render the scene |
| `<pc-collision>` | Collision component for triggers and rigid bodies |
| `<pc-element>` | Text, image or group UI element |
| `<pc-entity>` | Defines an entity (container) |
| `<pc-light>` | Light component |
| `<pc-listener>` | Audio listener component |
| `<pc-module>` | WebAssembly module |
| `<pc-particles>` | Particle system component |
| `<pc-render>` | Render component (primitives or assets) |
| `<pc-rigidbody>` | Rigidbody physics component |
| `<pc-scene>` | Defines a scene |
| `<pc-script>` | Single script assigned to a script component |
| `<pc-scripts>` | Script component (container for scripts) |
| `<pc-sky>` | Image-based skybox |
| `<pc-screen>` | Screen component for UI rendering |
| `<pc-sound>` | Single sound assigned to a sound component |
| `<pc-sounds>` | Sound component (container for sounds) |
| `<pc-splat>` | Renders 3D Gaussian Splats |
