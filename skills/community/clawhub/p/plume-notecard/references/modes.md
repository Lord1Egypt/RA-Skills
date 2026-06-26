# Notecard Modes and Parameters

## mode (Scenario Type)

| mode | Description | Required Parameters |
|------|-------------|---------------------|
| `article` | Convert topic or long-form text to notecard. `--article` can carry user-provided long text, or Agent-expanded/ planned complete content based on topic | `--article` |
| `reference` | Generate notecard based on reference image | `--reference-type` + `--reference-image-urls` |

> Note: Script layer still supports `--mode topic --topic`, but skill no longer recommends it. All text-based notecard requests should go through `article`.

## reference_type (Reference Image Sub-scenario)

Only for `mode=reference`.

| reference_type | Description | Required Parameters | Typical Scenario |
|---------------|-------------|---------------------|------------------|
| `sketch` | Hand-drawn/sketch to notecard | `--reference-image-urls` | User uploads hand-drawn, whiteboard photo |
| `style_transfer` | Imitate reference image style | `--reference-image-urls` + (`--reference-topic` or `--reference-article`) | User uploads existing notecard as style reference |
| `product_embed` | Product/character embedded in notecard | `--reference-image-urls` + `--reference-article` | User uploads product/character image and provides selling points/intro text; differs from style_transfer (style_transfer's reference is a card style sample, product_embed's reference is the product/character itself to be embedded) |
| `content_rewrite` | Rewrite text content in reference image | `--reference-image-urls` + (`--reference-article` or `--reference-topic`) | User uploads notecard, only changing text |

> Note: In reference mode, if caller mistakenly puts content in `--article`, script will auto-map to `--reference-article`. But recommended to pass `--reference-article` directly.

## child_reference_type (Batch Mode Sub-task Strategy)

Only valid when `count >= 2`.

| child_reference_type | Description | Applicable Scenario |
|---------------------|-------------|---------------------|
| `style_transfer` (default) | Each image generated independently, style roughly consistent but layout may vary | Series with varied content |
| `content_rewrite` | Strictly maintain base image's layout and style, only replace text content | Coherent paginated series |

## action (Retry Action)

| action | Description | Requires `--last-task-id` |
|--------|-------------|--------------------------|
| `repeat_last_task` | Regenerate (content and style unchanged) | Yes |
| `switch_style` | Switch style retry (content unchanged) | Yes |
| `switch_content` | Switch content retry (style unchanged) | Yes |
| `switch_all` | Both content and style switched | Yes |

### Additional Rules for Reference Mode Retry

- Normal text mode (article/topic) retry: pass `--action` + `--last-task-id` + `--article`
- Reference mode retry: also need `--mode reference` + `--reference-type` + `--reference-image-urls`
- `action=switch_content`: must pass `--article` as new content
- `action=switch_style`: must pass `--article` to preserve original content context
- `reference_type=content_rewrite` / `style_transfer` and `action=switch_style`: executor will downgrade to `switch_all` (style from reference image)

## Slide Deck Mode (Deck Mode)

Generate a complete slide deck style notecard set, where each page has different page roles (cover, table of contents, content page, back cover), but shares a unified visual style system.

Activated via `--deck-mode` flag. Mutually exclusive with batch mode (`--count >= 2`) and reference image mode.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--deck-mode` | Enable slide deck notecard generation | `false` |
| `--page-count` | Total pages, including cover and back cover (3-10) | `5` |

Features:
- Default ratio: `16:9` (landscape), differs from single image `3:4`
- Page roles: cover → table of contents (optional) → content pages (1-N) → back cover
- Style consistency from template's shared visual style system (not reference image)
- Does not support reference image mode
- Mutually exclusive with batch mode (`count >= 2`)
- Supports `--mode article` and `--mode topic`

## Other Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--style-hint` | Style keyword (max 10 chars), e.g. "minimalist", "cyberpunk" | None |
| `--aspect-ratio` | Image ratio: `3:4` / `4:3` / `1:1` / `16:9` / `9:16` | `3:4` (deck defaults to `16:9`) |
| `--locale` | Text language: `zh-CN` / `en-US` / `ja-JP` etc | `zh-CN` |
| `--count` | Generation count, 1-10, >=2 triggers batch mode | `1` |
| `--deck-mode` | Enable slide deck generation (mutually exclusive with batch) | `false` |
| `--page-count` | Slide deck page count, 3-10 (only when `--deck-mode`) | `5` |
| `--template-id` | Specify template ID, skip auto-match | None |
| `--article-summary` | Article summary (optional when mode=article) | None |
