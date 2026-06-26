# Supported Source Types

## Source type mapping

| Type     | Telegram Input            | CLI Command                           | Notes                      |
|----------|--------------------------|---------------------------------------|----------------------------|
| url      | Paste article link       | `source add "<url>"`                  | Any web article URL        |
| youtube  | Paste YouTube link       | `source add "<youtube_url>"`          | YouTube video URL          |
| text     | Type or paste text       | `source add "./temp.txt"`             | Save to .txt first, then add |
| pdf      | Upload .pdf file         | `source add "./file.pdf"`             | PDF document               |
| word     | Upload .docx file        | `source add "./file.docx"`            | Word document              |
| audio    | Upload audio file        | `source add "./file.mp3"`             | Audio recording            |
| image    | Upload image file        | `source add "./file.png"`             | Image with text content    |
| drive    | Paste Google Drive link  | `source add-drive <file_id> "<title>"`| Google Drive shared file   |

## Auto-detection rules

When the user sends content via Telegram, detect the source type:

1. **URL pattern** (`https?://...`):
   - Contains `youtube.com` or `youtu.be` → type: `youtube`
   - Contains `drive.google.com` or `docs.google.com` → type: `drive`
   - Otherwise → type: `url`
2. **File attachment**:
   - `.pdf` extension → type: `pdf`
   - `.docx` / `.doc` extension → type: `word`
   - `.mp3` / `.wav` / `.m4a` / `.ogg` extension → type: `audio`
   - `.jpg` / `.jpeg` / `.png` / `.webp` extension → type: `image`
3. **Plain text** (no URL, no file) → type: `text`

## CLI notes

- `source add` auto-detects content type (URL vs file path)
- Plain text must be saved to a `.txt` file first — CLI does not support stdin
- Google Drive sources use `source add-drive <file_id> "<title>"`
- After adding, use `source list` to verify sources were imported
