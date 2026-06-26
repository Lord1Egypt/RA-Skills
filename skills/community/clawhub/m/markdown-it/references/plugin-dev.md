# markdown-it Plugin Development

## Choosing the Right Place

1. Does it conflict with existing markup (priority issues)?
   - Yes → Write an inline or block rule
   - No → Morph tokens in the core chain
2. Modifying tokens in the core chain is simpler than writing block/inline rules (when not duplicating existing rules), but block/inline rules are usually faster
3. Sometimes simply modifying the renderer is enough (e.g., adding header IDs or `target="_blank"`)
4. Plugins should **not** depend on `markdown-it` in `package.json`. Internal APIs are passed in via the parser instance

## Development Essentials

- Search existing [plugins](https://www.npmjs.org/browse/keyword/markdown-it-plugin) or [source rules](https://github.com/markdown-it/markdown-it/tree/master/lib) first
- Keywords for npm package `package.json`: `markdown-it` + `markdown-it-plugin` (for plugins), `markdown-it` (for related packages)

## FAQ

### How to implement an async rule?

Not directly supported. Workarounds:
1. During parsing, replace content with random numbers and store in `env`
2. Process data asynchronously
3. Replace back with text during rendering

Or render HTML → parse into DOM/cheerio AST → transform using a more convenient approach.

### How to replace part of a text token with a link?

Correct sequence: Split the text token → insert link_open/text/link_close tokens.
Reference implementations: [linkify](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_core/linkify.mjs) and [emoji](https://github.com/markdown-it/markdown-it-emoji/blob/master/lib/replace.mjs).

**Do not replace text with HTML fragments! It is unsafe.**

### Why isn't my inline rule executing?

The inline parser skips large text sections for performance, stopping only at [a small set of specific characters](https://github.com/markdown-it/markdown-it/blob/master/lib/rules_inline/text.mjs). This list is not extensible. If you find that an important character is missing, file an issue.

### Token attribute manipulation

```js
tokens[idx].attrGet('src');           // Get attribute
tokens[idx].attrSet('target', '_blank'); // Set attribute
tokens[idx].attrIndex('class');       // Find attribute index
tokens[idx].attrPush(['class', 'foo']); // Append attribute
tokens[idx].attrJoin('class', 'foo'); // Merge attribute value
```