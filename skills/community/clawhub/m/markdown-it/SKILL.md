---
name: markdown-it
description: Use markdown-it to render Markdown to HTML, configure plugins, custom rendering rules, syntax highlighting.
---

# markdown-it

markdown-it is a Markdown parser for Node.js/browser, 100% CommonMark compliant, supports plugin extensions and custom syntax. Current version 14.x, ESM/CJS dual mode.

## Trigger Scenarios

Use when the user needs to parse/render Markdown, perform markdown-it related operations, or parse CommonMark.

## Installation

```bash
npm install markdown-it
```

## Basic Usage

```js
import MarkdownIt from 'markdown-it';
const md = new MarkdownIt();
const html = md.render('# Hello markdown-it!');
// <h1>Hello markdown-it!</h1>

// Inline rendering (no paragraph wrapping)
md.renderInline('**bold** text');
// <strong>bold</strong> text
```

## Presets

Three modes that control default enabled rules and options:

```js
// CommonMark strict mode (standard syntax only)
const md = new MarkdownIt('commonmark');

// Default mode (CommonMark + tables + strikethrough, recommended)
const md = new MarkdownIt('default');
// Equivalent to
const md = new MarkdownIt();

// Zero rules mode (completely empty, configure everything yourself)
const md = new MarkdownIt('zero');
```

## Complete Configuration Options

All defaults:

```js
const md = new MarkdownIt({
  html:         false,  // Allow HTML tags in source text
  xhtmlOut:     false,  // Use '/' to close single tags (<br />)
  breaks:       false,  // Convert newlines to <br>
  langPrefix:   'language-', // CSS language prefix for fenced code blocks
  linkify:      false,  // Automatically convert URLs to links
  typographer:  false,  // Smart quotes + language replacements
  quotes:       '""',   // Double + single quote replacement pairs
  highlight: function (str, lang) { return ''; }
});
```

## Plugin System

Chain `.use()` calls:

```js
import MarkdownIt from 'markdown-it';
import markdownItSub from 'markdown-it-sub';
import markdownItSup from 'markdown-it-sup';

const md = new MarkdownIt()
  .use(markdownItSub)
  .use(markdownItSup, /* plugin options */);
```

### Common Official Plugins

| Plugin | Feature |
|--------|---------|
| `markdown-it-sub` | Subscript `~subscript~` |
| `markdown-it-sup` | Superscript `^superscript^` |
| `markdown-it-footnote` | Footnotes `[^1]` |
| `markdown-it-deflist` | Definition lists |
| `markdown-it-abbr` | Abbreviations `<abbr>` |
| `markdown-it-emoji` | Emoji `:smile:` |
| `markdown-it-container` | Custom containers `::: warning` |
| `markdown-it-ins` | Insert `<ins>` via `++text++` |
| `markdown-it-mark` | Mark `<mark>` via `==text==` |
| `markdown-it-for-inline` | Iterator for traversing inline tokens |
| `markdown-it-anchor` | Heading anchor IDs |

Built-in extensions (enabled by default): **tables** (GFM), **strikethrough** (GFM `~~text~~`)

## Rule Management

```js
const md = new MarkdownIt();
md.disable(['link', 'image'])  // Disable specific rules
  .enable(['link'])            // Re-enable
  .enable('image');
```

## Syntax Highlighting

With highlight.js:

```js
import hljs from 'highlight.js';

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre><code class="hljs">' +
               hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
               '</code></pre>';
      } catch (_) {}
    }
    return '<pre><code class="hljs">' + md.utils.escapeHtml(str) + '</code></pre>';
  }
});
```

## Custom Rendering

Override renderer rules to modify output. For example, adding `target="_blank"` to all links:

```js
const defaultRender = md.renderer.rules.link_open ||
  function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };

md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
  tokens[idx].attrSet('target', '_blank');
  return defaultRender(tokens, idx, options, env, self);
};
```

Converting Vimeo links to iframe embeds:

```js
const defaultRender = md.renderer.rules.image;

md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const src = tokens[idx].attrGet('src');
  if (/^https?:\/\/(www\.)?vimeo.com\//.test(src)) {
    const id = src.split('/').pop();
    return `<div class="embed-responsive"><iframe src="//player.vimeo.com/video/${id}"></iframe></div>`;
  }
  return defaultRender(tokens, idx, options, env, self);
};
```

## linkify Configuration

After enabling `linkify: true`, you can further configure linkify-it:

```js
md.linkify.set({ fuzzyEmail: false }); // Disable auto email linking
md.linkify.tlds('.py', false);         // Allow .py top-level domain
```

## CLI

```bash
npm install -g markdown-it
markdown-it README.md > README.html
```

## Security

- Does **not** parse HTML in source text by default (`html: false`) to prevent XSS
- Output is always HTML-escaped (unless using `html: true`)
- To render user-generated Markdown, keep `html: false` (default)

## Reference Documentation

- Architecture principles and plugin development → Read `references/architecture.md`
- Plugin development FAQ → Read `references/plugin-dev.md`