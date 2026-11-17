---
name: html-to-wechat
description: "Take existing HTML content (file, URL, or pasted HTML) and publish it directly to WeChat Official Account draft box. No file conversion, no web scraping — just HTML to WeChat compatibility check to publish. Use when the user already has HTML and wants to push it to WeChat."
version: 1.0.0
prerequisites:
  - anything-to-wechat
tags:
  - wechat
  - html
  - publishing
  - 公众号
  - 发布
  - 草稿箱
triggers:
  - "HTML.*发.*微信"
  - "HTML.*发.*公众号"
  - "html.*to.*wechat"
  - "把这个HTML发到微信"
  - "把这个HTML发到公众号"
  - "HTML.*发布"
  - "HTML.*草稿箱"
  - "html.*publish.*wechat"
  - "html.*draft.*wechat"
  - "推送HTML到微信"
  - "上传HTML到公众号"
  - "已有HTML.*发布"
---

# HTML to WeChat

Take **existing HTML content** — a file, a URL, or pasted HTML — and publish it to the **WeChat Official Account draft box** in one streamlined workflow.

This is the simplest WeChat publishing skill: **no file conversion, no web scraping**. Just HTML, a compatibility check, and publish.

## User-Facing Promise

Accept requests like:

- "把这个 HTML 文件发到我的微信公众号"
- "我有一个现成的 HTML 页面，帮我发到公众号草稿箱"
- "Publish this HTML to my WeChat account"
- "把这个链接里的 HTML 推送到微信"
- "我有一段 HTML 代码，发到公众号"
- "Help me push this HTML page to my WeChat draft box"

**Return a published draft in the WeChat draft box, not a proposal.**

---

## First-Time Setup

### 1. Configure WeChat Credentials

You need a **WeChat Official Account** (服务号 or 订阅号 with API access).

**Get your credentials:**

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 -> 基本配置
3. Copy your **AppID** and reset/view **AppSecret**
4. Add your server's public IP to the **IP白名单**

> **SECURITY: NEVER hardcode credentials in scripts or source files. Always use environment variables or interactive prompts.**

**Set environment variables (recommended):**

On **macOS / Linux**:
```bash
export WECHAT_APP_ID="your_appid_here"
export WECHAT_APP_SECRET="your_appsecret_here"
```

On **Windows** (PowerShell, persistent):
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid_here", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret_here", "User")
```

On **Windows** (Command Prompt, session only):
```cmd
set WECHAT_APP_ID=your_appid_here
set WECHAT_APP_SECRET=your_appsecret_here
```

**No environment variables set?** The publish script will prompt interactively on first run. You can also pass credentials at runtime via Python subprocess (see Phase 5).

### 2. Install Companion Skill

This skill depends on the **anything-to-wechat** skill from ClawHub:

```
clawhub install anything-to-wechat
```

- **anything-to-wechat** -- provides `publish_to_wechat.py` (WeChat API publishing) and `convert_for_wechat.py` (HTML compatibility conversion)

---

## Prerequisites

| Dependency | Required | Purpose |
|---|---|---|
| `beautifulsoup4` (pip) | Yes | HTML parsing for validation and conversion |
| `cssutils` (pip) | Yes | CSS parsing for style inlining |
| `Pillow` (pip) | Yes | Cover image compression |
| `requests` (pip) | Yes | WeChat API HTTP calls |
| **anything-to-wechat** skill | Yes | `publish_to_wechat.py` and `convert_for_wechat.py` |

> All pip dependencies auto-install on first use if missing.

---

## Workflow

### Phase 1: Collect HTML Input

Determine the source of the HTML content.

**If the user has already provided one of the following, skip to Phase 2:**

- A local file path (e.g., `./article.html`)
- A URL pointing to an HTML page
- Pasted HTML source code

**Otherwise, ask the user:**

```
Question: "请提供你想发布到微信公众号的 HTML 内容"
Options:
  - "本地 HTML 文件路径"
  - "粘贴 URL 链接"
  - "直接粘贴 HTML 代码"
```

**Handling each input type:**

| Input Type | Action |
|---|---|
| **Local file path** | Read the file directly. Use the Read tool or open in Python. |
| **URL** | Use the `WebFetch` tool to retrieve the page HTML source. |
| **Pasted HTML** | Save the pasted content to a temporary file (e.g., `<workspace>/input.html`). |

**Important for URLs:** Use WebFetch only to fetch the raw HTML. If the page requires JavaScript rendering or returns a login wall, inform the user and ask them to provide the HTML file directly.

**Save the HTML** to `<workspace>/input.html` before proceeding.

---

### Phase 2: Validate HTML for WeChat Compatibility

Before converting, **inspect the HTML** for known WeChat incompatibilities.

**Read the HTML file** and check for the following issues:

#### WeChat Strips / Rejects

| Issue | Detection Method | Severity |
|---|---|---|
| `<style>` tags | Search for `<style` in HTML | HIGH -- WeChat removes all style blocks |
| `<link>` stylesheet tags | Search for `<link.*stylesheet` | HIGH -- External stylesheets are stripped |
| CSS variables (`var(--xxx)`) | Regex: `var\(--` | HIGH -- Rendered as blank |
| `<script>` tags | Search for `<script` | CRITICAL -- Removed entirely, may indicate interactive content |
| `position: fixed` or `position: sticky` | Regex: `position:\s*(fixed\|sticky)` | MEDIUM -- Layout breakage |
| `backdrop-filter` | Search for `backdrop-filter` | LOW -- Visual degradation |
| `z-index` | Regex: `z-index` | LOW -- Layering ignored |
| External fonts (`@font-face`, Google Fonts) | Search for `@font-face`, `fonts.googleapis` | MEDIUM -- Font fallback used |
| `<iframe>` embeds | Search for `<iframe` | HIGH -- Removed by WeChat |
| `<video>` / `<audio>` tags | Search for `<video`, `<audio` | MEDIUM -- May not play |

#### WeChat Requires

| Requirement | Check Method |
|---|---|
| Inline styles only | Verify all elements use `style=""` attributes |
| Light background (`#ffffff` or near-white) | Check `background-color` values |
| Max-width 680px on outer container | Check container width constraints |
| System fonts only | Verify `font-family` uses `-apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif` |
| Total HTML size under 2MB | Check file size |
| Images via `<img>` tags with explicit styles | Verify image markup |

**Decision after validation:**

- **No issues found** -- Skip Phase 3, proceed directly to Phase 4.
- **Issues found** -- Proceed to Phase 3 for automated conversion.

**Report the validation results to the user** with a brief summary:
```
[WeChat Compatibility Check]
- Found 2 <style> tags (will be inlined)
- Found CSS variables (will be resolved)
- Found position:sticky (will be removed)
- File size: 145KB (OK, under 2MB limit)
- Background: #ffffff (OK)
```

---

### Phase 3: Convert HTML for WeChat

If Phase 2 found incompatibilities, run the conversion script from the **anything-to-wechat** skill:

```bash
python "<anything-to-wechat_skill_dir>/scripts/convert_for_wechat.py" \
  --input "<workspace>/input.html" \
  --output "<workspace>/wechat_article.html"
```

This script automatically:

- Extracts CSS from `<style>` tags and inlines them as `style=""` attributes
- Converts dark backgrounds to light themes
- Resolves all CSS variables (`var(--xxx)`) to literal color values
- Removes WeChat-incompatible CSS properties (`position: fixed/sticky`, `backdrop-filter`, `z-index`)
- Ensures all elements have inline styles
- Applies system font fallbacks

**After conversion:** Re-validate the output by reading `wechat_article.html` and confirming:

1. No `<style>` tags remain
2. No `<script>` tags remain
3. All elements have inline `style=""` attributes
4. Background is light (white or near-white)
5. File size is under 2MB

If any issues persist after conversion, **manually fix them** using the Edit tool:

- Remove remaining `<style>` or `<script>` blocks
- Replace dark background colors with `#ffffff`
- Add `max-width: 680px; margin: 0 auto;` to the outermost container
- Ensure `font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif` on the body

If no conversion was needed in Phase 2, copy the input file:

```bash
copy "<workspace>/input.html" "<workspace>/wechat_article.html"
```

---

### Phase 4: Prepare Cover Image

WeChat requires a cover image for `thumb_media_id` upload. The image **must be under 64KB**.

**Option A: User provides a cover image**

If the user supplied a cover image path, use it directly and proceed to compression.

**Option B: Generate a cover image**

Use the `ImageGen` tool with a prompt derived from the HTML content:

- Read the HTML `<title>` or first `<h1>` to determine the topic
- Generate a visually compelling cover image
- **Size: `1024x768`** (WeChat cover ratio 4:3)
- Save as `<workspace>/wechat_cover.png`

**Compress the cover image:**

WeChat requires cover images (thumb_media_id) to be **under 64KB**.

```bash
python "<skill_dir>/scripts/compress_image.py" \
  --input "<workspace>/wechat_cover.png" \
  --output "<workspace>/wechat_cover_compressed.jpg" \
  --max-size 64
```

Always run compression, even if the image seems small -- it will not enlarge files.

**Fallback:** If `compress_image.py` fails to reach 64KB, use `ImageGen` to regenerate a simpler cover image (fewer details, simpler composition, larger flat color areas) and try compression again.

---

### Phase 5: Publish to WeChat Draft Box

Use `publish_to_wechat.py` from the **anything-to-wechat** skill.

**IMPORTANT: Credentials must NEVER be hardcoded in scripts. Use environment variables or the Python subprocess pattern below.**

#### macOS / Linux

```bash
WECHAT_APP_ID="$WECHAT_APP_ID" WECHAT_APP_SECRET="$WECHAT_APP_SECRET" \
python "<anything-to-wechat_skill_dir>/scripts/publish_to_wechat.py" \
  --file "<workspace>/wechat_article.html" \
  --title "<article_title>" \
  --cover "<workspace>/wechat_cover_compressed.jpg" \
  --digest "<article_summary_under_120_chars>"
```

#### Windows (Python subprocess for env vars + UTF-8 encoding)

On Windows, environment variable passing via `set` in cmd or `$env:` in PowerShell can be unreliable across sessions and may have encoding issues with Chinese characters. Use the Python subprocess pattern:

```python
python -c "
import os, subprocess, sys
os.environ['WECHAT_APP_ID'] = '<app_id>'
os.environ['WECHAT_APP_SECRET'] = '<app_secret>'
result = subprocess.run([
    sys.executable,
    r'<anything-to-wechat_skill_dir>\scripts\publish_to_wechat.py',
    '--file', r'<workspace>\wechat_article.html',
    '--title', '<article_title>',
    '--cover', r'<workspace>\wechat_cover_compressed.jpg',
    '--digest', '<article_summary_under_120_chars>'
], capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
print(result.stderr)
"
```

**Key Windows notes:**
- Always pass `encoding='utf-8'` to `subprocess.run` to handle Chinese titles and digests correctly
- Use raw strings (`r'...'`) for Windows file paths to avoid backslash escape issues
- Never write credentials to disk -- pass them via `os.environ` in the subprocess wrapper only

**If credentials are not set:** The script will prompt interactively for AppID and AppSecret.

**Handle IP whitelist errors:**

If the API returns `ip not in whitelist`:

1. Extract the server's public IP from the error message
2. Tell the user: "请将 IP `<ip>` 添加到微信公众号后台的 IP 白名单中（设置与开发 -> 基本配置 -> IP白名单）"
3. Wait for confirmation, then retry the publish command

---

### Phase 6: Confirm and Handoff

After successful publishing, report to the user:

1. **Success status** with the Media ID
2. **Link to WeChat backend:** https://mp.weixin.qq.com/
3. **Message:** "文章已发送到你的微信公众号草稿箱，请登录微信公众平台审核后一键发布。"

Include the following summary:

```
[Publish Complete]
- Title: <article_title>
- Media ID: <media_id>
- Cover image: <compressed_cover_path> (<file_size>KB)
- HTML file: <wechat_article_path> (<file_size>KB)
- Digest: <article_summary>
- Next step: Log in to https://mp.weixin.qq.com/ to review and publish
```

---

## WeChat HTML Compatibility Reference

### What WeChat Strips

| Stripped | Effect |
|---|---|
| `<style>` tags | All block-level CSS lost |
| `<link rel="stylesheet">` | External stylesheets removed |
| CSS variables (`var(--*)`) | Rendered as empty / broken |
| `position: fixed` / `sticky` | Layout elements may overlap or disappear |
| `backdrop-filter` | Visual effect lost |
| `z-index` | Element layering ignored |
| `@font-face` / web fonts | Falls back to system font |
| `<script>` tags | All JavaScript removed |
| `<iframe>` tags | Embedded content removed |
| External images (some) | Must be uploaded to WeChat CDN |

### What WeChat Requires

| Requirement | Detail |
|---|---|
| Inline styles | All styling via `style=""` attributes on elements |
| Light background | `#ffffff` or near-white (WeChat renders on white) |
| Max-width 680px | Outer container width for article display |
| System fonts | `-apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif` |
| Under 2MB total | Combined HTML size limit |
| `<img>` tags | Images must use `<img>` with inline width/height styles |
| Cover under 64KB | For `thumb_media_id` upload |

### Recommended HTML Structure

```html
<section style="max-width: 680px; margin: 0 auto; padding: 20px; background: #ffffff; font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #333333; line-height: 1.8;">
  <h1 style="font-size: 22px; font-weight: bold; color: #1a1a1a; margin-bottom: 16px;">Article Title</h1>
  <p style="font-size: 16px; margin-bottom: 16px;">Article content...</p>
  <img src="..." style="width: 100%; height: auto; border-radius: 8px; margin: 16px 0;" />
</section>
```

---

## Error Handling

| Error | Cause | Action |
|---|---|---|
| `<style>` tags remain after conversion | Conversion script missed nested styles | Manually inline remaining styles with Edit tool |
| HTML file exceeds 2MB | Too many inline assets or large content | Simplify content, reduce image count, split into parts |
| Cover image > 64KB after compression | Image too complex for JPEG compression | Regenerate simpler cover via ImageGen, retry compression |
| Cover image upload fails | WeChat CDN rejection | Retry with different format (JPG instead of PNG) or smaller dimensions |
| `invalid content` from WeChat API | Remaining unsupported CSS or HTML | Re-run convert_for_wechat.py, manually inspect output |
| `ip not in whitelist` | Server IP not in WeChat backend whitelist | Extract IP from error, guide user to add it, retry |
| `access_token expired` | Token TTL exceeded (7200s) | Re-fetch token and retry publish |
| No AppID / AppSecret | Credentials not configured | Script prompts interactively, or ask user to set env vars |
| `beautifulsoup4` not installed | Missing pip dependency | Auto-installed by convert_for_wechat.py on first run |
| Chinese characters garbled (Windows) | Console encoding not UTF-8 | Use `encoding='utf-8'` in Python subprocess pattern |
| File not found | Incorrect path or workspace issue | Verify path exists before proceeding |
| URL returns 403 / login wall | Site blocks automated fetching | Ask user to provide HTML file directly |

---

## Script Reference

| Script | Location | Purpose |
|---|---|---|
| `compress_image.py` | `html-to-wechat/scripts/` | Compress images to meet WeChat 64KB cover limit |
| `convert_for_wechat.py` | `anything-to-wechat/scripts/` | Convert HTML with style tags to inline-style WeChat HTML |
| `publish_to_wechat.py` | `anything-to-wechat/scripts/` | Publish HTML to WeChat Official Account draft box |

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID. Read from env var or prompted interactively. |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret. Read from env var or prompted interactively. |

> **Never commit credentials to version control.** Always use environment variables, and the publish script falls back to interactive prompts when env vars are missing.
