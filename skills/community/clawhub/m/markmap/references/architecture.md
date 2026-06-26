# Architecture & Pipeline

## Package Structure

```
markmap-lib           ← Markdown → mindmap data
markmap-view          ← Data → SVG interactive rendering
markmap-render        ← Data → HTML template filling
markmap-html-parser   ← HTML → pure node tree
markmap-common        ← Shared: Hook/walkTree/UrlBuilder/loader
markmap-cli           ← CLI tool
```

## Markdown → SVG Pipeline

```
Markdown → Transformer.transform()
  ├─ frontmatter plugin → YAML parsing
  ├─ markdown-it(html:true, breaks:true) → HTML
  ├─ Plugin enhancements (katex/hljs/checkbox/source-lines)
  ├─ markmap-html-parser → buildTree(html)
  │   ├─ cheerio<string> → classify by selector rules
  │   ├─ Comment extraction: <!--markmap: fold--> → payload.fold
  │   └─ cleanNode() → remove empty intermediate nodes
  └─ ITransformResult { root, features, frontmatter }

Markmap.setData(root)
  ├─ _initializeData() → INode: id/depth/key/path
  ├─ _relayout() → d3-flextree layout
  │   ├─ foreignObject → measure actual rendered size
  │   └─ flextree → tree coordinates(x,y,width,height)
  └─ renderData() → D3 data join
      ├─ g.markmap-node → foreignObject+circle+line
      ├─ path.markmap-link → Bezier curves
      └─ g.markmap-highlight → highlight box
  → Interactive SVG
```

## Transformer.transform() Execution Order

```
hooks.beforeParse → md.render(rawContent) → hooks.afterParse → buildTree(html) → cleanNode(root)
                                                                      ↓
                                                               parseHtml → cheerio traversal
                                                               convertNode → to IPureNode
```

## Asset Loading Flow

```
transform() → features: { katex:true, hljs:false, ... }
getUsedAssets(features) → { styles:[CSSItem], scripts:[JSItem] }
  ├─ Browser: loadJS() → <script>/<link rel:preload> + fetch fallback
  ├─ CLI: fillTemplate → persistJS/persistCSS → inline into HTML
  └─ Offline: inlineAssets → all assets inlined, no CDN
```