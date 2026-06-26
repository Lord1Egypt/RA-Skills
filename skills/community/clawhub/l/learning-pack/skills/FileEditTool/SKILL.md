---
name: FileEditTool
description: "Edit a file by replacing exact text. The oldText must match exactly (including whitespace). Use this for precise, surgical edits."
metadata: { "openclaw": { "emoji": "🔧", "requires": { "bins": [] } } }
---

# FileEditTool

Edit a file by replacing exact text. The oldText must match exactly (including whitespace).

## When to Use

✅ **USE this skill when:**
- Making small, precise changes to files
- Fixing typos or bugs
- Updating configuration values
- Refactoring code snippets
- Surgical text replacements

❌ **DON'T use this skill when:**
- Creating new files → use `FileWriteTool`
- Reading files → use `FileReadTool`
- Rewriting entire files → use `FileWriteTool`
- Complex multi-location edits → consider multiple edit calls

## Usage

```bash
# Replace exact text
edit --path /path/to/file.txt --oldText "old text" --newText "new text"

# Alternative parameter names
edit --path /path/to/file.txt --old_string "old text" --new_string "new text"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | string | Path to the file (relative or absolute) |
| `oldText` | string | Exact text to find and replace (must match exactly) |
| `newText` | string | New text to replace the old text with |
| `file_path` | string | Alternative path parameter |
| `old_string` | string | Alternative oldText parameter |
| `new_string` | string | Alternative newText parameter |

## Important Notes

⚠️ **Exact Match Required**: The `oldText` must match exactly, including:
- Whitespace (spaces, tabs, newlines)
- Indentation
- Line endings

## Examples

### Example 1: Fix a Typo

```bash
edit --path ./README.md --oldText "funtion" --newText "function"
```

### Example 2: Update Version Number

```bash
edit --path ./package.json --oldText '"version": "1.0.0"' --newText '"version": "1.0.1"'
```

### Example 3: Replace Code Snippet

```bash
edit --path ./src/app.py --oldText "def greet():\n    return 'Hello'" --newText "def greet():\n    return 'Hello, World!'"
```

### Example 4: Update Configuration

```bash
edit --path ./config.yaml --oldText "debug: false" --newText "debug: true"
```

## Tips for Success

1. **Read the file first**: Use `FileReadTool` to see the exact content
2. **Copy exact text**: Include exact whitespace and indentation
3. **Use small edits**: One change per edit call for reliability
4. **Test after editing**: Verify the file still works correctly

## Integration Notes

This is a core OpenClaw built-in tool. No additional setup required.

## Security Notes

⚠️ **Edit restrictions:**
- Cannot edit files outside workspace without explicit paths
- Some system files may be protected
- Failed matches do not modify the file

## Troubleshooting

### "Text not found" Error

If the edit fails because the text wasn't found:
1. Re-read the file to verify exact content
2. Check for whitespace differences
3. Ensure line endings match (LF vs CRLF)
4. Try a smaller, more specific text segment
