---
name: GlobTool
description: "Find files matching glob patterns. Use when you need to search for files by name pattern, list directory contents, or locate specific file types."
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": [] } } }
---

# GlobTool

Find files matching glob patterns.

## When to Use

✅ **USE this skill when:**
- Finding files by name pattern
- Listing directory contents recursively
- Locating specific file types (*.py, *.js, etc.)
- Searching for configuration files
- Building file lists for batch operations

❌ **DON'T use this skill when:**
- Reading file contents → use `FileReadTool`
- Searching inside files → use `GrepTool`
- Running complex find commands → use `BashTool`

## Usage

```bash
# Find all Python files
glob --pattern "*.py"

# Find all test files
glob --pattern "*test*.py" --path "./src"

# List directory contents
glob --pattern "*" --path "/path/to/dir"

# Find files with max depth
glob --pattern "*.md" --max-depth 2
```

## Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `--pattern` | Glob pattern to match (e.g., `*.py`, `**/*.js`) | Yes | - |
| `--path` | Base path to search from | No | `.` |
| `--type` | File type filter: `f` (file), `d` (dir), `l` (link) | No | `f` |
| `--max-depth` | Maximum directory depth to recurse | No | unlimited |
| `--exclude` | Patterns to exclude from results | No | - |

## Glob Patterns

| Pattern | Matches |
|---------|---------|
| `*.py` | All Python files |
| `**/*.js` | All JS files in any subdirectory |
| `src/**/*.ts` | All TS files under src/ |
| `*.md` | All Markdown files |
| `test_*.py` | Files starting with test_ |

## Examples

### Example 1: Find All Python Files

```bash
glob --pattern "*.py"
```

### Example 2: Find Configuration Files

```bash
glob --pattern "*.json" --path "./config"
glob --pattern "*.yaml" --path "./config"
glob --pattern "*.yml" --path "./config"
```

### Example 3: List Directory Contents

```bash
glob --pattern "*" --path "/path/to/dir" --type f
```

### Example 4: Find TypeScript Files in src

```bash
glob --pattern "*.ts" --path "./src" --max-depth 3
```

## Integration with Other Tools

```bash
# Find and read files
files=$(find . -name '*.md' -type f)
for f in $files; do read --path "$f"; done

# Find and edit files
find . -name '*.py' -type f -exec edit --path {} ... \;
```

## Security Notes

⚠️ **Glob restrictions:**
- Searches are limited to workspace by default
- System directories may be excluded
- Symlinks may be followed or ignored based on policy

## Best Practices

1. **Use specific patterns**: Narrow down results with specific extensions
2. **Limit depth**: Use `-maxdepth` with find to avoid deep recursion
3. **Filter results**: Pipe to grep, head, tail for manageable output
4. **Verify before batch operations**: Always check matched files before bulk edits
