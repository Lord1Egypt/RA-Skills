# Plugin System

6 built-in plugins hook into the pipeline through ITransformHooks.

## Architecture

```ts
interface ITransformPlugin { name: string; config?: { versions, preloadScripts, resources, styles, scripts }; transform: (hooks) => IAssets; }
// hooks.parser.tap       after md creation → register markdown-it extensions
// hooks.beforeParse.tap  before transform → set context
// hooks.afterParse.tap   after transform → post-processing
```

## frontmatter — YAML Parsing

```yaml
---
title: My Map
markmap: { colorFreezeLevel: 2, maxWidth: 300 }
---
```
Auto-normalizes field types, merges htmlParser. Returns `context.frontmatter` + `context.parserOptions`.

## checkbox — `- [ ] / - [x]`

Replaces `[ ]`/`[x]` in heading and list item paragraphs with SVG checkbox icons. Implemented via markdown-it core rule.

## hljs — highlight.js Code Highlighting

```ts
{ name: 'hljs', config: { versions: { hljs }, preloadScripts: ['@highlightjs/cdn-assets@.../highlight.min.js'],
  styles: ['@highlightjs/cdn-assets@.../styles/default.min.css'] } }
```

`highlightAuto(str, [lang])` lazy activation, sets `features.hljs = true`.

## katex — LaTeX Formulas

`$...$` inline / `$$...$$` block formulas. Uses `@vscode/markdown-it-katex`, lazy activation.

```ts
{ name: 'katex', config: { versions: { katex, webfontloader },
  scripts: [webfontloader(defer), IIFE→WebFontConfig→refreshHook.call()],
  styles: ['katex@.../dist/katex.min.css'] } }
```

Auto-loads KaTeX fonts, triggers re-render on completion.

## prism — Prism.js Code Highlighting (hljs Alternative)

```ts
{ name: 'prism', config: { versions: { prismjs },
  preloadScripts: ['prismjs@.../components/prism-core.min.js', 'prismjs@.../plugins/autoloader/prism-autoloader.min.js'],
  styles: ['prismjs@.../themes/prism.css'] } }
```

`loadLanguages([lang])` dynamically loads language definitions, `Prism.highlight(str, grammar, lang)`.

## npm-url — `npm:` Path Resolution

Resolves `npm:` prefixed paths via UrlBuilder to CDN URLs in `afterParse`.

## source-lines — Line Number Tracking

Adds `data-lines="start,end"` to HTML, auto-offsets frontmatter line counts.

## Custom Plugins

```ts
definePlugin({ name: 'my-plugin', config: { styles: [...] },
  transform(hooks) {
    hooks.parser.tap(md => md.use(myPlugin));
    hooks.beforeParse.tap((md, ctx) => ctx.content = preprocess(ctx.content));
    return { styles: myPlugin.config?.styles, scripts: [...] };
  }
});
const tr = new Transformer([myPlugin]);
```