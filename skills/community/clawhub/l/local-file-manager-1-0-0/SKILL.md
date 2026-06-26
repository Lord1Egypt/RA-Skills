---
name: local-file-manager
description: Read, write, append, and list local files in the session's working directory. Use when you need to persist output to disk, read input files, or manipulate file system safely. Supports text files, JSON, CSV, Markdown.
---

# Local File Manager Skill

This skill provides safe file I/O operations within the session's `cwd`. It is designed for roles that need to store outputs locally (no cloud sync).

## Capabilities

- **Read file**: Get contents of a text file
- **Write file**: Create or overwrite a file
- **Append file**: Add content to existing file
- **List files**: Directory listing with filtering
- **Delete file**: Remove a file (with safety checks)
- **Copy/Move**: Simple file operations

## When to Use

Role needs to:
- Save generated code/analysis to disk
- Read input documents (PDFs, text, etc.)
- Append logs or results
- Create output files in Markdown/JSON/CSV

## Usage

```bash
# Read a file
file-manager --action read --path output.md

# Write content (from stdin or --content)
file-manager --action write --path result.json --content '{"status":"done"}'

# Append to file
file-manager --action append --path log.txt --content "Job completed at $(date)"

# List files in directory
file-manager --action list --dir . --pattern "*.md"

# Create directory
file-manager --action mkdir --dir reports

# Delete file (with confirmation)
file-manager --action delete --path old_file.txt
```

## Safety

- **Sandboxed to cwd**: Cannot access files outside session's working directory
- **Protected files**: Cannot delete files starting with `.` or in `../`
- **Size limit**: Max file size 10MB (configurable)
- **Dry-run support**: `--dry-run` shows what would happen

## Integration with Roles

In role config, enable this skill:

```yaml
plugins:
  allow:
    - local-file-manager
    - doc-parser
```

Then in the role's system prompt, guide usage:

```
When you finish analysis, write the result to a file:
  file-manager --action write --path summary.md --content "$YOUR_MARKDOWN"
```

## Examples

**Researcher saving analysis:**
```bash
file-manager --action write --path analysis_$(date +%Y%m%d).md \
  --content "# Analysis\n\n## Summary\n..." 
```

**Developer saving code:**
```bash
file-manager --action write --path src/main.py --content "$CODE"
```

**Automation appending log:**
```bash
file-manager --action append --path /var/log/automation.log \
  --content "[$(date)] Task completed\n"
```

## Error Handling

- If file doesn't exist for read: returns error code 1
- If path is outside cwd: denied
- If write fails (permission): returns error
- All errors logged to `~/.openclaw/logs/file-manager.log`

## Configuration

Environment variables:
- `FILE_MANAGER_MAX_SIZE`: Max file size in bytes (default 10485760)
- `FILE_MANAGER_LOG`: Path to operation log (default `~/.openclaw/logs/file-manager.log`)
- `FILE_MANAGER_DRY_RUN`: Set to "1" to only simulate operations