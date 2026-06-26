# Obsidian Supported File Formats

Source: https://help.obsidian.md/file-formats

## Native Formats

| Type | Extensions |
|------|-----------|
| Markdown | `.md` |
| Bases | `.base` |
| JSON Canvas | `.canvas` |

## Embeddable Attachments

| Type | Extensions |
|------|-----------|
| Images | `.avif`, `.bmp`, `.gif`, `.jpeg`, `.jpg`, `.png`, `.svg`, `.webp` |
| Audio | `.flac`, `.m4a`, `.mp3`, `.ogg`, `.wav`, `.webm`, `.3gp` |
| Video | `.mkv`, `.mov`, `.mp4`, `.ogv`, `.webm` |
| PDF | `.pdf` |

## Embed Syntax

```markdown
![[image.png]]                   # full size
![[image.png|300]]               # width 300px
![[image.png|300x200]]           # exact w×h
![[document.pdf]]                # full PDF
![[document.pdf#page=5]]         # specific page
![[audio.mp3]]                   # audio player
![[video.mp4]]                   # video player
![[note.md]]                     # embed note
![[note.md#Section]]             # embed section
![[note.md#^block-id]]           # embed block

![alt|300](https://url/image.png)  # external image with resize
```

## External Embeds (iframe)

```html
<iframe src="https://www.youtube.com/embed/VIDEO_ID" width="100%" height="400"></iframe>
```

## Attachment Storage

Place attachments in `assets/` subfolder. Configure in Obsidian:
Settings → Files & Links → Default location for new attachments → "In the folder specified below" → `assets`
