# -*- coding: utf-8 -*-
"""
Toutiao Publisher Module (v2)
=============================
Publishes articles to Toutiao (今日头条) via playwright-cli automation.

Generates a complete script suite for robust publishing:
  - inject_content.js     — ProseMirror paste injection (with json.dumps escaping)
  - batch_upload.js       — Batch image upload with placeholder matching
  - check_cover.js        — Verify cover image is set
  - check_missing.js      — Detect which placeholders were NOT replaced
  - insert_fallback.js  — Fallback: insert missing images at fixed positions

Usage:
    python toutiao_publish.py prepare article.md --output prep/ --images images/
    python toutiao_publish.py publish --title "标题" --content content.html --images img/
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def _md_to_html(md_content: str) -> str:
    """Convert Markdown to HTML using the markdown library (preferred) or regex fallback."""
    try:
        import markdown as md_lib
        html = md_lib.markdown(
            md_content,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.nl2br",
            ],
        )
        # Ensure paragraphs are clean (no extra <p> around block elements)
        html = html.replace("<p><blockquote>", "<blockquote>")
        html = html.replace("</blockquote></p>", "</blockquote>")
        return html
    except ImportError:
        # Fallback regex-based conversion (basic)
        html = md_content
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"^- (.+)$", r"<p>\1</p>", html, flags=re.MULTILINE)
        html = re.sub(r"\n\n", "</p><p>", html)
        return html


def _extract_images(md_content: str, images_dir: str) -> list:
    """Extract image references from Markdown, ordered by appearance.
    Returns list of dicts: {alt, src, placeholder, filename}
    """
    images = []
    seen = set()
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    for match in pattern.finditer(md_content):
        alt = match.group(1).strip()
        src = match.group(2).strip()
        # Resolve relative paths
        if not os.path.isabs(src) and images_dir:
            src_abs = os.path.join(images_dir, src)
            if os.path.exists(src_abs):
                src = src_abs
        # Deduplicate by resolved path
        if src in seen:
            continue
        seen.add(src)
        filename = Path(src).name
        images.append({
            "alt": alt,
            "src": src,
            "placeholder": f"[图表：{alt or filename}]" if alt else f"[配图{len(images) + 1}]",
            "filename": filename,
        })
    return images


def _replace_images_with_placeholders(md_content: str, images: list) -> str:
    """Replace image Markdown with text placeholders for ProseMirror injection."""
    result = md_content
    for img in images:
        md_ref = f"![{img['alt']}]({img['src']})"
        result = result.replace(md_ref, f"\n\n{img['placeholder']}\n\n")
    return result


def _generate_inject_script(html_content: str) -> str:
    """Generate ProseMirror paste injection script with proper JSON escaping."""
    html_escaped = json.dumps(html_content)
    return f"""// Toutiao ProseMirror content injection (v2)
async function(page) {{
  const htmlContent = {html_escaped};
  const result = await page.evaluate((htmlContent) => {{
    const editor = document.querySelector('.ProseMirror');
    if (!editor) {{ return 'editor-not-found'; }}
    editor.focus();
    const dt = new DataTransfer();
    dt.setData('text/html', htmlContent);
    const pasteEvent = new ClipboardEvent('paste', {{
      clipboardData: dt,
      bubbles: true,
      cancelable: true
    }});
    editor.dispatchEvent(pasteEvent);
    return editor.innerHTML.length;
  }}, htmlContent);
  return result;
}}
"""


def _generate_batch_upload_script(images: list, images_dir: str) -> str:
    """Generate batch image upload script with robust placeholder matching."""
    images_json = json.dumps(images, ensure_ascii=False, indent=2)
    images_dir_escaped = images_dir.replace("\\", "\\\\")
    return f"""// Batch image upload for Toutiao (v2)
async function(page) {{
  const images = {images_json};
  const results = [];

  for (const img of images) {{
    // 1. Locate placeholder paragraph
    const found = await page.evaluate((text) => {{
      const paragraphs = document.querySelectorAll('.ProseMirror p');
      for (const p of paragraphs) {{
        const t = p.textContent.trim();
        if (t === text || t.includes(text.replace('[图表：', '').replace('[配图', ''))) {{
          const range = document.createRange();
          range.selectNodeContents(p);
          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          return true;
        }}
      }}
      return false;
    }}, img.placeholder);

    if (!found) {{
      results.push(`NOT-FOUND: ${{img.placeholder}}`);
      continue;
    }}

    // 2. Delete placeholder
    await page.evaluate(() => {{
      document.execCommand('delete');
    }});
    await page.waitForTimeout(300);

    // 3. Click image button
    const imageBtn = await page.$('.syl-toolbar-tool.image');
    if (!imageBtn) {{ results.push(`NO-IMAGE-BTN: ${{img.placeholder}}`); continue; }}
    await imageBtn.click();
    await page.waitForTimeout(600);

    // 4. Upload file
    const fileInput = await page.$('input[type=file]');
    if (!fileInput) {{ results.push(`NO-FILE-INPUT: ${{img.placeholder}}`); continue; }}
    const filePath = `{images_dir_escaped}/${{img.filename}}`;
    await fileInput.setInputFiles(filePath);
    await page.waitForTimeout(2500);

    // 5. Click confirm
    const confirmBtn = await page.$('button:has-text("确定")');
    if (confirmBtn) await confirmBtn.click();
    await page.waitForTimeout(1800);

    results.push(`OK: ${{img.placeholder}}`);
  }}

  return results.join('\\n');
}}
"""


def _generate_check_cover_script() -> str:
    return """// Check if cover image is set
async function(page) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
  const result = await page.evaluate(() => {
    var imgs = [].slice.call(document.querySelectorAll('img'));
    var topImgs = [];
    imgs.forEach(function(i, idx) {
      var r = i.getBoundingClientRect();
      if (r.top > -10 && r.top < 200) {
        topImgs.push({idx: idx, top: Math.round(r.top), left: Math.round(r.left), w: i.width, h: i.height, src: (i.src || '').slice(0, 100)});
      }
    });
    return {total: imgs.length, topImgs: topImgs};
  });
  return result;
}
"""


def _generate_check_missing_script() -> str:
    return """// Check which placeholders were NOT replaced by images
async function(page) {
  return await page.evaluate(() => {
    function getId(src) {
      var m = (src || '').match(/tos-cn-i-6w9my0ksvp\/([a-f0-9]+)/);
      return m ? m[1] : '';
    }
    var templ = [].slice.call(document.querySelectorAll('.pgc-img')).map(x => getId(x.querySelector('img') ? x.querySelector('img').src : ''));
    var shown = [].slice.call(document.querySelectorAll('.img-loading-container')).map(x => getId(x.querySelector('img') ? x.querySelector('img').src : ''));
    var missing = templ.filter(id => id && shown.indexOf(id) === -1);
    return {templCount: templ.length, shownCount: shown.length, templIds: templ, shownIds: shown, missing: missing};
  });
}
"""


def _generate_insert_fallback_script(images: list, images_dir: str) -> str:
    """Generate fallback script that inserts missing images at specific positions."""
    if not images:
        return "// No images defined\nasync function(page) { return 'no-images'; }\n"
    # Build a search map: keyword -> filename for fallback insertion
    search_map = []
    for img in images:
        keyword = img["alt"] or img["filename"].replace("chart_", "").replace(".png", "")
        search_map.append({
            "keyword": keyword[:20],  # truncate for safety
            "filename": img["filename"],
        })
    search_map_json = json.dumps(search_map, ensure_ascii=False, indent=2)
    images_dir_escaped = images_dir.replace("\\", "\\\\")
    return f"""// Fallback: insert missing images by searching for keywords in headings/paragraphs
async function(page) {{
  const searchMap = {search_map_json};
  const results = [];

  for (const item of searchMap) {{
    // Try to find a heading or paragraph containing the keyword
    const found = await page.evaluate((kw) => {{
      const ps = document.querySelectorAll('.ProseMirror h1, .ProseMirror h2, .ProseMirror h3, .ProseMirror h4, .ProseMirror p');
      for (const p of ps) {{
        const t = (p.textContent || '').trim();
        if (t.indexOf(kw) > -1) {{
          const range = document.createRange();
          range.setStart(p, 0);
          range.collapse(true);
          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          return p.tagName + ': ' + t.slice(0, 40);
        }}
      }}
      return 'NOT-FOUND';
    }}, item.keyword);

    if (found === 'NOT-FOUND') {{
      results.push('NOT-FOUND: ' + item.keyword);
      continue;
    }}
    results.push('cursor-at: ' + found);
    await page.waitForTimeout(500);

    // Click image button
    const imageBtn = await page.$('.syl-toolbar-tool.image');
    if (!imageBtn) {{ results.push('NO-IMAGE-BTN: ' + item.keyword); continue; }}
    await imageBtn.click();
    await page.waitForTimeout(800);

    // Upload file
    const fileInput = await page.$('input[type=file]');
    if (!fileInput) {{ results.push('NO-FILE-INPUT: ' + item.keyword); continue; }}
    const filePath = `{images_dir_escaped}/${{item.filename}}`;
    await fileInput.setInputFiles(filePath);
    results.push('file-set: ' + item.filename);
    await page.waitForTimeout(4000);

    // Click confirm
    const confirmBtn = await page.$('button:has-text("确定")');
    if (confirmBtn) {{ await confirmBtn.click(); results.push('confirm-clicked: ' + item.filename); }}
    else {{ results.push('NO-CONFIRM-BTN: ' + item.filename); }}
    await page.waitForTimeout(2500);
  }}

  return results.join('\\n');
}}
"""


def prepare_content(md_path: str, output_dir: str, images_dir: str = "") -> dict:
    """Prepare content for Toutiao publishing."""
    os.makedirs(output_dir, exist_ok=True)

    with open(md_path, encoding="utf-8") as f:
        md_content = f.read()

    # Extract title from first H1
    title = "Untitled"
    lines = md_content.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            title = line.strip()[2:].strip()
            break

    # Validate title length
    title_warning = ""
    if len(title) > 30:
        title_warning = f"WARNING: Title is {len(title)} chars (>30 limit). Truncate to: {title[:30]}"
        print(title_warning)

    # Resolve images directory
    if not images_dir:
        images_dir = os.path.join(os.path.dirname(os.path.abspath(md_path)), "images")
    if not os.path.isabs(images_dir):
        images_dir = os.path.abspath(images_dir)

    # Extract images in order of appearance
    images = _extract_images(md_content, images_dir)
    print(f"Found {len(images)} images (ordered by appearance):")
    for i, img in enumerate(images, 1):
        print(f"  {i}. {img['placeholder']} -> {img['filename']}")

    # Replace images with placeholders
    md_with_placeholders = _replace_images_with_placeholders(md_content, images)

    # Convert to HTML
    html_content = _md_to_html(md_with_placeholders)

    # Generate scripts
    inject_script = _generate_inject_script(html_content)
    batch_script = _generate_batch_upload_script(images, images_dir)
    check_cover_script = _generate_check_cover_script()
    check_missing_script = _generate_check_missing_script()
    insert_fallback_script = _generate_insert_fallback_script(images, images_dir)

    # Save scripts
    files = {
        "inject_content.js": inject_script,
        "batch_upload.js": batch_script,
        "check_cover.js": check_cover_script,
        "check_missing.js": check_missing_script,
        "insert_fallback.js": insert_fallback_script,
    }
    for filename, content in files.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved: {path}")

    # Save metadata
    images_json = os.path.join(output_dir, "images.json")
    with open(images_json, "w", encoding="utf-8") as f:
        json.dump({"title": title, "images": images, "images_dir": images_dir}, f, ensure_ascii=False, indent=2)

    # Save raw HTML for reference
    html_path = os.path.join(output_dir, "content.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Save publish instructions
    instructions = _generate_publish_instructions(title, images, output_dir, images_dir)
    instructions_path = os.path.join(output_dir, "PUBLISH_INSTRUCTIONS.md")
    with open(instructions_path, "w", encoding="utf-8") as f:
        f.write(instructions)

    print(f"\nPrepared {len(images)} images. Next: run PUBLISH_INSTRUCTIONS.md")
    return {
        "title": title,
        "title_warning": title_warning,
        "images": images,
        "output_dir": output_dir,
        "instructions": instructions_path,
    }


def _generate_publish_instructions(title: str, images: list, output_dir: str, images_dir: str) -> str:
    """Generate comprehensive publish instructions."""
    n = len(images)
    return f"""# Toutiao Publishing Instructions

## Article Info
- Title: {title}
- Title length: {len(title)} chars (limit: 30)
- Images: {n}
- Images dir: {images_dir}

## Prepared Files (in `{output_dir}`)
| File | Purpose |
|------|---------|
| `inject_content.js` | ProseMirror paste injection (run first) |
| `batch_upload.js` | Batch upload {n} images, replacing placeholders |
| `check_cover.js` | Verify cover image is set at top of article |
| `check_missing.js` | Detect which placeholders were NOT replaced |
| `insert_fallback.js` | Fallback: insert missing images by keyword search |
| `content.html` | Raw HTML for reference |
| `images.json` | Image metadata |

## Step-by-Step Publishing Guide

### 1. Launch playwright-cli in headed mode
```bash
playwright-cli open "https://mp.toutiao.com/profile_v4/graphic/publish" --headed
```
**Critical**: Must use `--headed` so the browser window is visible for QR code scan.

### 2. Scan QR code to login
Wait for user to scan and log in. Toutiao keeps login state after first scan.

### 3. Close AI assistant popup
```bash
playwright-cli eval "(function(){{document.querySelectorAll('.byte-drawer-mask, .byte-drawer, .ai-assistant-drawer').forEach(el=>el.remove());return 'cleared';}})()"
```
This popup blocks the title input and preview area.

### 4. Fill title
```bash
playwright-cli fill <ref> "{title[:30]}"
```
Note: Title limit is 30 chars. Current title is {len(title)} chars.
{"**WARNING**: Title exceeds 30 chars! Truncate manually." if len(title) > 30 else ""}

### 5. Inject content (run inject_content.js)
```bash
playwright-cli run-code {output_dir}/inject_content.js
```
Expected output: a large number (e.g., 30000+) indicating successful HTML injection.

### 6. Batch upload images (run batch_upload.js)
```bash
playwright-cli run-code {output_dir}/batch_upload.js
```
This will upload {n} images one by one, replacing placeholders in order.
**Important**: Images are matched in the order they appear in the article. If any placeholder is NOT found, it will be reported as `NOT-FOUND`.

### 7. Check for missing images
If batch_upload reports any `NOT-FOUND`, run check_missing.js to diagnose:
```bash
playwright-cli run-code {output_dir}/check_missing.js
```
Then run insert_fallback.js to insert the missing images:
```bash
playwright-cli run-code {output_dir}/insert_fallback.js
```

### 8. Check cover image
```bash
playwright-cli run-code {output_dir}/check_cover.js
```
Verify the cover image is visible at the top of the article.

### 9. Set cover image (if not auto-set)
If cover is not set, click the "单图" button, upload your cover image, and confirm.

### 10. Preview and publish
Click "预览并发布" (red button) → enters preview page → click "确认发布" to submit.
**Critical**: Must click TWICE! First "预览并发布", then "确认发布".

### 11. Verify success
After publishing, the URL should contain the article ID. Check `https://mp.toutiao.com/profile_v4/graphic/articles` to see the new article at the top with "审核中" status.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser window not visible | Add `--headed` to playwright-cli |
| Title input blocked | Close AI assistant popup (step 3) |
| Placeholder NOT-FOUND | Check if placeholder text matches exactly; run insert_fallback.js |
| Image not uploaded | Check if file exists in `{images_dir}`; verify filename matches |
| Cover missing | Run check_cover.js and manually set cover (step 9) |
| "预览并发布" no response | It opens preview page; scroll down to find "确认发布" |

## Image Mapping (ordered by appearance in article)
{"\n".join([f"{i+1}. `{img['placeholder']}` -> `{img['filename']}`" for i, img in enumerate(images)])}

## Key Lessons from Recent Pushes (2026-08-14 to 2026-08-21)
1. **Image upload fails silently** — placeholders show "编辑|搜图" instead of images. Use check_missing.js to detect.
2. **Placeholder order matters** — images must match top-to-bottom article order. prepare orders them by appearance.
3. **Batch upload sometimes misses** — insert_fallback.js provides keyword-based fallback insertion.
4. **Title must be <= 30 chars** — or Toutiao will reject or truncate.
5. **Always use headed mode** — no headless for QR login.
6. **Click publish TWICE** — "预览并发布" then "确认发布".
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toutiao publisher (v2)")
    subparsers = parser.add_subparsers(dest="command")

    prep = subparsers.add_parser("prepare", help="Prepare article for publishing")
    prep.add_argument("input", help="Markdown article path")
    prep.add_argument("--output", "-o", default="./toutiao-prep", help="Output directory")
    prep.add_argument("--images", "-i", default="", help="Images directory (default: <input_dir>/images)")

    pub = subparsers.add_parser("publish", help="Generate publish instructions")
    pub.add_argument("--title", required=True, help="Article title")
    pub.add_argument("--inject", required=True, help="Inject script path")
    pub.add_argument("--images", required=True, help="Images JSON path")

    args = parser.parse_args()

    if args.command == "prepare":
        result = prepare_content(args.input, args.output, args.images)
        print(f"\nTitle: {result['title']}")
        if result['title_warning']:
            print(f"Warning: {result['title_warning']}")
        print(f"Images: {len(result['images'])}")
        print(f"Instructions: {result['instructions']}")
    elif args.command == "publish":
        print("Use 'prepare' command to generate scripts, then follow PUBLISH_INSTRUCTIONS.md")
    else:
        parser.print_help()
