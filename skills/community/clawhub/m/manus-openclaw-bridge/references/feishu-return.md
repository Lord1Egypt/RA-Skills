# Feishu return

## Goal

Return Manus-generated images, documents, or PPTX files back into the current Feishu conversation.

## Recommended flow

1. Submit Manus task.
2. Wait for completion with `scripts/manus_wait_and_collect.py`.
3. Inspect `files[]` in the returned JSON.
4. Send the saved local file paths back through OpenClaw's normal reply/file send mechanism.

## Practical rules

- Prefer sending the downloaded local file instead of a raw Manus CDN URL.
- For images, send the image file directly so the user gets an inline preview.
- For PPTX/PDF/DOCX, send the file and optionally add one short line describing what it is.
- If Manus returns many outputs, send the most likely final artifact first.

## Fallback

If download fails but `task_url` exists:
- tell the user the task completed
- include the task URL
- include the download failure reason if useful

## Notes for OpenClaw implementers

- Keep the reply short.
- Do not dump the entire raw task JSON into chat.
- If there are both text and files, send the file and summarize the text in one sentence.
