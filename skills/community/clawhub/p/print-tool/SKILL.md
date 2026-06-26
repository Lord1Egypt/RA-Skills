---
name: print-tool
description: Output text and variable values to standard output. Use for displaying messages, script output, and debug information.
---
# Print - Text Output Utility

Write text to standard output with optional formatting. Supports multiple arguments, newline control, and special character escaping.

## Usage
```bash
print-tool [options] [text...]
```

## Options

- `-n`: Suppress trailing newline
- `-e`: Enable interpretation of escape sequences

## Examples

```bash
print-tool "Hello World"
print-tool -n "No newline"
print-tool -e "Line1\nLine2"
```