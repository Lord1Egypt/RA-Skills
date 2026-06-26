---
name: nexus-ciba-wechat
description: generate shareable html and png cards from the ciba or iciba daily sentence api. use when the user asks for 词霸每日一句, iciba, ciba, open.iciba.com/dsapi, daily english sentence cards, magazine torn-paper cards, friends circle or moments poster layouts, postcard horizontal cards, qr codes for tts pronunciation audio, multi-template html customization, or playwright rendering of these cards to png.
---

# Nexus Ciba Wechat

## Overview

Use this skill to create polished HTML and PNG cards from the 词霸每日一句 API at `https://open.iciba.com/dsapi/`. The bundled renderer supports multiple HTML templates, including a vertical friends-circle card and a horizontal postcard-style card, with QR codes that encode the API `tts` audio URL.

## Default workflow

1. Use `scripts/render_iciba_card.py` unless the user explicitly asks for hand-written HTML only.
2. Fetch the daily JSON from `https://open.iciba.com/dsapi/` by default.
3. Prefer the API image fields for the hero image in this order: `picture`, `picture2`, `picture3`, `picture4`.
4. Only generate the local fallback image if the API cannot be reached or all picture downloads fail.
5. Encode `tts` into the QR code. Do not encode the page URL unless the user explicitly asks.
6. Choose the template requested by the user, or use `moments_vertical` by default.
7. Render the selected HTML template to PNG with Playwright.
8. Return links to the generated PNG and HTML. Also mention whether the card used the API picture or the generated fallback.

## Script usage

Run from the skill directory or pass the script path directly:

```bash
python scripts/render_iciba_card.py --output-dir /mnt/data/iciba-card
```

List available templates:

```bash
python scripts/render_iciba_card.py --list-templates
```

Render the default vertical friends-circle card:

```bash
python scripts/render_iciba_card.py \
  --template moments_vertical \
  --output-dir /mnt/data/iciba-card
```

Render the horizontal postcard card:

```bash
python scripts/render_iciba_card.py \
  --template postcard_horizontal \
  --output-dir /mnt/data/iciba-postcard
```

Useful options:

```bash
python scripts/render_iciba_card.py \
  --template postcard_horizontal \
  --output-dir /mnt/data/iciba-postcard \
  --width 1200 \
  --height 760 \
  --api-url https://open.iciba.com/dsapi/
```

For testing or reproducibility without live network access, pass a JSON file:

```bash
python scripts/render_iciba_card.py --input-json /mnt/data/iciba.json --output-dir /mnt/data/iciba-card
```

Expected outputs in the output directory:

- `<output_stem>.html`
- `<output_stem>.png`
- `<output_stem>_data.json`
- `hero_source.txt`

Default output stems:

- `moments_vertical` -> `iciba_moments_card`
- `postcard_horizontal` -> `iciba_postcard_horizontal`

## Template system

HTML is separated from Python and stored in `templates/`:

- `templates/moments_vertical.html`: 9:16 friends-circle card, image above and text below.
- `templates/postcard_horizontal.html`: horizontal postcard-style card, photo left and message/stamp area right.

Templates use simple replacement tokens rather than a templating dependency. Supported tokens include:

- `[[WIDTH]]`, `[[HEIGHT]]`, `[[TEMPLATE_NAME]]`
- `[[CAPTION]]`, `[[CONTENT]]`, `[[NOTE]]`, `[[TRANSLATION]]`, `[[DATELINE]]`
- `[[ISSUE_DAY]]`, `[[ISSUE_TEXT]]`, `[[QUOTE_SIZE]]`
- `[[HERO_URI]]`, `[[HERO_ALT]]`, `[[HERO_SOURCE]]`, `[[HERO_FIELD]]`, `[[HERO_URL]]`
- `[[QR_URI]]`, `[[TTS_URL]]`, `[[STATUS]]`

To add a new template, create a new HTML file under `templates/`, add an entry to `TEMPLATE_CONFIG` in `scripts/render_iciba_card.py`, then test with `--template <name>`.

## Layout rules

For `moments_vertical`:

- Use a 9:16 canvas, default `540 x 960` CSS pixels.
- Keep the image in the top section, not as a full-card background.
- Keep the text in a separate lower paper section.
- Put the QR code in the lower-right of the text section.

For `postcard_horizontal`:

- Use a horizontal canvas, default `1200 x 760` CSS pixels.
- Keep the hero image on the left and the postcard message area on the right.
- Include a postcard cue such as `POST CARD`, address lines, a stamp area, and a QR voice stamp.
- Keep the quote and translation readable; reduce quote size for long sentences.

For all templates:

- Preserve the magazine or paper aesthetic through clipped edges, paper texture, subtle shadows, tape accents, and warm cream tones.
- Keep text readable over decoration.
- Put the QR code payload on `tts`, not on the HTML page URL, unless explicitly requested otherwise.

## Data mapping

Use these fields from the API:

- `caption` -> label, default `词霸每日一句`
- `content` -> main English quote
- `note` -> Chinese translation
- `translation` -> small source line, default `新版每日一句`
- `dateline` -> displayed date and issue badge
- `tts` -> QR code payload
- `picture`, `picture2`, `picture3`, `picture4` -> image candidates, in that priority order

See `references/iciba-api-fields.md` for more details.

## Path separator behavior

The Python renderer keeps `pathlib.Path` for real filesystem operations, but formats logged and serialized output paths with the native OS separator. Windows uses `\`; Linux, macOS, and other POSIX-like systems use `/`. The generated data JSON includes `_path_separator` and `_output_dir` for debugging.

## Handling failures

If the API fetch fails, use the built-in fallback data and clearly state that the run used fallback data. If the API returns text but image download fails, still use the API text and `tts`, but use the generated fallback image. Do not claim that the visible image came from an API picture unless `hero_source.txt` says `api_picture` and includes the selected picture field and URL.
