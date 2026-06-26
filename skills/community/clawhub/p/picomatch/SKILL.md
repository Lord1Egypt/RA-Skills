---
name: picomatch
description: Picomatch — A fast and accurate glob pattern matching library.
---

# Picomatch

A blazing fast, zero-dependency JavaScript glob pattern matching library, supporting standard and extended Bash glob features.

## Trigger Scenarios

Use when the user needs file path matching, glob wildcards (*, **, ?, [...]), .gitignore-style exclusion rules, build tool file filtering, CLI path filtering, file watcher allow/deny lists, etc.
Trigger keywords: picomatch, glob matching, *.js, **/*.ts, wildcards, .gitignore pattern matching, file filtering, minimatch alternative.

## Installation

```sh
npm install picomatch
```

## Core API

### picomatch(glob[, options]) → matcher

Main entry point: Takes a glob pattern and returns a matcher function.

```js
const pm = require('picomatch');
const isMatch = pm('*.js');

isMatch('a.js');  // true
isMatch('a.md');  // false
isMatch('a/b.js'); // false (* does not cross /)
```

### picomatch.isMatch(string, patterns[, options])

Directly checks if a string matches any pattern, without manually calling a matcher.

```js
picomatch.isMatch('a.a', ['b.*', '*.a']); // true
picomatch.isMatch('a.a', 'b.*');          // false
```

### picomatch.matchBase(input, glob)

Matches only the basename of a path (ignores directories).

```js
picomatch.matchBase('foo/bar.js', '*.js');  // true
```

### picomatch.scan(input[, options])

Parses a glob pattern into a structured object.

```js
picomatch.scan('!./foo/*.js', { tokens: true });
// { prefix: '!./', base: 'foo', glob: '*.js', negated: true, tokens: [...] }
```

### picomatch.parse(pattern[, options]) → state

Converts a glob to an intermediate state object, which can be used with `.compileRe` / `.makeRe`.

### picomatch.makeRe(pattern[, options]) → RegExp

Directly converts a glob to a RegExp.

```js
picomatch.makeRe('*.js');  // /^(?:(?!\.)(?=.)[^/]*?\.js)$/
```

### picomatch.toRegex(source[, options]) → RegExp

Creates a RegExp from a regex source string.

## Common Options

| Option | Type | Description |
|---|---|---|
| `dot` | boolean | Allow matching dotfiles, default false |
| `nocase` | boolean | Case-insensitive matching |
| `matchBase` | boolean | Match against basename only |
| `noglobstar` | boolean | Disable `**` matching nested directories |
| `noextglob` | boolean | Disable extglob (`+(a\|b)`) |
| `nobrace` | boolean | Disable brace expansion (`{a,b}`) |
| `globstar` | boolean | Treat single `*` as globstar (bash option) |
| `windows` | boolean | Support Windows backslash paths |
| `ignore` | array | Exclusion list (blacklist) |
| `onMatch` | function | Callback on match success |
| `onIgnore` | function | Callback on ignore |
| `onResult` | function | Callback on all results |

## Glob Syntax Quick Reference

| Syntax | Description |
|---|---|
| `*` | Match any character (excluding `/`, excluding dotfiles) |
| `**` | Match any character, including path separators |
| `?` | Match a single character |
| `[abc]` | Match any character within brackets |
| `{a,b}` | Match a or b (brace expansion) |
| `+(a\|b)` | Extglob: match one or more times |
| `!(pattern)` | Exclude matches |
| `!` prefix | Negated pattern |

## Practical Pattern Examples

```js
const pm = require('picomatch');

// JS/TS files
pm('**/*.{js,ts,mjs}');

// Ignore node_modules
pm('**', { ignore: 'node_modules/**' });

// Specific extension with subdirectories
pm('src/**/*.md');

// Dotfiles (hidden files)
pm('.*', { dot: true });

// Case-insensitive (Windows/macOS)
pm('*.JPG', { nocase: true });

// Windows paths
pm('src\\**\\*.js', { windows: true });
```

## Common Use Cases

- **File watcher allow/deny lists** — glob filtering for watchman / chokidar
- **.gitignore parsing** — parsing ignore pattern lists
- **CLI path filtering** — underlying engine for `glob` / `fast-glob`
- **Build artifact matching** — determining if a file belongs to dist output
- **minimatch alternative** — similar API but better performance (micromatch ecosystem)

## Detailed Reference

For complete API signatures, option descriptions, scan options, and option examples, see `references/api_reference.md`.