---
name: FileWriteTool
description: "Write content to a file. Creates the file if it doesn't exist, overwrites if it does. Automatically creates parent directories."
metadata: { "openclaw": { "emoji": "✍️", "requires": { "bins": [] } } }
---

# FileWriteTool

Write content to a file. Creates the file if it doesn't exist, overwrites if it does.

## When to Use

✅ **USE this skill when:**
- Creating new files
- Overwriting existing files
- Writing configuration files
- Generating code or documentation
- Saving output from commands

❌ **DON'T use this skill when:**
- Making small edits to existing files → use `FileEditTool`
- Reading files → use `FileReadTool`
- Appending to files → use `BashTool` with `>>`

## Usage

```bash
# Write content to a file
write --path /path/to/file.txt --content "Hello, World!"

# Write multi-line content
write --path /path/to/script.py --content "def main():\n    print('Hello')"

# Create nested directories automatically
write --path /path/to/nested/dir/file.txt --content "Content"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | Path to the file (relative or absolute) |
| `content` | string | Content to write to the file |
| `file_path` | string | Alternative path parameter |

## Features

- **Auto-create directories**: Parent directories are created automatically
- **Overwrite mode**: Existing files are completely overwritten
- **UTF-8 encoding**: All files are written as UTF-8 text

## Examples

### Example 1: Create New File

```bash
write --path ./notes.txt --content "Meeting notes for today..."
```

### Example 2: Write Python Script

```bash
write --path ./scripts/hello.py --content "#!/usr/bin/env python3\nprint('Hello, World!')"
```

### Example 3: Write JSON Configuration

```bash
write --path ./config.json --content '{"name": "myapp", "version": "1.0.0"}'
```

### Example 4: Create Nested Directory Structure

```bash
write --path ./src/components/Button.tsx --content "export const Button = () => {}"
```

## Integration Notes

This is a core OpenClaw built-in tool. No additional setup required.

## Security Notes

⚠️ **File write restrictions:**
- Cannot overwrite files outside workspace without explicit paths
- Some system files may be protected
- Large files may be truncated

## Best Practices

1. **Use FileEditTool for small changes**: If you only need to change a few lines, use `FileEditTool` instead
2. **Verify before overwriting**: Check if the file exists and contains important data
3. **Use absolute paths for clarity**: Especially when working with nested structures
