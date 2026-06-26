---
name: Example Skill
description: A representative skill for testing compression
version: 0.1.0
---

# Example Skill

A skill with typical structure for testing compression ratios.

## When to Use

Activate when:
- Testing skill-distiller compression
- Demonstrating realistic token reduction
- Validating protected pattern preservation

## Process

### Step 1: Setup

First, configure the environment:
- Set required variables
- Validate prerequisites
- Initialize state

### Step 2: Execution

Execute the main workflow:
1. Parse input
2. Classify sections
3. Apply compression
4. Output result

### Step 3: Verification

Verify the output:
- Check functionality preservation
- Validate protected patterns
- Confirm token reduction

## Examples

### Example 1: Basic Usage

```bash
/example-skill input.txt
```

Output:
```
Processing input.txt...
Result: success
```

### Example 2: With Options

```bash
/example-skill input.txt --verbose --output=result.txt
```

Output:
```
[VERBOSE] Parsing input.txt
[VERBOSE] Found 15 sections
[VERBOSE] Writing to result.txt
Result: success (15 sections processed)
```

### Example 3: Error Case

```bash
/example-skill nonexistent.txt
```

Output:
```
Error: File not found: nonexistent.txt
Hint: Provide a valid file path
```

## Edge Cases

### Empty Input

When input is empty, return early with warning:
```
Warning: Empty input, nothing to process
```

### Large Files

For files >10MB, process in chunks to avoid memory issues.

### Special Characters

Handle Unicode and special characters gracefully.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--verbose` | `false` | Show detailed output |
| `--output` | stdout | Output file path |
| `--format` | `text` | Output format: text, json, yaml |

## Error Handling

| Error | Recovery |
|-------|----------|
| File not found | Check path, provide valid file |
| Invalid format | Use supported format (text/json/yaml) |
| Memory exceeded | Use smaller input or chunked mode |

## Related

- [Parent Skill](../parent/)
- [Documentation](https://example.com/docs)
