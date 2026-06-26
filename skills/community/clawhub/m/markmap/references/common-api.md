# Type Reference & Common Utilities

## IMarkmapOptions

```ts
interface IMarkmapOptions {
  // Interaction
  zoom: boolean; pan: boolean; autoFit: boolean;
  scrollForPan: boolean; toggleRecursively: boolean;
  // Animation & Fit
  duration: number; fitRatio: number; maxInitialScale: number;
  initialExpandLevel: number; // -1 all 0 root 1 first level...
  // Color & Lines
  color: (node: INode) => string;  // default scaleOrdinal(schemeCategory10)
  lineWidth: (node: INode) => number;
  // Layout
  maxWidth: number; nodeMinHeight: number; paddingX: number;
  spacingHorizontal: number; spacingVertical: number;
  embedGlobalCSS: boolean;
  id?: string; style?: (id: string) => string;
}
```

## IMarkmapJSONOptions (serializable via frontmatter)

```ts
interface IMarkmapJSONOptions {
  colorFreezeLevel: number; duration: number;
  extraCss: string[]; extraJs: string[];
  fitRatio: number; initialExpandLevel: number; maxInitialScale: number;
  maxWidth: number; nodeMinHeight: number; paddingX: number;
  pan: boolean; zoom: boolean;
  spacingHorizontal: number; spacingVertical: number;
  lineWidth: number | number[];
}
```

**Color Freeze:** colorFreezeLevel=N → first N levels get colors assigned, deeper levels inherit. Defaults to D3 schemeCategory10.

**Line Width:** `baseWidth(1) + deltaWidth(3) / k(2) ** depth` → level 0: 4px, level 1: 2.5px...

## CSS Variables

| Variable | Default | Dark | Purpose |
|----------|---------|------|---------|
| --markmap-font | 300 16px/20px sans-serif | — | Node font |
| --markmap-text-color | #333 | #eee | Text color |
| --markmap-code-bg | #f0f0f0 | #1a1b26 | Code background |
| --markmap-code-color | #555 | #ddd | Code text color |

See source style.css for full list. Dark mode `.markmap-dark` auto-detects `prefers-color-scheme`.

## Node Types

```ts
interface IPureNode { content: string; children?: IPureNode[]; payload?: { fold?: 0|1|2; tag?: string; [k]: unknown }; }
interface INode extends IPureNode { state: { id: number; depth: number; key: string; path: string; rect: {x,y,w,h}; size: [number,number]; }; }
interface ITransformResult { root: IPureNode; features: IFeatures; frontmatter?: { title?: string; markmap?: Partial<IMarkmapJSONOptions> }; content: string; parserOptions?: object; }
```

## Hook Events

```ts
const hook = new Hook<[md: MarkdownIt]>();
hook.tap(fn);          // Register
hook.call(md);         // Trigger
hook.revoke(fn);       // Remove
```

Built-in hooks: `parser`(after md creation) | `beforeParse`(before each transform) | `afterParse`(after each transform) | `retransform`(re-render)

## walkTree

```ts
walkTree(root, (node, next, parent) => {
  const children = next();   // Recursive result of child nodes
  return processed;
});
```

## Asset Loading

```ts
import { loadJS, loadCSS, buildJSItem, buildCSSItem, mergeAssets } from 'markmap-common';
await loadJS(scripts, context);   // Dynamic script/iife loading
await loadCSS(styles);            // style/stylesheet loading
buildJSItem('d3@7/dist/d3.min.js');
buildCSSItem('style.css');
mergeAssets(a1, a2);             // Merge {scripts,styles}
persistJS(scripts, ctx);          // → HTML string array
persistCSS(styles);               // → HTML string array
```

## UrlBuilder

```ts
urlBuilder.setProvider('unpkg', p => `https://unpkg.com/${p}`);
await urlBuilder.findFastestProvider();
urlBuilder.getFullUrl('d3@7.8.5/dist/d3.min.js');
```

## Package Versions

| Package | Version | Package | Version |
|---------|---------|---------|---------|
| markmap-lib | 0.18.12 | markmap-view | 0.18.12 |
| markmap-common | 0.18.9 | markmap-render | 0.18.12 |