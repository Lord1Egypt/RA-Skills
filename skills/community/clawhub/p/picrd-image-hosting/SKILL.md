---
name: picrd-image-hosting
description: "Free image hosting via picrd.com — upload screenshots, diagrams, and image files to get permanent, embeddable URLs. No account required. Supports PNG, JPEG, WebP, and GIF up to 10 MB. Perfect for free image hosting, free hosting, image hosting, file hosting, file share, and image host needs."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "\U0001F5BC"
    homepage: https://picrd.com/docs
---

# picrd.com — Free Image Hosting

Upload images to [picrd.com](https://picrd.com) and get back permanent, embeddable URLs.
No API key required. No account needed. Images are served from a CDN at `i.picrd.com`.

## When to use this skill

- You need to share a screenshot, diagram, or generated image via a public URL.
- You want to embed an image in a GitHub issue, PR, markdown doc, or chat message.
- You need free image hosting with permanent links and no sign-up.
- You are working with file hosting, file sharing, or image hosting tasks.

## Supported formats

| Format | Max size |
|--------|----------|
| PNG    | 10 MB    |
| JPEG   | 10 MB    |
| WebP   | 10 MB    |
| GIF    | 10 MB    |

## Rate limits

- **60 uploads per hour** per IP address.
- Read/download endpoints are not rate limited.

---

## Upload a single image

**Endpoint:** `POST https://picrd.com/api/upload`
**Content-Type:** `multipart/form-data`

### Required field

| Field  | Description                              |
|--------|------------------------------------------|
| `file` | The image file (PNG, JPEG, WebP, or GIF) |

### Optional fields

| Field         | Description                                          | Default    |
|---------------|------------------------------------------------------|------------|
| `visibility`  | `"unlisted"` or `"public"`                           | `unlisted` |
| `ttl_seconds` | Auto-delete after this many seconds (omit = permanent)| permanent  |
| `album_id`    | Add the image to an existing album                   | none       |

### curl command

```bash
curl -s -F "file=@/path/to/image.png" -F "visibility=unlisted" https://picrd.com/api/upload
```

### Example response (HTTP 200)

```json
{
  "image_id": "Ab3xK9xQ2Lm",
  "page_url": "https://picrd.com/Ab3xK9xQ2Lm",
  "image_url": "https://i.picrd.com/images/Ab3xK9xQ2Lm.png",
  "delete_url": "https://picrd.com/delete/<token>",
  "expires_at": null
}
```

### What to do with the response

1. Use `image_url` to embed the image in markdown: `![description](image_url)`
2. Use `page_url` to link to the image's landing page.
3. **Save `delete_url` somewhere safe** — it is a single-use secret URL and cannot be retrieved later.

---

## Create an album

Group multiple images into an album.

**Endpoint:** `POST https://picrd.com/api/albums`

```bash
curl -s -X POST https://picrd.com/api/albums
```

### Example response (HTTP 200)

```json
{
  "album_id": "J82Lm9Qp2X1",
  "album_url": "https://picrd.com/a/J82Lm9Qp2X1"
}
```

Then pass the `album_id` in subsequent upload requests:

```bash
curl -s -F "file=@/path/to/image.png" -F "album_id=J82Lm9Qp2X1" https://picrd.com/api/upload
```

---

## List album images

**Endpoint:** `GET https://picrd.com/api/albums/<album_id>`

```bash
curl -s https://picrd.com/api/albums/J82Lm9Qp2X1
```

### Example response (HTTP 200)

```json
{
  "album_id": "J82Lm9Qp2X1",
  "images": [
    {
      "image_id": "Ab3xK9xQ2Lm",
      "page_url": "https://picrd.com/Ab3xK9xQ2Lm",
      "image_url": "https://i.picrd.com/images/Ab3xK9xQ2Lm.png"
    }
  ]
}
```

---

## Error handling

| HTTP status | Meaning                                         | Action                                      |
|-------------|--------------------------------------------------|---------------------------------------------|
| 400         | Invalid file type, file too large, or bad params | Check file format is PNG/JPEG/WebP/GIF and ≤ 10 MB |
| 429         | Rate limited                                     | Wait and retry — limit is 60 uploads/hour   |

If the upload fails with a 400 error due to file size, try compressing or resizing the image first:

```bash
# macOS — resize to max 1920px wide using sips
sips --resampleWidth 1920 /path/to/image.png --out /path/to/resized.png

# Linux — resize using ImageMagick
convert /path/to/image.png -resize 1920x /path/to/resized.png
```

Then retry the upload with the resized file.

---

## Workflow: screenshot → upload → embed

A common end-to-end workflow:

1. **Capture a screenshot** (using whatever tool is available).
2. **Upload it:**
   ```bash
   curl -s -F "file=@screenshot.png" -F "visibility=unlisted" https://picrd.com/api/upload
   ```
3. **Parse the JSON response** to extract `image_url`.
4. **Embed in markdown:**
   ```markdown
   ![Screenshot](https://i.picrd.com/images/Ab3xK9xQ2Lm.png)
   ```
5. **Store the `delete_url`** if the image may need to be removed later.

## Important notes

- Images uploaded as `unlisted` are not listed publicly but are accessible if someone has the URL.
- The `delete_url` is a **one-time secret**. Store it immediately — it cannot be recovered.
- Image URLs at `i.picrd.com` are permanent and served with long cache headers.
- This service is free with no account required — do not upload sensitive or private data.
