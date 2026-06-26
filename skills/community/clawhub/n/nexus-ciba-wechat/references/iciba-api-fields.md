# Iciba API fields

The default endpoint is `https://open.iciba.com/dsapi/` and usually returns JSON with these useful fields:

- `sid`: sentence id.
- `tts`: mp3 pronunciation URL. Use this as the QR code payload.
- `content`: English daily sentence. Use this as the main quote.
- `note`: Chinese translation. Use this below the English quote.
- `translation`: source/version label such as `新版每日一句`.
- `picture`, `picture2`, `picture3`, `picture4`: image candidates. Prefer `picture`, then `picture2`, then `picture3`, then `picture4` for the card hero image.
- `caption`: title label, commonly `词霸每日一句`.
- `dateline`: date in `YYYY-MM-DD` format.

Renderer behavior:

1. Fetch API JSON unless `--input-json` is provided.
2. Merge missing fields with fallback data.
3. Download the first available picture candidate using the priority `picture -> picture2 -> picture3 -> picture4`.
4. If all picture downloads fail, generate a warm illustrated fallback image.
5. Generate a QR code from `tts`.
6. Load the selected HTML file from `templates/` and replace tokens.
7. Render HTML to PNG with Playwright.

Template-related generated debug fields:

- `_template`: selected template name.
- `_hero_source`: `api_picture` or `generated_fallback`.
- `_hero_field`: selected API image field such as `picture`, or `fallback`.
- `_hero_url`: selected image URL when available.
- `_picture_priority`: the image priority list.
- `_path_separator`: `\\` on Windows or `/` elsewhere.
- `_output_dir`: output directory formatted for the current OS.
