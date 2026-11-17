# OCR

Use `POST /ocr/` for an image, screenshot, photograph, or scanned page.

## Request

```json
{
  "image_base64": "<Base64>",
  "language": "mw",
  "image_encoding": "jpg"
}
```

- Default to `mw` for Traditional Mongolian and use `mn` only for Cyrillic.
- Supported encodings are `jpg`, `png`, `bmp`, `webp`, `tif`, `tiff`, and `gif`.
- Keep decoded input at or below 10 MiB.
- Generate Base64 from the file without placing the encoded payload in a shell argument.

Use `scripts/ocr.sh <image> [mw|mn]`.

## Response and chaining

Return `data.text`. If the user also requested translation, pass that value directly into `/translation/`. Do not expose `data.lines`, raw provider data, or the Base64 request.
