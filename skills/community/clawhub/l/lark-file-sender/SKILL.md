---
name: feishu-file-sender
description: Send files to Feishu/Lark users and groups via the message tool. Use when the user wants to send documents, images, PDFs, or any files through Feishu. Handles file path validation, channel selection, and proper message formatting for seamless file delivery in Feishu conversations.
---

# Feishu File Sender

Send files to Feishu/Lark users and chat groups with proper formatting and error handling.

## When to Use

Use this skill when:
- User wants to send a file via Feishu
- Need to deliver documents, images, PDFs to Feishu contacts
- Transferring generated files (reports, exports, etc.) to Feishu
- Sharing any file through Feishu messaging

## Quick Start

```python
# Basic file send
message action=send filePath="/path/to/file.pdf"

# With custom message
message action=send filePath="/path/to/report.docx" message="Here's the report you requested"
```

## File Types Supported

- Documents: `.pdf`, `.doc`, `.docx`, `.txt`, `.md`
- Spreadsheets: `.xls`, `.xlsx`, `.csv`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Archives: `.zip`, `.rar`, `.tar.gz`
- Code files: `.py`, `.js`, `.html`, `.json`, etc.

## Usage Examples

### Send a Single File

```python
message action=send filePath="/workspace/report.pdf"
```

### Send with Caption

```python
message action=send filePath="/workspace/data.xlsx" message="Q4 sales data"
```

### Send Multiple Files

Send files one by one with context:

```python
for file in files:
    message action=send filePath=file
```

### Send to Specific Target

```python
# To a specific user
message action=send target="user:ou_xxx" filePath="/path/to/file"

# To a specific chat
message action=send target="chat:oc_xxx" filePath="/path/to/file"
```

## Best Practices

1. **Always verify file exists** before sending
2. **Provide context** with the message parameter when helpful
3. **Check file size** - Feishu has limits (typically 100MB-1GB depending on plan)
4. **Use absolute paths** to avoid confusion

## Common Patterns

### After Generating a File

```python
# Generate report
exec command="python generate_report.py"

# Send to user
message action=send filePath="/workspace/output/report.pdf" message="Your report is ready"
```

### Batch File Delivery

```python
# Collect all generated files
files = ["/workspace/file1.pdf", "/workspace/file2.xlsx"]

for i, file in enumerate(files, 1):
    message action=send filePath=file message=f"File {i} of {len(files)}"
```

## Error Handling

Common issues and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Wrong path | Use absolute path with `filePath` |
| Access denied | Permissions | Check file permissions with `ls -la` |
| Too large | File size limit | Compress or split file |
| Channel error | Feishu config | Verify channel is properly configured |

## Tool Reference

### message tool (action=send)

```yaml
action: send
filePath: /absolute/path/to/file    # Required: path to file
message: "Optional caption text"    # Optional: accompanying message
target: "user:xxx" or "chat:xxx"   # Optional: specific recipient
channel: feishu                     # Optional: defaults to current
```

## Related Skills

- `auto-file-sender` - Automatic file sending when files are generated
- `feishu-file-transfer` - Large file transfer via Feishu API

---

*Version: 1.0*  
*Compatible with: OpenClaw v1.x+*  
*Platform: Feishu / Lark*
