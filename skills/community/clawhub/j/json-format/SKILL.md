---
name: json-format
description: Format, prettify, minify, or validate JSON. Use when the user asks to format JSON, prettify JSON, beautify JSON, minify JSON, compress JSON, validate JSON, fix JSON indentation, or make JSON readable.
---

# JSON Formatter

Format and validate JSON — pretty-print with configurable indentation or minify to a single line.

## Input
- A JSON string (object, array, string, number, boolean, or null)
- May be already formatted or a single minified line
- Optional action: format (default), minify, or validate-only
- Optional indent size: 2 (default) or 4 spaces

## Output
- **format**: Pretty-printed JSON with proper indentation and line breaks
- **minify**: Single-line compact JSON with no whitespace
- **validate**: A message confirming valid or invalid JSON (with error details)

## Instructions

1. Receive the raw JSON string from the user.
2. Determine the requested action (default: format).
3. Attempt to parse the JSON:
   - Call `JSON.parse(input)` conceptually — parse the string strictly following JSON spec.
   - If parsing fails, report the error with as much detail as possible (e.g., "Unexpected token at position 42", "Missing closing bracket").
4. For **format** action:
   - Serialize the parsed value back to a string with the requested indent size (default: 2 spaces).
   - Use `JSON.stringify(parsed, null, indentSize)` semantics: keys are sorted by insertion order (not alphabetically), arrays and objects are expanded across multiple lines, strings are double-quoted.
5. For **minify** action:
   - Serialize with no indentation or extra whitespace: `JSON.stringify(parsed)` semantics.
6. For **validate** action:
   - If parsing succeeded, report "Valid JSON" along with type and top-level key count if it is an object.
   - If parsing failed, report the error message.
7. If sort-keys option is requested, sort all object keys alphabetically at every nesting level before serializing.
8. Output the result.

## Options
- `indent`: `2` (default) | `4` — number of spaces per indent level
- `action`: `format` (default) | `minify` | `validate`
- `sort-keys`: `false` (default) | `true` — sort object keys alphabetically

## Examples

**Format (default, 2-space indent)**

Input:
```
{"name":"Alice","age":30,"hobbies":["reading","coding"]}
```

Output:
```json
{
  "name": "Alice",
  "age": 30,
  "hobbies": [
    "reading",
    "coding"
  ]
}
```

**Minify**

Input:
```json
{
  "name": "Alice",
  "age": 30
}
```

Output:
```
{"name":"Alice","age":30}
```

**Validate — invalid JSON**

Input:
```
{name: 'Alice', age: 30}
```

Output:
```
Invalid JSON: Unexpected token 'n' at position 1. Keys must be double-quoted strings and string values must use double quotes, not single quotes.
```

**Format with 4-space indent and sort-keys**

Input:
```
{"z":3,"a":1,"m":2}
```

Output:
```json
{
    "a": 1,
    "m": 2,
    "z": 3
}
```

## Error Handling
- If the input is empty or whitespace-only, respond: "No input provided. Please paste a JSON string."
- If `JSON.parse` fails, report the error message and the approximate position or line number if determinable. Do not attempt to silently fix the JSON — report the exact parse error. (If the user wants repair, suggest using the json-repair skill.)
- If the input is valid JSON but the user asked to "format" a primitive (e.g., just `42` or `"hello"`), format it as-is (a primitive is valid JSON).
- Never truncate the output — always return the full formatted result.
