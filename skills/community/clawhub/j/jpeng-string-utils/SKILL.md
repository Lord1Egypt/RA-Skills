---
name: string-utils
description: Provides string manipulation and transformation operations for working with text. Use when you need to transform, format, or manipulate strings.
---

# String Utils

Provides string manipulation and transformation operations.

## Usage

```javascript
const str = require('./skills/string-utils');

// Case conversion
const camel = str.toCamelCase('hello world'); // helloWorld
const snake = str.toSnakeCase('helloWorld'); // hello_world
const kebab = str.toKebabCase('helloWorld'); // hello-world

// Trimming and padding
const trimmed = str.trim('  hello  '); // 'hello'
const padded = str.padLeft('5', 3, '0'); // '005'

// Truncation
const short = str.truncate('hello world', 8); // 'hello...'

// Slug generation
const slug = str.slugify('Hello World!'); // 'hello-world'

// Escape/unescape
const escaped = str.escapeHtml('<div>'); // '&lt;div&gt;'
```

## Features

- Case conversion (camelCase, snake_case, kebab-case, PascalCase, etc.)
- Trimming and padding
- Truncation with ellipsis
- Slug generation
- HTML escape/unescape
- URL encoding/decoding
- Template interpolation
- String similarity
