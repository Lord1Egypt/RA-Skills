---
name: minimatch
description: Use minimatch (glob pattern matching library) for file path matching, such as *.js, **/*.ts and other glob patterns. Note: Do NOT use user input as pattern source to prevent ReDoS attacks.
---

# minimatch

The glob matching library used internally by npm, converting glob expressions to JavaScript `RegExp`. Current version 10.x, ESM/CJS dual mode.

## Trigger Scenarios

Use when the user needs glob matching, file pattern matching, or .gitignore-style matching.

## Installation

```bash
npm install minimatch
```

## Basic Usage

```js
import { minimatch } from 'minimatch';
// or: const { minimatch } = require('minimatch');

minimatch('bar.foo', '*.foo');  // true
minimatch('bar.foo', '*.bar');  // false
minimatch('bar.foo', '*.+(bar|foo)', { debug: true }); // true + stderr debug output
```

## Supported Glob Features

- **Brace Expansion** — `{a,b}`, `{1..3}`
- **Extended glob** — `+(a|b)`, `*(a|b)`, `?(a|b)`, `@(a|b)`, `!(a|b)`
- **Globstar** — `**` matches any number of directory levels
- **Posix character classes** — `[[:alpha:]]` (full Unicode support, e.g., `é`)

## Exported APIs

### `minimatch(path, pattern, options?)`

Test whether a path matches a pattern:

```js
minimatch('src/app.js', '*.js', { matchBase: true }); // true
```

### `minimatch.filter(pattern, options?)`

Returns a filter function that can be passed to `Array.filter`:

```js
const jsFiles = fileList.filter(minimatch.filter('*.js', { matchBase: true }));
```

### `minimatch.match(list, pattern, options?)`

Performs fnmatch/glob style matching on a list of files. Returns the pattern itself when no matches are found and `nonull: true`:

```js
minimatch.match(fileList, '*.js', { matchBase: true });
```

### `minimatch.escape(pattern)`

Escapes all special characters in a glob pattern so it will match literal text only:

```js
minimatch.escape('*.js'); // '\*.js'
```

### `minimatch.unescape(pattern)`

Unescapes a pattern:

```js
minimatch.unescape('\\*.js'); // '*.js'
```

### `minimatch.makeRe(pattern, options?)`

Generates a RegExp object from a pattern:

```js
const re = minimatch.makeRe('*.js');
re.test('foo.js'); // true
```

## Minimatch Class

```js
import { Minimatch } from 'minimatch';
const mm = new Minimatch('**/*.js', { dot: true });

mm.match('src/foo.js');      // true
mm.match('.hidden.js');      // true (because dot: true)
mm.hasMagic();                // true
mm.makeRe();                  // Returns RegExp
mm.negate;                    // false — whether it's a negated ! pattern
mm.comment;                   // false — whether it's a # comment pattern
```

### `mm.matchOne(fileArray, patternArray, partial?)`

Matches path components after splitting by `/`, primarily used by glob-walkers to reduce filesystem calls.

## All Options (all default to `false`)

| Option | Description |
|--------|-------------|
| `debug` | Output debug information to stderr |
| `nobrace` | Disable `{a,b}` and `{1..3}` brace expansion |
| `noglobstar` | Disable `**` multi-level directory matching |
| `dot` | Allow matching filenames starting with `.` (disabled by default) |
| `noext` | Disable extglob patterns such as `+(a\|b)` |
| `nocase` | Case-insensitive matching |
| `nocaseMagicOnly` | Only effective when `nocase: true`, makes case-insensitive only for parts containing magic characters |
| `nonull` | When `minimatch.match` finds no matches, return `[pattern]` instead of `[]` |
| `magicalBraces` | Affects `hasMagic()`: treats braces without other magic characters as magic |
| `matchBase` | Patterns without `/` match against the path basename |
| `nocomment` | Disable comment patterns starting with `#` |
| `nonegate` | Disable negated `!` patterns |
| `flipNegate` | Reverse the result of negated patterns (return false on match) |
| `partial` | Partial path matching, used when traversing directory trees to determine if a match is possible |
| `windowsPathsNoEscape` | On Windows, `\` acts only as a path separator, not an escape character |
| `windowsNoMagicRoot` | On Windows + nocase, do NOT make UNC roots/drive letters case-insensitive |
| `preserveMultipleSlashes` | Preserve consecutive `/` (default `a///b` matches `a/b`) |
| `optimizationLevel` | Optimization level 0/1/2 (default 1), see reference documentation |
| `platform` | Defaults to `process.platform`, setting to `'win32'` triggers Windows behavior |

## Security Warning (❗Important)

minimatch uses JavaScript regular expressions. **Never pass user input as a pattern to this library** —

> If you build a system that takes user input and uses it directly as a regex pattern, whether with minimatch or any JS glob matcher, **you will be pwned**.

Future versions may switch to a non-backtracking matching algorithm, but this will not be backported.

## Path Notes

- **Use only `/` in patterns** — `\` is treated as an escape character
- On Windows, `\` in paths is automatically matched against `/`
- UNC paths (`//?/C:/...`, `//Server/Share/...`) receive special handling

## Reference Documentation

- Optimization level details → `references/optimization.md`