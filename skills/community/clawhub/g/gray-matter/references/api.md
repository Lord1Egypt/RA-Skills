# gray-matter API Reference

> Parse front-matter from a string or file. Parses YAML by default; also supports JSON, TOML, CoffeeScript front-matter.

## Main Function

```js
const matter = require('gray-matter');
matter(input, options)
```

**Params:**
- `input` — String (or object with `content` property) containing front-matter
- `options` — Optional options object

**Returns:** A `file` object with:

| Property | Type | Description |
|---|---|---|
| `file.data` | Object | Parsed front-matter data |
| `file.content` | String | Input string with front-matter stripped |
| `file.excerpt` | String | Excerpt if option is set |
| `file.empty` | String | Original string if front-matter is empty |
| `file.isEmpty` | Boolean | true if front-matter is empty |
| `file.orig` | Buffer | Original input (non-enumerable) |
| `file.language` | String | Parsed language (`yaml` default) |
| `file.matter` | String | Raw un-parsed front-matter string (non-enumerable) |
| `file.stringify` | Function | Stringify back to front-matter |

## Static Methods

### `matter.read(filepath, options)`

Synchronously read a file and parse front matter. Returns same object as main function.

```js
const file = matter.read('./content/blog-post.md');
```

### `matter.test(str, options)`

Returns `true` if the given string has front matter.

```js
matter.test('---\ntitle: Hello\n---\nContent'); // true
matter.test('Plain text'); // false
```

### `matter.stringify(content, data, options)`

Stringify an object to YAML (or specified language) and prepend to content.

```js
matter.stringify('Hello world', { title: 'Home' });
// ---
// title: Home
// ---
// Hello world
```

## Options

### `options.language` (String, default: `"yaml"`)

Engine to use for parsing. Supported: `yaml`, `json`, `javascript`, `toml`, `coffee`, `cson`.

Dynamic detection is also supported — if the delimiter is followed by the language name:
```
---toml
title = "TOML"
---
```

### `options.delimiters` (String|Array, default: `"---"`)

Custom open/close delimiters. Can be a string (same for both) or `[open, close]` array.

```js
matter.read('file.md', { delimiters: '~~~' });
matter.read('file.md', { delimiters: ['~~~', '~~~'] });
```

### `options.excerpt` (Boolean|Function)

Extract an excerpt following front-matter. If `true`, grabs everything up to the next `---` delimiter.

```js
matter(str, { excerpt: true });
```

Can also be a function:
```js
matter(str, {
  excerpt: function(file, options) {
    file.excerpt = file.content.split('\n').slice(0, 4).join(' ');
  }
});
```

### `options.excerpt_separator` (String)

Custom separator for excerpts.

```js
matter(str, { excerpt_separator: '<!-- end -->' });
```

### `options.engines` (Object)

Custom engines for parsing/stringifying front-matter. Each engine is an object with `parse` and optional `stringify` methods, or a parse function.

```js
const toml = require('toml');
matter(str, {
  engines: {
    toml: toml.parse.bind(toml),
  }
});

// Or as object with stringify:
matter(str, {
  engines: {
    toml: {
      parse: toml.parse.bind(toml),
      stringify: function(data) {
        throw new Error('cannot stringify to TOML');
      }
    }
  }
});
```

### Deprecated Options

| Old | New |
|---|---|
| `options.lang` | `options.language` |
| `options.delims` | `options.delimiters` |
| `options.parsers` | `options.engines` |