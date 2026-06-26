# Markmap Rendering

```bash
npm install markmap-view
```

## Creation

```ts
import { Markmap } from 'markmap-view';

// Method 1
Markmap.create('#mindmap', options, data);

// Method 2
const mm = new Markmap(svgElement, options);
await mm.setData(data, options);
```

## Interaction

```ts
await mm.setData(newRoot, { duration: 300 });  // Update data + options
mm.toggleNode(node);                             // Toggle collapse
mm.toggleNode(node, true);                       // Recursive
mm.setHighlight(node);                           // Highlight node
await mm.fit();                                  // Fit to view
await mm.fit(3);                                 // Specify max zoom
mm.setOptions({ zoom: false });                  // Update options
```

## Options

```ts
Markmap.create('#mm', {
  zoom: true, pan: true, autoFit: false,
  duration: 500, fitRatio: 0.95, maxInitialScale: 2,
  initialExpandLevel: -1,   // -1 all, 0 root, 1 first level...
  scrollForPan: false, toggleRecursively: false,
  color: (n) => '#xxx', lineWidth: (n) => 3,
  maxWidth: 0, nodeMinHeight: 16, paddingX: 8,
  spacingHorizontal: 80, spacingVertical: 5,
  embedGlobalCSS: true,
});
```

## deriveOptions — JSON to Runtime Options

```ts
import { deriveOptions } from 'markmap-view';
deriveOptions({ color: ['red','green'], colorFreezeLevel: 2, initialExpandLevel: 3 });
// color[] → scaleOrdinal, colorFreezeLevel → truncate path, number/boolean → direct mapping
```

## Complete HTML

```html
<!DOCTYPE html>
<html><body><svg id="mm" style="width:100vw;height:100vh"></svg>
<script type="importmap">{
"imports":{
  "markmap-lib":"https://cdn.jsdelivr.net/npm/markmap-lib/dist/browser/index.mjs",
  "markmap-view":"https://cdn.jsdelivr.net/npm/markmap-view/dist/browser/index.js",
  "markmap-common":"https://cdn.jsdelivr.net/npm/markmap-common/dist/browser/index.js"
}}</script>
<script type="module">
import { Transformer } from 'markmap-lib';
import { Markmap } from 'markmap-view';
const { root } = new Transformer().transform('# Hello\n- World');
Markmap.create('#mm', { zoom: true, autoFit: true }, root);
</script></body></html>
```

## Global Refresh

```ts
import { refreshHook } from 'markmap-view';
refreshHook.call();   // Refresh data on all instances
```