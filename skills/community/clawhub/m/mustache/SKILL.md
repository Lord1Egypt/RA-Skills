---
name: mustache
description: Use mustache.js (logic-less Mustache templates) for any templating task in JavaScript/Node.js environments.
---

# Mustache

Zero-dependency, logic-less template engine for JavaScript. Renders tags in templates using values from a view object.

## Triggers

when the user asks to render templates, use Mustache syntax {{ }}, create .mustache files,generate HTML/config/code from templates, or mentions mustache/mustache.js/{{mustache}}.

## Covers

variables, sections, inverted sections, partials, comments, custom delimiters, CLI usage,
pre-parsing/caching, and common patterns (email templates, config generation, code scaffolding).

## Install

```bash
npm install mustache --save        # project dependency
npm install -g mustache            # CLI tool
```

## Core API

```js
const Mustache = require('mustache');
const html = Mustache.render(template, view, partials, tags);
```

- `template` (string) — Mustache template string
- `view` (object) — data & helper functions
- `partials` (object, optional) — `{ name: partialString }`
- `tags` (string[], optional) — custom delimiters `[ open, close ]`

## Tag Types Quick Reference

| Tag | Syntax | Behavior |
|-----|--------|----------|
| Variable | `{{key}}` | HTML-escaped value |
| Unescaped | `{{{key}}}` or `{{&key}}` | Raw HTML output |
| Dot notation | `{{a.b.c}}` | Nested property access |
| Current item | `{{.}}` | Current item in string array loop |
| Section | `{{#key}}...{{/key}}` | Truthy → render block; array → loop |
| Inverted | `{{^key}}...{{/key}}` | Falsy/empty → render block |
| Comment | `{{! text }}` | Stripped from output |
| Partial | `{{> name}}` | Inline another template |
| Set Delimiter | `{{=<% %>=}}` | Change tag delimiters |

## Sections — Detailed

**Falsy (skip):** `null`, `undefined`, `false`, `0`, `NaN`, `""`, `[]` → block not rendered.

**Non-empty array (loop):** Block renders once per item; context shifts to each item.

```js
// String array — use {{.}} for current item
Mustache.render('{{#items}}- {{.}}\n{{/items}}', { items: ['a','b'] });
// → "- a\n- b\n"

// Object array — access properties directly
Mustache.render('{{#people}}* {{name}}\n{{/people}}', {
  people: [{ name: 'Alice' }, { name: 'Bob' }]
});
// → "* Alice\n* Bob\n"

// Lambda function — receives raw block text + render helper
Mustache.render('{{#bold}}Hi {{name}}{{/bold}}', {
  name: 'World',
  bold: function() {
    return function(text, render) {
      return '<b>' + render(text) + '</b>';
    };
  }
});
// → "<b>Hi World</b>"
```

## Partials

Pass as third argument; inherit the calling context.

```js
Mustache.render(
  '<h2>Names</h2>{{#names}}{{> user}}{{/names}}',
  { names: [{ name: 'Alice' }, { name: 'Bob' }] },
  { user: '<strong>{{name}}</strong>\n' }
);
// → <h2>Names</h2>\n<strong>Alice</strong>\n<strong>Bob</strong>\n
```

## Custom Delimiters

```js
// JS: pass as 4th argument or set Mustache.tags
Mustache.render(template, view, {}, ['<%', '%>']);

// Template: set delimiter inline
{{=<% %>=}}<% erb_style %><%={{ }}=%>
// Delimiters may not contain whitespace or =
```

## Pre-parsing / Caching

```js
Mustache.parse(template);  // cache parsed tree
// Later calls with the same template skip parsing
```

## CLI Usage

```bash
mustache data.json template.mustache > output.html
mustache data.json -p partials/header.mustache -p partials/footer.mustache template.mustache
cat data.json | mustache - template.mustache > output.html
```

## Common Patterns

For detailed examples and anti-patterns, see [references/patterns.md](references/patterns.md).

**Escape override** (for non-HTML like config files):
```js
Mustache.escape = t => t;
```

**Include template in HTML** (static sites):
```html
<script id="tpl" type="x-tmpl-mustache">{{> content}}</script>
```

**Async load template** (SPAs):
```js
fetch('tpl.mustache').then(r => r.text()).then(t => {
  document.getElementById('out').innerHTML = Mustache.render(t, data);
});
```

## Anti-patterns

- Do NOT put logic in views — Mustache is logic-less; move logic to pre-processing
- Avoid recursive partials without a termination condition
- Do NOT use `Mustache.escape = t => t` globally without restoring it afterward
