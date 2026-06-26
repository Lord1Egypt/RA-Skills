---
name: FileReadTool
description: "Read file contents with support for text and images. Use when you need to read file contents, inspect code, or analyze images. Supports offset/limit for large files."
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": [] } } }
---

# FileReadTool

Read file contents with support for text files and images.

## When to Use

✅ **USE this skill when:**
- Reading source code files
- Inspecting configuration files
- Analyzing text documents
- Viewing images (jpg, png, gif, webp)
- Reading large files (use offset/limit)

❌ **DON'T use this skill when:**
- Writing or modifying files → use `FileWriteTool` or `FileEditTool`
- Listing directory contents → use `GlobTool` or `exec ls`
- Running commands → use `BashTool`

## Usage

### Read Text File

```bash
# Read entire file
read --path /path/to/file.txt

# Read with offset and limit (for large files)
read --path /path/to/largefile.txt --offset 100 --limit 50
```

### Read Image

```bash
# Read image file (returned as attachment)
read --path /path/to/image.png
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | Path to the file (relative or absolute) |
| `offset` | number | Line number to start reading from (1-indexed) |
| `limit` | number | Maximum number of lines to read |
| `file_path` | string | Alternative path parameter |

## Output

- **Text files**: Output truncated to 2000 lines or 50KB (whichever is hit first)
- **Images**: Returned as MEDIA attachments
- **Large files**: Use offset/limit to read in chunks

## Examples

### Example 1: Read Configuration File

```bash
read --path ./config.json
```

### Example 2: Read Large Log File

```bash
# Read lines 1000-1100
read --path ./logs/app.log --offset 1000 --limit 100
```

### Example 3: Read Full File in Chunks

```bash
# First chunk
read --path ./largefile.txt --offset 1 --limit 2000

# Second chunk
read --path ./largefile.txt --offset 2001 --limit 2000
```

## Integration Notes

This is a core OpenClaw built-in tool. No additional setup required.

## Security Notes

⚠️ **File access is sandboxed:**
- Cannot read files outside workspace without explicit paths
- Sensitive files may be restricted by policy
- Image files are analyzed via vision model
