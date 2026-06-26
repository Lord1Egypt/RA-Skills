---
name: GrepTool
description: "Search for patterns in files using grep. Use when you need to find text patterns, search codebases, or locate specific content across multiple files."
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["grep"] } } }
---

# GrepTool

Search for patterns in files using grep.

## When to Use

✅ **USE this skill when:**
- Finding text patterns in files
- Searching codebases for function/class names
- Locating specific content across multiple files
- Finding TODO/FIXME comments
- Searching logs for errors

❌ **DON'T use this skill when:**
- Reading single file contents → use `FileReadTool`
- Complex pattern matching → consider `exec` with advanced grep
- Binary file search → use specialized tools

## Usage

```bash
# Basic search
grep --pattern "pattern" --path "file.txt"

# Recursive search
grep --pattern "pattern" --path "./src" --recursive

# Search with line numbers
grep --pattern "pattern" --path "file.txt" --line-number

# Case insensitive
grep --pattern "pattern" --path "file.txt" --ignore-case

# Search specific file types
grep --pattern "pattern" --path "." --recursive --include "*.py"
```

## Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `--pattern` | Text pattern to search for (supports regex with -E) | Yes | - |
| `--path` | File or directory path to search | Yes | - |
| `--recursive` | Search recursively through directories | No | false |
| `--line-number` | Show line numbers in output | No | false |
| `--ignore-case` | Case insensitive search | No | false |
| `--include` | Only search files matching pattern (e.g., `*.py`) | No | - |
| `--exclude` | Exclude files matching pattern | No | - |
| `--count` | Only show count of matches | No | false |
| `--context` | Show N lines of context around matches | No | 0 |

## Common Options

| Option | Description |
|--------|-------------|
| `-r` | Recursive search |
| `-n` | Show line numbers |
| `-i` | Case insensitive |
| `-l` | Show only filenames |
| `-c` | Count matches |
| `-v` | Invert match |
| `--include` | Include files matching pattern |
| `--exclude` | Exclude files matching pattern |

## Examples

### Example 1: Find Function Definition

```bash
grep --pattern "def main" --path "." --recursive --line-number --include "*.py"
```

### Example 2: Find TODO Comments

```bash
grep --pattern "TODO" --path "." --recursive --line-number --include "*.ts"
grep --pattern "TODO" --path "." --recursive --line-number --include "*.tsx"
```

### Example 3: Search for Error Patterns

```bash
grep --pattern "error|exception|fail" --path "logs/app.log" --ignore-case
```

### Example 4: Find Import Statements

```bash
grep --pattern "^import|^from" --path "src/" --line-number --include "*.py"
```

### Example 5: Count Occurrences

```bash
grep --pattern "pattern" --path "file.txt" --count
```

## Advanced Patterns

### Example 6: Regex Search

```bash
# Find email addresses
grep --pattern "[a-z]+@[a-z]+\.[a-z]+" --path "file.txt"

# Find version numbers
grep --pattern "v[0-9]+\.[0-9]+\.[0-9]+" --path "package.json"
```

### Example 7: Context Lines

```bash
# Show 3 lines before and after match
grep --pattern "pattern" --path "file.txt" --context 3

# Show 2 lines before
grep --pattern "pattern" --path "file.txt" --context 2

# Show 5 lines after
grep --pattern "pattern" --path "file.txt" --context 5
```

## Integration with Other Tools

```bash
# Grep and read matching files
grep -rl 'pattern' . | xargs -I {} read --path {}

# Grep and edit
grep -rn 'old_text' --include='*.py' . 
# Then use FileEditTool for each result
```

## Security Notes

⚠️ **Search restrictions:**
- Searches limited to accessible directories
- Large result sets may be truncated
- Binary files may cause issues

## Best Practices

1. **Use specific patterns**: Narrow down with file type filters
2. **Escape special characters**: Use quotes around patterns
3. **Limit scope**: Use --include to focus on relevant files
4. **Use -n for context**: Line numbers help locate matches
