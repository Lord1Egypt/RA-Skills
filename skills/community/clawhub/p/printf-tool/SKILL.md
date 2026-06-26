---
name: printf-tool
description: Format and print data with precise control over output format. Use for formatted output with padding, precision, and type specifications.
---
# Printf - Formatted Output Utility

Format and display data using format specifiers similar to C printf. Supports string, integer, floating-point, and hexadecimal formatting with width and precision control.

## Usage
```bash
printf-tool <format> [arguments...]
```

## Common Format Specifiers

- `%s`: String
- `%d`: Integer
- `%f`: Floating point
- `%x`: Hexadecimal
- `%05d`: Zero-padded integer (5 digits)

## Examples

```bash
printf-tool "Name: %s, Age: %d" "Alice" 30
printf-tool "Price: $%.2f" 19.99
printf-tool "%010d" 42
```