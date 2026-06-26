---
name: protobuf-linter
description: Lint Protocol Buffer (.proto) files for style, naming conventions, breaking changes, and best practices. Supports proto2 and proto3 syntax with 24 rules across structure, naming, security, and compatibility categories.
---

# Protobuf Linter

Lint `.proto` files for style violations, naming issues, breaking changes, and best practices.

## Commands

```bash
# Lint a proto file (all rules)
python3 scripts/protobuf_linter.py lint path/to/file.proto

# Check naming conventions only
python3 scripts/protobuf_linter.py naming path/to/file.proto

# Check for breaking changes between two versions
python3 scripts/protobuf_linter.py breaking path/to/old.proto path/to/new.proto

# Validate syntax and structure
python3 scripts/protobuf_linter.py validate path/to/file.proto

# Lint a directory recursively
python3 scripts/protobuf_linter.py lint path/to/protos/ --recursive

# JSON output
python3 scripts/protobuf_linter.py lint path/to/file.proto --format json

# Summary only
python3 scripts/protobuf_linter.py lint path/to/file.proto --format summary
```

## Rules (24)

### Structure (6)
- Missing syntax declaration
- Missing package declaration  
- Empty message/enum/service definitions
- Duplicate field numbers
- Reserved field number conflicts
- Import not found (relative path check)

### Naming (8)
- Message names must be CamelCase
- Enum names must be CamelCase
- Enum values must be UPPER_SNAKE_CASE
- Enum values must be prefixed with enum name
- Field names must be lower_snake_case
- Service names must be CamelCase
- RPC method names must be CamelCase
- Package names must be lower_snake_case with dots

### Compatibility (5)
- Changed field type (breaking)
- Removed field without reserving number (breaking)
- Changed field number (breaking)
- Renamed enum value (breaking)
- Changed RPC request/response type (breaking)

### Best Practices (5)
- Use proto3 syntax (proto2 warning)
- Avoid required fields (proto2)
- Use wrapper types for optional semantics
- Comment coverage (messages/services)
- File should match package name

## Output Formats

- **text** (default): Human-readable with colors and severity icons
- **json**: Machine-readable with file, line, rule, severity, message
- **summary**: Counts by severity only

## Exit Codes

- 0: No issues (or warnings only)
- 1: Errors found
- 2: Invalid input
