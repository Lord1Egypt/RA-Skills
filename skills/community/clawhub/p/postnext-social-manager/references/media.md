# Media

> Safety: upload only files the user asked to attach (images and video). Use a dedicated API key and never echo it. The `postnext` helper refuses other file types.

Upload an image or video, then put the returned **`asset.url`** into a post's `content.media[].url`. The `assetId` is not used by the publish path.

## Upload with the helper

```bash
./postnext upload ./hero.png                    # prints a preview and sends nothing (exit code 3)
./postnext upload ./hero.png --confirm <code>   # only after the user approves; prints the asset URL
```

Or skip the separate upload and pass the file straight to `post` or `schedule` with `--media ./hero.png`. The file is then uploaded only after that command's own confirmation. Either way the preview pins the file by its sha256, so a swapped file needs a fresh approval.

Never upload with raw curl: it skips the preview and `--confirm` step.

## How the helper uploads

| Case | Route | Cap |
|------|-------|-----|
| jpeg, png, webp, gif, mp4 or webm up to 50 MB | 3-step presigned upload (request a URL, PUT the bytes, finalize) | 50 MB |
| larger video (up to 500 MB), or .mov | multipart single upload (the helper adds the account `uniqueId` for you) | 500 MB |

Other file types are refused. Presigned uploads pre-charge storage quota for the declared size, return 413 over 50 MB, and the finalize step checks the bytes against the declared type (415 on a mismatch).

Uploading a remote URL into the media library is not covered by this skill. Either ask the user for a local copy of the file and upload that, or pass the public URL straight to `--media` on `post` or `schedule` (the helper accepts URLs and attaches them as they are).

## Then attach it

```jsonc
"content": { "text": "...", "media": [{ "url": "<asset.url>", "type": "IMAGE" }] }
```
`type` is `IMAGE`, `VIDEO`, or `GIF`. For a multi-image Instagram carousel, verify whether a top-level `mediaType: "CAROUSEL"` is also required (unverified).

## Manage assets

- `GET /api/assets/mine?page=1&limit=50` -> `{success, data, pagination}` (pagination is top-level).
- `GET /api/assets/{assetId}` -> `{success, data}`.

Deleting assets is out of scope for this skill; use the PostNext web app.
