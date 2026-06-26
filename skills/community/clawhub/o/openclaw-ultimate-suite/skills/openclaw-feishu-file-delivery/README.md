# OpenClaw Feishu File Delivery

Deliver locally generated files back into Feishu chats as real attachments.

## What It Does

- Detects absolute local file paths in the final reply
- Lets the Feishu adapter upload the actual artifact instead of only sending text
- Works well for office-style deliverables such as `.pptx`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.zip`, `.txt`, and `.md`

## Recommended Pattern

1. Generate the file locally.
2. Write one short caption.
3. Put each absolute file path on its own line.

Example:

```text
已完成，已附上文件：
/absolute/path/to/weekly-review.pptx
/absolute/path/to/weekly-review.pdf
```

## Files

- `SKILL.md` — skill definition
- `skill.json` — metadata for discovery
- `_meta.json` — lightweight publish metadata

## Homepage

[GitHub repository](https://github.com/wd041216-bit/openclaw-feishu-file-delivery)

## 中文说明

中文使用方式与英文说明一致；如果后续需要，也可以单独补一份中文 README。
