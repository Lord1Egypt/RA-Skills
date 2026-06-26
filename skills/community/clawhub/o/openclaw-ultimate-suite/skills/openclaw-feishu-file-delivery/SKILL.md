---
name: feishu-file-delivery
homepage: https://github.com/wd041216-bit/openclaw-feishu-file-delivery
description: Deliver locally generated office files back into Feishu chats as real attachments. Use when a task creates a .pptx, .pdf, .docx, .xlsx, .csv, .zip, .txt, or .md file for a Feishu user.
---

# Feishu File Delivery

Use this skill whenever you generate a local artifact for a Feishu chat.

## Goal

Make Feishu receive the actual file attachment, not just a sentence saying the file exists.

## Delivery Contract

1. Save the artifact to a real local file first.
2. In the final Feishu reply, write a short caption or summary.
3. Then place each artifact's absolute local path on its own line with no bullets and no markdown link wrapper.
4. For multiple files, use one absolute path per line.

Example:

```text
已完成，已附上文件：
/absolute/path/to/weekly-review.pptx
/absolute/path/to/weekly-review.pdf
```

## Rules

- Prefer absolute paths over relative paths.
- Do not say only "文件已生成" without the path.
- When the artifact is the main deliverable, always include the path in the final reply.
- Keep the caption short so the file path lines stay easy for the Feishu adapter to detect.
- This is especially important for `.pptx`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.zip`, `.txt`, and `.md`.

## Channel Note

OpenClaw's Feishu outbound adapter can auto-upload supported local files when their absolute paths appear in the outgoing reply text.
