# Transformer + Frontmatter

Core library `markmap-lib`: Markdown → mindmap data.

```bash
npm install markmap-lib
```

## Transformer

```ts
import { Transformer } from 'markmap-lib';
const tr = new Transformer();               // With all built-in plugins
const tr = new Transformer([myPlugin]);      // Custom plugins
const tr = new Transformer([]);              // No plugins (no-plugins entry)
```

### transform(markdown) → ITransformResult

```ts
const { root, features, frontmatter, content, parserOptions } = tr.transform(mdContent);
// root:      IPureNode — tree root
// features:  IFeatures — detected features (katex/hljs, etc.)
// frontmatter: { title?: string, markmap?: Partial<IMarkmapJSONOptions> }
```

### Asset Management

```ts
tr.getAssets();                          // All plugin assets
tr.getAssets(['katex', 'hljs']);         // Filter by name
tr.getUsedAssets(features);              // Auto-filter by features from transform()
// → { styles: CSSItem[], scripts: JSItem[] }
tr.resolveJS(item);   // URL resolution
tr.resolveCSS(item);
```

### CDN / Offline

```ts
tr.urlBuilder.setProvider('unpkg', path => `https://unpkg.com/${path}`);
await tr.urlBuilder.findFastestProvider();   // Auto speed test
tr.urlBuilder.provider = 'local';            // Offline mode
```

### markdown-it Configuration

```ts
const md = MarkdownIt({ html: true, breaks: true });
md.use(md_ins).use(md_mark).use(md_sub).use(md_sup);
// Supports: ++insert++ / ==mark== / ~subscript~ / ^superscript^
```

### HTML Parser

```bash
npm install markmap-html-parser
```

```ts
import { buildTree, parseHtml, convertNode } from 'markmap-html-parser';
const root = buildTree(html, parserOptions);  // HTML → IPureNode
```

**Levels:** None(0) → H1(1) → H2(2) → ... → H6(6) → Block(7) → List(8) → ListItem(9)

**Selector Rules:** `div,p`(expand children) → `h1-h6`(heading nodes) → `ul,ol`(child lists) → `li`(list items) → `table,pre,p>img:only-child`(preserve as-is)

**Comment Controls:** `<!--markmap: fold-->` → payload.fold=1, `<!--markmap: foldAll-->` → payload.fold=2

## Frontmatter

```markdown
---
title: My Map
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 3
  maxWidth: 300
---
```

Option values are auto-normalized: `extraJs/extraCss/color` string→array, `duration/maxWidth` etc. → number.

## Browser CDN

```html
<script src="https://cdn.jsdelivr.net/npm/markmap-lib/dist/browser/index.iife.js"></script>
<script>const { Transformer } = window.markmap;</script>
```

## Vite Multi-Target Build

| Target | Format | File |
|--------|--------|------|
| node | CJS+ESM | dist/index.js/.mjs |
| nodeLight (no plugins) | CJS+ESM | dist/index.no-plugins |
| browserEs | ESM | dist/browser/index.mjs |
| browserJs | IIFE | dist/browser/index.iife.js |

Compile-time injections: `__define__.LIB_VERSION` `__define__.VIEW_VERSION` `__define__.PRISM_VERSION` `__define__.HLJS_VERSION` `__define__.KATEX_VERSION` `__define__.NO_PLUGINS` `__define__.TEMPLATE`