---
name: html-mender
description: HTML Mender is a visual editor for local or saved `.html` files only, including HTML-based PPT/deck pages, AI-generated slide HTML, and saved one-page presentation HTML. Use this skill when the user provides a local/saved HTML file and wants visual edits such as fixing text, adding text/images, replacing images, adjusting layout/position/size, or moving/scaling/resizing a title/image/card/block. Search phrases like “HTML 编辑”, “HTML editor”, “HTML editing”, “PPT 编辑”, “PPT editor”, “HTML PPT 编辑”, “网页 HTML 编辑”, “演示稿编辑”, and “幻灯片编辑” apply only when the target is a local/saved HTML file. Clean export patches text/images/backgrounds/layout styles back into the original source HTML instead of saving runtime DOM. Do not use for live websites, authenticated pages, generic source-code editing, or PPTX/PowerPoint files; ask for a saved local HTML copy first.
metadata:
  openclaw:
    homepage: https://github.com/wuhaoyupku/html-mender
    requires:
      bins:
        - node
---

# HTML Mender

Use this skill to turn a local `.html` deck into a browser-editable copy. HTML Mender is built for HTML PPTs and AI-generated slide pages where the user wants small visual edits instead of regenerating the whole page.

## Core Behavior

- Generates an editable `*.editable.html` next to the source unless `--out` is provided.
- Keeps the original source HTML as the clean-export baseline.
- Exports by patching changed or newly inserted text/images, background images, and layout styles back into the source.
- Avoids saving editor UI, generated runtime state, navigation dots, current-slide transforms, or injected scripts.
- Never modifies the original HTML by default.

## Workflow

1. Locate the user's local source HTML. If multiple files match, ask which one to edit.
2. Run the injector:

```bash
node /path/to/this-skill/scripts/inject-html-editor.mjs /absolute/path/input.html
```

3. Open the generated editable file directly, preferably as `file:///absolute/path/name.editable.html`.
4. Let the user edit visually in the browser.
5. Tell the user to click `下载 HTML` / `Download HTML` to save the durable clean result.

Do not start a local HTTP server just to view the file unless `file://` blocks required local assets.

## Script Options

```bash
node scripts/inject-html-editor.mjs <input.html> \
  --out <output.html> \
  --lang zh-CN \
  --mode basic
```

- `--out`: custom output path.
- `--lang zh-CN|en`: editor language. Default: `zh-CN`.
- `--mode basic`: keeps external links and applies edits back to source HTML. Default: `basic`.
- `--no-autostart`: inject runtime without starting the editor automatically.

## Important Notes

- Local draft saving is disabled; refreshing can lose unsaved edits.
- Keep editable/exported HTML next to the original assets when the deck uses relative CSS or images.
- CSP meta tags are preserved. If CSP blocks inline startup, use the browser extension workflow or ask the user how to handle the trusted file.
- The skill runtime does not bundle remote CSS/images and avoids network-backed export.
- If the editable page appears unstyled, regenerate it beside the original HTML so relative paths resolve.

## Version Notes

### 0.1.16

- Tightens the skill trigger wording around local or saved HTML files.

### 0.1.15

- Refines the marketplace-facing title and summary wording for common HTML/PPT editing requests.
- Keeps the same local/saved HTML scope and safety boundaries as 0.1.14.

### 0.1.14

- Improves Chinese search and trigger wording for `HTML 编辑`, `PPT 编辑`, `HTML PPT 编辑`, `网页编辑`, `演示稿编辑`, and `幻灯片编辑`.
- Keeps the skill scope explicitly limited to local or saved HTML files and excludes live websites, authenticated online pages, generic source-code edits, and PPTX files.

### 0.1.13

- Adds direct border handles in the default text/image editing mode.
- Drag the selected border or label to move an element.
- Drag side handles to resize width/height; drag corner handles to resize proportionally.
- Default image dragging moves the image frame; hold Option/Alt to adjust image content inside the frame.
- Shift / Cmd / Ctrl multi-select works in default text/image mode and opens alignment / same-size controls.
- Overlapping text/image boxes are ordered so individual elements are easier to select.
- Removes the top-level Text/Image vs. Move layout switch because border handles now cover the normal layout workflow.
- Shortens the toolbar status text to fit in compact toolbars.
- Fixes Ctrl/Cmd+Z when focus is on editor UI such as image handles or popover controls.
- Fixes first-drag undo for images whose frame originally had no inline style, and covers sequential image drags so they do not snap back.
- Adds a movable cursor when hovering a selected text box's draggable border or label.

### 0.1.12

- Adds `新增文字` / `Add text` and `新增图片` / `Add image` toolbar actions.
- Persists inserted text and image elements through source-based `basic` export.

### 0.1.11

- Renames the public ClawHub listing, skill title, and visible description to HTML Mender.

### 0.1.10

- Adds temporary multi-selection in layout mode with `Shift` / `Cmd` / `Ctrl` click.
- Multi-selected modules can move, scale, resize, reset, align, and match width/height together.
- Batch layout operations undo and redo as one history step.

### 0.1.9

- Fixes injection for complex HTML files that contain embedded `</body>` strings inside JavaScript data.
- Keeps unchanged source HTML byte-for-byte during clean export.
- Exports only elements that the editor actually modified, then applies source-string patches before falling back to DOM serialization.

### 0.1.8

- Adds `移动缩放 / 改宽高 / 恢复` in layout mode.
- `移动缩放` uses `transform: scale(...)` for safer visual scaling.
- `改宽高` writes real `width` / `height` for width-only, height-only, or stretched changes.
- `恢复` clears movement, scale, and editor-added size while preserving original transform and inline dimensions.

### 0.1.7

- Adds `文字/图片` and `位置微调` mode switching.
- Adds drag and arrow-key layout movement for visible text, images, cards, and blocks.
- Preserves layout changes in clean source-based export.
- Improves nested layout selection so smaller inner elements remain selectable.
- Adds explicit edit-box state feedback.

## Example

User: `帮我把 /Users/me/deck.html 变成可编辑版本`

Run:

```bash
node /path/to/this-skill/scripts/inject-html-editor.mjs /Users/me/deck.html --lang zh-CN --mode basic
```

Then open `/Users/me/deck.editable.html` for visual editing.
