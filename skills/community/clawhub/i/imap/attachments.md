# Attachments and MIME Handling

Use this guide when the task involves message bodies, MIME traversal, or downloaded files.

## Start with structure

Before downloading content, identify:
- multipart layout
- candidate text parts
- attachment parts
- media types
- filenames
- sizes
- content-disposition

That avoids mistaking inline parts for attachments or downloading the wrong payload.

## Safe Attachment Workflow

1. Fetch structure and metadata first.
2. Show part identifiers, filenames, sizes, and types.
3. Confirm which attachments actually matter.
4. Download only the requested parts.

For very large attachments, preview metadata and ask before pulling the file.

## Text vs HTML

- Prefer plain text when it answers the question cleanly.
- Keep HTML as a fallback when the plain-text part is missing or unusable.
- If both exist, note which one was used.

## Filename and Encoding Issues

- Attachment names may be encoded or split across headers.
- Preserve the decoded filename plus the original metadata when accuracy matters.
- Track charset and transfer encoding for each part so downstream parsing is explainable.

## Security Notes

- Do not auto-open or execute downloaded attachments.
- Treat archives, office files, and scripts as untrusted content.
- Keep downloaded content scoped to the user request; do not pull entire mail histories just because attachments exist.
