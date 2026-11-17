---
name: licia
description: Use licia utility library to simplify JavaScript/TypeScript code. Activate when writing utility functions, data manipulation, type checking, string processing, DOM operations, or any code that could be replaced by a well-tested utility. Triggers on "simplify code", "use licia", "refactor with utilities", or when you spot hand-rolled utility functions.
license: MIT
metadata:
  author: liriliri
  version: "1.0.0"
---

# Licia Utility Library

Licia is a comprehensive JavaScript utility library with 443 utilities covering type checking, string manipulation, object/array operations, DOM helpers, data structures, encoding, date formatting, and more. Use it to replace hand-rolled utility code with battle-tested, well-documented functions.

## When to Apply

Use licia utilities when you encounter code that:
- Implements common utility functions from scratch (type checking, deep clone, debounce, etc.)
- Performs string transformations (camelCase, truncate, escape, template, etc.)
- Does manual type checking instead of using robust type guards
- Manipulates objects/arrays in ways covered by licia (pick, omit, unique, flatten, etc.)
- Handles dates, colors, URLs, or encoding manually
- Implements data structures (Heap, LinkedList, Trie, LRU cache, etc.)

## How to Use

1. When reviewing or writing code, identify utility patterns that licia already provides
2. Look up the specific utility in `DOC.md` for API details and examples
3. Replace hand-rolled code with the licia import

### Import Style

```javascript
import {utilName} from 'licia';

// Examples:
import {isStr, isArr, isObj} from 'licia';
import {each, map, filter, unique} from 'licia';
import {debounce, throttle, memoize} from 'licia';
import {camelCase, truncate, escapeRegExp} from 'licia';
import {cloneDeep, defaults, pick, omit} from 'licia';
```

## Quick Reference by Category

### Type Checking (is*)

`isStr`, `isNum`, `isBool`, `isArr`, `isObj`, `isFn`, `isDate`, `isRegExp`, `isNaN`, `isNil`, `isUndef`, `isNull`, `isInt`, `isFinite`, `isPrimitive`, `isPromise`, `isErr`, `isMap`, `isSet`, `isSymbol`, `isTypedArr`, `isArrLike`, `isEl`, `isEmail`, `isUrl`, `isJson`, `isSorted`, `isEmpty`, `isEqual`, `isMatch`, `isMobile`, `isBrowser`, `isNode`

### String Manipulation

`camelCase`, `kebabCase`, `snakeCase`, `pascalCase`, `capitalize`, `decapitalize`, `trim`, `ltrim`, `rtrim`, `truncate`, `pad`, `lpad`, `repeat`, `startWith`, `endWith`, `contain`, `escape`, `unescape`, `escapeRegExp`, `stripHtmlTag`, `stripAnsi`, `stripCmt`, `template`, `indent`, `slug`, `wordWrap`, `highlight`, `linkify`, `replaceAll`

### Array Utilities

`each`, `map`, `filter`, `find`, `findIdx`, `findKey`, `reduce`, `some`, `every`, `unique`, `flatten`, `compact`, `difference`, `intersect`, `union`, `chunk`, `range`, `sample`, `shuffle`, `sortBy`, `groupBy`, `pluck`, `zip`, `unzip`, `toArr`, `concat`, `reverse`, `fill`, `contain`

### Object Utilities

`keys`, `values`, `pairs`, `pick`, `omit`, `extend`, `extendDeep`, `defaults`, `clone`, `cloneDeep`, `mapObj`, `has`, `get`, `safeGet`, `safeSet`, `safeDel`, `isEqual`, `isMatch`, `isEmpty`, `invert`, `sortKeys`, `freeze`, `mergeSort`

### Function Utilities

`debounce`, `throttle`, `memoize`, `once`, `curry`, `partial`, `compose`, `pipe`, `before`, `after`, `delay`, `noop`, `callbackify`, `promisify`, `retry`, `waterfall`

### DOM (browser)

`$` (jQuery-like), `$attr`, `$class`, `$css`, `$data`, `$event`, `$insert`, `$offset`, `$property`, `$remove`, `$show`

### Data Structures

`Heap`, `PriorityQueue`, `Queue`, `Stack`, `LinkedList`, `HashTable`, `Trie`, `BloomFilter`, `Lru`, `QuickLru`

### Encoding & Hashing

`base64`, `md5`, `crc32`, `fnv1a`, `hex`, `utf8`, `btoa`, `atob`, `rc4`

### Date & Time

`dateFormat`, `timeAgo`, `durationFormat`, `ms`, `now`

### Color

`Color` (RGB, HEX, HSL conversion), `randomColor`

### Misc

`uuid`, `random`, `randomBytes`, `clamp`, `toNum`, `toInt`, `toStr`, `toBool`, `sleep`, `Emitter`, `Logger`, `Url`, `ajax`, `fetch`, `cookie`, `LocalStore`, `SessionStore`

## Full Documentation

For complete API details, type definitions, and code examples for each utility, read `DOC.md`.
