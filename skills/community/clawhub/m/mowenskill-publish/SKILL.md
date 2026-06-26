---
name: mowen-note-publisher
description: Publish, edit, or configure notes on Mowen (墨问) via Open API. Use when user mentions 墨问, mowen, 发布笔记, publish note, or wants to create social-media-style notes with rich text and images.
dependencies: "python>=3"
---

# 墨问笔记发布 (Mowen Note Publisher)

## Overview

Publish rich-text notes (text, images, formatting) to 墨问 via its Open API. This skill covers three operations: **creating** new notes, **editing** existing notes (API-created only), and **modifying note settings** (privacy, sharing, expiration). A Python script (`scripts/publish_note.py`) handles all API calls, image uploads, and NoteAtom construction with zero third-party dependencies.

## Prerequisites

- **API Key**: Obtain from 墨问小程序 → 我的 → 设置 → 开放平台 → 创建 API Key
- **Environment**: Set `MOWEN_API_KEY` environment variable, or pass via `--api-key` argument
- **Python 3**: Required for running the publish script (macOS has it pre-installed)

## Workflow Decision Tree

```
User Request
    │
    ├── "发布/创建笔记" or "publish note"
    │   └── ACTION: create
    │       ├── Has images? → Upload images first (see Image Handling)
    │       ├── Build input JSON with paragraphs, tags, autoPublish
    │       └── Run: publish_note.py --action create
    │
    ├── "编辑/修改笔记内容" or "edit note"
    │   └── ACTION: edit (requires noteId from previous create)
    │       ├── ⚠️ Only API-created notes can be edited
    │       ├── Build input JSON with new paragraphs
    │       └── Run: publish_note.py --action edit --note-id <ID>
    │
    └── "修改笔记设置/隐私" or "change note settings"
        └── ACTION: settings (requires noteId)
            └── Run: publish_note.py --action settings --note-id <ID> --privacy <N>
```

## Creating a Note (Step by Step)

### 1. Gather Content from User

Collect the note content. Identify:
- Text paragraphs (plain text or rich text with bold/highlight/links)
- Images (local file paths or URLs)
- Tags (optional, max 10, each ≤ 30 chars)
- Whether to auto-publish (default: draft)
- Privacy setting (default: public)

### 2. Prepare Input JSON

Build a JSON object following this schema:

```json
{
  "paragraphs": [
    "Plain text paragraph",
    [{"text": "Bold text", "bold": true}, " and normal text"],
    {"type": "heading", "level": 1, "text": "Title"},
    {"type": "image", "src": "https://example.com/photo.jpg"},
    {"type": "image", "src": "/path/to/local/photo.jpg", "width": 1080, "height": 720},
    {"type": "blockquote", "text": "A quote"},
    {"type": "bulletList", "items": ["Item 1", "Item 2"]},
    {"type": "orderedList", "items": ["First", "Second"]}
  ],
  "tags": ["tag1", "tag2"],
  "autoPublish": true,
  "privacyType": 1
}
```

**Paragraph types:**

| Type | Format | Description |
|------|--------|-------------|
| Plain text | `"string"` | Simple text paragraph |
| Rich text | `[{...}, ...]` | Array of text items with optional `bold`, `highlight`, `link` |
| Heading | `{"type":"heading", "level":1, "text":"..."}` | h1-h6 heading |
| Image | `{"type":"image", "src":"..."}` | Image (URL, local path, or fileId) |
| Quote | `{"type":"blockquote", "text":"..."}` or `{"type":"quote", "text":"..."}` | Block quote |
| Bullet list | `{"type":"bulletList", "items":["..."]}` | Unordered list |
| Ordered list | `{"type":"orderedList", "items":["..."]}` | Numbered list |
| Raw node | `{"type":"raw", "node":{...}}` | Direct NoteAtom node passthrough |

**Privacy types:** `public` = public, `private` = self-only, `rule` = custom rules (with noShare/expireAt)

### 3. Save Input and Run Script

Save the JSON to a temporary file and execute:

```bash
python {SKILL_DIR}/scripts/publish_note.py --action create --input /tmp/note_input.json
```

Or pipe directly via stdin:

```bash
echo '<json>' | python {SKILL_DIR}/scripts/publish_note.py --action create
```

The script outputs a JSON result with `noteId` on stdout. **Save this noteId** — it is needed for subsequent edit or settings operations.

### 4. Report Result

Inform the user of the created note's ID and status (draft vs published).

## Editing a Note

> ⚠️ **Limitation**: Only notes created via the API can be edited. Notes created in the 墨问 mini-program cannot be edited through this API.

To edit, provide the `noteId` (from a previous create) and new content:

```bash
python {SKILL_DIR}/scripts/publish_note.py --action edit --note-id <NOTE_ID> --input /tmp/note_edit.json
```

The input JSON format is identical to creation (the `paragraphs` field). The entire note content will be **replaced**.

## Modifying Note Settings

To change privacy, sharing, or expiration settings:

```bash
# Set to private
python {SKILL_DIR}/scripts/publish_note.py --action settings --note-id <NOTE_ID> --privacy private

# Set to public
python {SKILL_DIR}/scripts/publish_note.py --action settings --note-id <NOTE_ID> --privacy public

# Set custom rule: forbid sharing with expiration
python {SKILL_DIR}/scripts/publish_note.py --action settings --note-id <NOTE_ID> --privacy rule --no-share --expire-at 1735689600
```

## Image Handling

The script automatically handles images found in `paragraphs`:

- **URL images** (`http://` or `https://`): Uploaded via remote upload API (< 30MB)
- **Local file paths**: Uploaded via local upload API (< 50MB, formats: gif/jpeg/jpg/png/webp)
- **Existing fileId**: Passed through directly (no upload needed)

Image upload is automatic — simply include image entries in the `paragraphs` array and the script handles the rest. Optionally provide `width` and `height` for better rendering.

Rate limiting (1 req/sec) is automatically enforced between API calls.

## API Reference

For complete API documentation including endpoint details, NoteAtom structure specification, request/response examples, and error codes, refer to:

📄 `references/mowen_api.md`

Key search patterns for the reference file:
- `## 1. 笔记创建` — Create endpoint details
- `## 2. 笔记编辑` — Edit endpoint details
- `## 3. 笔记设置` — Settings endpoint details
- `## 4. NoteAtom 结构定义` — Full NoteAtom schema with all node types
- `## 5. 图片上传` — Image upload (local + remote) procedures
- `## 7. 限频与配额汇总` — Rate limits and daily quotas

## Common Use Cases

### Publish a simple text note

```json
{
  "paragraphs": [
    "今天天气真好，适合出门散步 ☀️"
  ],
  "tags": ["日常", "心情"],
  "autoPublish": true
}
```

### Publish a note with images and formatting

```json
{
  "paragraphs": [
    {"type": "heading", "level": 1, "text": "周末探店记录"},
    "今天去了一家超棒的咖啡店！",
    {"type": "image", "src": "https://example.com/coffee.jpg"},
    [{"text": "拿铁", "bold": true}, "味道超赞，推荐指数 ⭐⭐⭐⭐⭐"],
    {"type": "image", "src": "/Users/me/photos/cake.jpg", "width": 1080, "height": 1080},
    {"type": "blockquote", "text": "生活需要一点甜"},
    {"type": "bulletList", "items": ["环境优雅", "咖啡好喝", "甜品精致"]}
  ],
  "tags": ["探店", "咖啡", "美食"],
  "autoPublish": true
}
```

### Edit a previously created note

```bash
# Original creation returned noteId = "note_abc123"
python publish_note.py --action edit --note-id note_abc123 --input updated_content.json
```

### Make a note private

```bash
python publish_note.py --action settings --note-id note_abc123 --privacy private
```
