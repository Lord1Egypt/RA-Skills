---
name: gray-matter
description: Parse YAML/JSON/TOML front-matter from strings or files using the gray-matter library.
---

# Gray Matter

Parse YAML/JSON/TOML/CSON/CoffeeScript front-matter from strings or files.
Use whenever working with markdown files that have front-matter (YAML/JSON/TOML headers), extracting metadata from documents with ---- delimited headers, stringifying data back to front-matter format, or any task involving front-matter parsing/stringification.

## Triggers

"front matter", "frontmatter", "gray-matter", "YAML header","parse markdown metadata", "extract front matter", "add front matter", "stringify front matter".

## Quick Start

Use `scripts/parse.js` for all front-matter operations:

```bash
# Parse front-matter from a file (outputs JSON)
node scripts/parse.js path/to/file.md

# Parse from piped stdin
type file.md | node scripts/parse.js --stdin

# Output only the front-matter data (YAML format)
node scripts/parse.js file.md --data-only

# Output only the content (no front-matter)
node scripts/parse.js file.md --content-only

# Include excerpt in output
node scripts/parse.js file.md --excerpt

# Force a specific language
node scripts/parse.js file.md --lang json

# Custom delimiters
node scripts/parse.js file.md --delims "~~~"

# Test if a file has front-matter
node scripts/parse.js file.md --test

# Stringify: write JSON data to a temp file, then:
node scripts/parse.js data.json --stringify
# Outputs front-matter delimiters wrapping YAML-serialized data
```

## Common Operations

### 1. Extract metadata from a markdown file

```bash
node scripts/parse.js path/to/post.md --data-only
```

### 2. Strip front-matter, keep only content

```bash
node scripts/parse.js path/to/post.md --content-only
```

### 3. Check if a file has front-matter

```bash
node scripts/parse.js path/to/file.md --test
# prints: true or false
```

### 4. Add front-matter to content

Write JSON data to a temp file, then stringify:
```bash
node scripts/parse.js _data.json --stringify
# Prepends YAML front-matter (with --- delimiters) to empty content
```

### 5. Parse TOML front-matter

gray-matter does not include a TOML engine by default. First install the `toml` package:
```bash
cd <skill-dir>/scripts && npm install toml
```

Then use inline `require('gray-matter')` with a custom engine:
```js
const toml = require('toml');
const matter = require('gray-matter');
const result = matter(str, {
  engines: { toml: toml.parse.bind(toml) },
  language: 'toml'
});
```

Alternatively, gray-matter auto-detects the language when specified in the delimiter line:
```
---toml
title = "My Post"
---
```

## When to Use the Script vs Inline Code

- **Use the script** (above) for most operations -- it handles edge cases reliably
- **Use inline `require('gray-matter')`** only when doing programmatic transformations (iterating over many files, conditional logic, custom engine integration). In that case, see `references/api.md` for the full API.

## Script Installation

The script auto-installs gray-matter via `npm install gray-matter` on first run. If auto-install fails, run manually:

```bash
cd <skill-dir>/scripts && npm install gray-matter
```

## Reference

See `references/api.md` for the complete gray-matter API documentation (main function, static methods, all options, engines, deprecated options).