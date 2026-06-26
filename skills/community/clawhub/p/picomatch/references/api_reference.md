# Picomatch API Reference

## Complete API Signatures

### picomatch(globs[, options]) → Function

Creates a matcher function. Pass `true` as the second argument to return an `{ isMatch, match, output }` object.

```js
const matcher = pm('*.js');
matcher('a.js');        // true
matcher('a.js', true);  // { isMatch: true, match: [...], output: 'a.js' }
```

### picomatch.test(input, regex[, options]) → Object

Tests input directly with a regex, returns match information object.

### picomatch.matchBase(input, glob[, options]) → Boolean

Matches only against the basename of the path.

### picomatch.isMatch(str, patterns[, options]) → Boolean

Checks whether a string matches any pattern. Patterns can be a string or an array.

### picomatch.scan(input[, options]) → Object

Scans and parses a glob pattern, returning the parsed result:

```js
pm.scan('!./foo/*.js', { tokens: true });
// {
//   prefix: '!./', input: '!./foo/*.js', start: 3,
//   base: 'foo', glob: '*.js',
//   isBrace: false, isBracket: false, isGlob: true,
//   isExtglob: false, isGlobstar: false, negated: true,
//   maxDepth: 2,
//   tokens: [
//     { value: '!./', depth: 0, isGlob: false, negated: true, isPrefix: true },
//     { value: 'foo', depth: 1, isGlob: false },
//     { value: '*.js', depth: 1, isGlob: true }
//   ],
//   slashes: [2, 6],
//   parts: ['foo', '*.js']
// }
```

### picomatch.parse(pattern[, options]) → Object

Returns a `{ output, ... }` state object.

### picomatch.compileRe(state[, options]) → RegExp

Compiles a regex from a parse result.

### picomatch.makeRe(state[, options]) → RegExp

Creates a regular expression for matching.

### picomatch.toRegex(source[, options]) → RegExp

Creates a RegExp instance from a regex source string.

## Complete Options Table

### Picomatch Main Options

| Option | Type | Default | Description |
|---|---|---|---|
| `basename` | boolean | false | Match basename when pattern contains no `/` |
| `bash` | boolean | false | Strict bash rules, `*` ⇒ `**` |
| `capture` | boolean | undefined | Return regex capture groups |
| `contains` | boolean | undefined | Allow matching anywhere in the string |
| `debug` | boolean | undefined | Print debug info on error |
| `dot` | boolean | false | Enable dotfile matching |
| `expandRange` | function | undefined | Custom brace range expansion function |
| `fastpaths` | boolean | true | Skip full parsing for common patterns to speed up |
| `flags` | string | undefined | Regex flags (overrides nocase) |
| `format` | function | undefined | Format input string before matching |
| `ignore` | array/string | undefined | Exclusion pattern list |
| `keepQuotes` | boolean | false | Keep quotes in generated regex |
| `literalBrackets` | boolean | undefined | Match literal brackets only |
| `matchBase` | boolean | false | Alias for basename |
| `maxLength` | number | 65536 | Maximum input length |
| `maxExtglobRecursion` | number/boolean | 0 | Limit extglob nesting depth, false disables limit |
| `nobrace` | boolean | false | Disable brace matching |
| `nobracket` | boolean | undefined | Disable bracket matching |
| `nocase` | boolean | false | Case-insensitive matching |
| `noext` | boolean | false | Alias for noextglob |
| `noextglob` | boolean | false | Disable extglob |
| `noglobstar` | boolean | false | Disable `**` |
| `nonegate` | boolean | false | Disable `!` negation |
| `onIgnore` | function | undefined | Callback for ignored items |
| `onMatch` | function | undefined | Callback for matched items |
| `onResult` | function | undefined | Callback for all items |
| `posix` | boolean | false | Support POSIX character classes `[[:alpha:]]` |
| `prepend` | string | undefined | Regex prefix |
| `regex` | boolean | false | `*` after brackets follows regex semantics |
| `strictBrackets` | boolean | undefined | Error on unbalanced brackets/braces |
| `strictSlashes` | boolean | undefined | `*` does not match trailing `/` |
| `unescape` | boolean | undefined | Remove `\\` escape characters |
| `windows` | boolean | false | Support `\\` as path separator |

### Scan Options

| Option | Type | Default | Description |
|---|---|---|---|
| `tokens` | boolean | false | Return token array |
| `parts` | boolean | false | Return path segment string array (auto-enabled when tokens=true) |

### Option Examples

**expandRange**:
```js
const fill = require('fill-range');
pm.makeRe('foo/{01..25}/bar', {
  expandRange(a, b) { return `(${fill(a, b, { toRegex: true })})`; }
});
// /^(?:foo\/((?:0[1-9]|1[0-9]|2[0-5]))\/bar)$/
```

**format**:
```js
const isMatch = pm('foo/*.js', { format: s => s.replace(/^\.\//, '') });
isMatch('./foo/bar.js'); // true
```

**onMatch / onIgnore / onResult**:
```js
const onMatch = ({ glob, regex, input, output }) => console.log({ glob, regex, input, output });
pm('*', { onMatch })('foo');
```

## Glob Syntax Details

### Basic Syntax

| Character | Description |
|---|---|
| `*` | Match zero or more non-separator characters, excluding dotfiles |
| `**` | Match zero or more any characters, including path separators |
| `?` | Match a single non-separator character |
| `[abc]` | Character class, matches any character within brackets |
| `[a-z]` | Range, matches any character a-z |

### Advanced Syntax

**Braces**:
```
{a,b}        → matches a or b
{1..5}       → matches 1,2,3,4,5
{01..10}     → matches 01,02,...,10
```

**Extglobs**:
```
?(pattern)           → zero or one times
*(pattern)           → zero or more times
+(pattern)           → one or more times
@(pattern)           → exactly once
!(pattern)           → matches anything not matching pattern
+(a|b|c)             → one or more times a/b/c
```

**POSIX Brackets** (requires options.posix = true):
```
[[:alpha:]]          → letters
[[:digit:]]          → digits
[[:alnum:]]          → letters or digits
[[:space:]]          → whitespace
[[:upper:]]          → uppercase letters
[[:lower:]]          → lowercase letters
[[:punct:]]          → punctuation
```

### Escaping

```js
pm('\\[a\\]');       // matches literal [a]
pm('a/b');           // matches a/b on posix
pm('a\\b');          // matches a\b on posix (backslash literal)
```

## Behavioral Differences from Bash

- In Bash, `*` can match subdirectories; in picomatch it cannot (use `**`)
- In Bash, `*` does not match dotfiles; picomatch can enable this with `{ dot: true }`
- picomatch does not support backslash path separators by default (requires `{ windows: true }`)

## Comparison with Other Libraries

| Library | Size | Dependencies | Speed | Features |
|---|---|---|---|---|
| **picomatch** | Tiny | 0 | Fastest | Core of micromatch |
| minimatch | Medium | 1 | Fast | Long history, used by node glob |
| micromatch | Larger | 2 | Fast | Most feature-rich, based on picomatch |