---
name: md-out-of-chat
description: 和 AI 聊完，先把它写成的那堆东西拿出来——一句话就能把 .md 变成手机上能读、能转发的样子。默认出单页网页；要发群或发朋友圈就出**一张手机长图 PNG**（750px 宽 @2x）。典型用法：聊完看到满意的方案想躺床上再读一遍；今天写了一天的笔记想一次全转出来在手机上看；把一段结论转成图发到群里。**全程在本机跑，不上传、不需要账号和 API Key**；支持单个文件，也支持把一个目录里「今天 / 本周」改过的 .md 批量转出（无状态文件、不依赖定时任务）。长图出图前自动做隐私自检（手机号 / 身份证 / 邮箱 / 疑似密钥 / 长卡号），只报类别与数量、不打印原文。
Convert a Markdown file into a mobile-friendly local HTML page, or a share-ready long-image PNG (chat export to long image). WeChat/Feishu/Slack/Discord-friendly view. Use when a .md report, note, or chat export needs to be read or forwarded from a phone, or when you're away from your computer and want everything you made today readable on mobile. Runs 100% locally with no API key, no account, no upload. A public web URL is produced only when the user explicitly asks for it AND confirms, using a trusted deploy tool. A Mermaid block in the page is a structural summary card (text source that some renderers can draw), not a truly rendered diagram. Respond in the user's current language.
version: 1.9.0
homepage: https://github.com/bonniegeng-max/md-out-of-chat
license: MIT
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python3"],"packages":[],"env":[]}}}
---

# md-out-of-chat

**Pulling Markdown out of chat, into something people can actually read.**

AI agents live in chat (WeChat, Feishu, Slack, Discord, …) and love to write `.md`. But `.md` doesn't render well in any of those apps. Code breaks, tables misalign, links look dead. This skill is the bridge: it takes a `.md` file and turns it into a mobile-friendly, copyable, shareable view.

## Activation

Only activate this skill when **both** conditions hold: (1) the user explicitly mentions it by name (e.g. "use md-out-of-chat", "用 md-out-of-chat 转换"), and (2) the user identifies a concrete input — a `.md` file path, an attached file, a file selected in the conversation, or (for batch export) a named folder. Do not activate on vague phrases alone ("show me this", "转一下", "convert this"), and never infer conversion targets from chat history. Only read the file(s) the user explicitly identified. Never deploy, publish, or invoke other tools unless the user separately requests and confirms that action.

## The Problem

- `.md` files **cannot be opened in WeChat** on mobile
- Code blocks **break layout** on small screens
- Tables **misalign columns** on mobile
- When you're away from your computer, you **can't view** what your assistant just made

## Input

- Path to a `.md` file
- Optional output type: `html` (local file, default), `long-image` (`--long-image`: share-ready PNG + fallback HTML), or `web` (public URL — see the strict conditions below)

## Output

- Default: a local `.html` file that opens in any mobile browser
- `--long-image`: a share-ready **long-image PNG** (750px wide @2x) plus a fallback `.long.html` — see "Long Image Export" below
- `web`: a public URL **only** if the user explicitly asks for it, explicitly confirms before anything is deployed, and the assistant has a trusted deploy tool; otherwise fall back to local HTML
- A Mermaid block written into a page is a **structural summary card** — plain-text diagram source that *some* renderers can display, and that always stays readable as text in the worst case. It is **not** a really rendered diagram: this skill does not lay out nodes, route arrows, or guarantee the picture looks right. If the diagram itself matters, render it to an image elsewhere and embed that image.

## Long Image Export · 长图导出（v1.8.0）

Triggered by `--long-image`, or in conversation by 「出长图」「转长图」「手机长图」「发朋友圈的长图」 **together with an explicitly named .md file** — same activation discipline as HTML mode, never guess the input.

```bash
python3 md2share.py note.md --long-image          # 750px 宽 @2x PNG + 长图版 HTML
python3 md2share.py note.md --long-image=640      # 自定义宽度（480–1600）
python3 md2share.py note.md --long-image --png-scale=3   # 3 倍图
python3 md2share.py note.md --long-html-only      # 只要长图版 HTML，不截图
python3 md2share.py ~/notes --since=today --long-image   # 批量长图
```

How it works (all local, zero installs):

1. Render the same block rules into a **dedicated long-image page**: fixed width, larger type (17.5px body), no TOC, no theme toggle, no copy buttons — interactive controls would be dead pixels in an image.
2. **Tables and code blocks never scroll horizontally in long-image mode.** A scroll container in an image is a cropped image, so they wrap instead (`white-space: pre-wrap` / `table-layout: fixed`).
3. External links print their URL in small gray after the text — a link inside an image is not clickable, so the address is the content.
4. Measure the page height with a first headless pass (`--dump-dom` reading a `<meta>` written by an inline script), then screenshot the full page with a second pass at 2x.
5. Output: `<name>.long.png` (share this) + `<name>.long.html` (fallback, can be screenshotted manually).

Browser requirement and degradation: the PNG step uses a Chromium-family browser **already on the machine** (Chrome / Chromium / Edge / Brave; found, never downloaded or installed). If none exists — or both headless passes fail — the skill still writes the long-image HTML and says so. It never bundles a browser, never installs anything.

Privacy gate: before any PNG is written, the source markdown is scanned for 手机号 / 身份证号 / 邮箱 / 疑似密钥（sk-、ghp_、AKIA、AIza 前缀）/ 长卡号. Findings are reported as **category + count only** (never the matched text, so the log itself cannot leak). The image is still produced — the user decides — but the warning must be relayed. A long image is forwarded more casually than text; that asymmetry is why this check exists here and only here.

No watermark: the long image carries only the document title and a generation timestamp in the footer. No logo, no skill name, no source mark.

### 长图之后：要发小红书 / 视频号怎么办（切图，但不在本 skill 里做）

长图是**一张**，小红书图文是**一组 3:4**。这两件事别混为一谈：

- **本 skill 只负责出长图，不做切割。** 切图改尺寸是另一个动作，混进来会让「只做一件事」的边界糊掉。
- 需要图组时，明确告诉用户：**先用本 skill 出长图 → 再交给图片切割工具按 3:4 切开**（`changtu-xiaohongshu-cropper` 一类专做这件事，或任何能按网格裁图的工具）。
- 不要为了迁就切图而把长图宽度改成非 750px——750px @2x 是给「手机上直接滚动阅读」调的，切成 3:4 时上下留白由切割工具负责。

### 隐私边界（长图模式尤其要讲清）

长图比文字更容易被随手转发，所以这道门槛只加在出图这一侧，**且只在出图时加**：

| 检查什么 | 怎么报 | 是否阻断 |
|---|---|---|
| 手机号 / 身份证号 / 邮箱 / 疑似密钥（`sk-`、`ghp_`、`AKIA`、`AIza` 前缀）/ 长卡号 | **只报类别与数量，绝不打印命中原文**（日志本身不能成为泄露源） | **不阻断**——照常出图，由用户决定 |

三条纪律，任何情况下都不破：

1. **自检结果必须转述给用户**，不能静默跳过；命中了要说"哪一类、几处"，不说"具体是什么"。
2. **不上传、不联网核对、不调用任何外部服务**判断隐私——本地正则，跑完即弃。
3. **不提供"一键删除敏感信息"**。本 skill 只报不改：自动改写正文会让用户以为发出去的是原件，反而更危险。要改就让用户改源 .md 再重跑。

Not for: 生成插画/照片类图像（那不是本 skill 的事）；把长图再切成小红书图组（用专门的切割工具，见上）。

## 对话 → 能发的一页（上游入口）

最常见的真实情况不是「我有一个 .md 文件」，而是**「我刚和 AI 聊出了一堆东西，现在想把它变成能发给别人的一页」**。这个场景由本 skill 承接，分三段走：

| 段 | 谁做 | 做什么 |
|---|---|---|
| 1. 从对话里落成文件 | 宿主 agent | 把这次对话该留下的部分写成 `.md`（一页一个主题，别把整段聊天原样倒出来） |
| 2. 转成能看的样子 | **本 skill** | 单页 HTML（自己手机上读）/ 长图 PNG（发群、发朋友圈）|
| 3. 发出去 | 用户 | 长图直接发；图组先切图；需要公网链接时才走显式确认的部署 |

**关键取舍：本 skill 只做第 2 段。** 第 1 段是写作与归纳，属宿主 agent 的活；第 3 段的公开发布有隐私与账号风险，永远要用户显式确认。把三段混进一个 skill，隐私边界就守不住了。

什么时候用这个入口：聊完看到满意的方案想躺着再读一遍 / 今天写了一天的笔记想一次全转出来 / 把一段结论做成图发到群里。

**这一页应该是「给自己的确认件」，不是「给别人的排版稿」。** 区别在于：为了自己确认，可以保留过程、待办、不确定的地方；为了给别人看，才需要主题、脚注、公众号兼容样式。前者是本 skill，后者是排版类工具——`Not the same as` 里那段话讲的就是这条界线。

## Not the same as

- **A viewer for phones, not a publisher** — it converts one file you name into something a phone can read or forward. It is not a live editor, and it does not keep a library.
- **An art/image generator** — the long image is a faithful picture of your markdown (text, tables, code), not an illustration tool. It does not draw, style, or invent visuals; a Mermaid block written into a page is a **structural summary card** — plain-text diagram source that *some* renderers can display, and that always stays readable as text in the worst case. It is **not** a really rendered diagram: this skill does not lay out nodes, route arrows, or guarantee the picture looks right. If the diagram itself matters, render it to an image elsewhere and embed that image.
- **A publish tool** — local HTML is the default. A public URL is produced only after an explicit, separately confirmed request.
- **baoyu-markdown-to-html** — that skill targets 公众号 article formatting: themes, footnotes, WeChat-compatible rich HTML. This one is not trying to format anything for publication. Its job is narrower and different: "read on your phone what the agent just wrote" — name a file or a folder, get today's/this week's notes as mobile pages, stateless, 100% local, no upload, no account. 排版给别人看是发布，转给自己在手机上读是确认——本 skill 只做后者。

## Design Spec (Blue / White / Gray — Minimal & Clean)

### Colors
- Primary: `#1F4E79` (deep blue, used for titles & headings)
- Accent: `#3B7DD8` (bright blue, used for emphasis)
- Background: `#F5F7FA` (light gray)
- Card: `#FFFFFF` (white)
- Text: `#333333` (main) / `#666666` (secondary)
- Border: `#E1E5EB`

### Typography
- Body: `system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`
- Code: `"SF Mono", Menlo, Monaco, Consolas, monospace`
- Base size: 16px (auto-shrinks on small screens)

## Block Rules

### Headings (h1–h6)
- Color: deep blue
- Weight: 600
- h1: 24px / h2: 20px / h3: 18px
- h1 has a 2px bottom border

### Paragraphs
- 16px, line-height 1.7
- Inline: `**bold**` → strong, `*italic*` → em, `` `code` `` → inline code

### Tables
- Column-aligned
- Header: deep blue background, white text, bold
- Zebra striping (odd / even rows)
- `white-space: nowrap` on headers
- Wraps in a scrollable container on narrow screens

### Code Blocks
- Top label shows the language (e.g. `PYTHON`, `SQL`, `BASH`)
- Syntax highlighting per language:
  - Keywords: red, bold
  - Strings: green
  - Numbers: blue
  - Comments: gray, italic
- Horizontal scroll for long lines
- Never breaks layout

### Lists
- Unordered: bullet points
- Ordered: numbered
- Task lists: `- [ ]` / `- [x]` render as checkboxes (done items struck through)
- 6px vertical spacing between items

### Blockquotes
- `>` lines render as a left-accent-border quote block, gray text

### Links
- `[text](url)` renders as styled anchor; only `http:` / `https:` / `mailto:` schemes allowed (XSS-safe)
- Long URLs wrap on mobile (`word-break: break-all`)

### Inline in table cells
- Cell content supports bold / italic / inline code / links
- `\|` escapes a literal pipe inside cells

## Output Type Decision

Default to **local HTML** for safety and privacy. Produce a long-image PNG when the user asks for 长图 / an image to forward. Only produce a public web URL when the user explicitly asks for one, explicitly confirms, and the assistant has a safe deploy path.

### Default: Local HTML

When the user asks to view a Markdown file without specifying the output type, generate a local `.html` file. Tell the user where it is and that it can be opened on a phone browser.

### When the User Asks for an Image

Use long-image mode (`--long-image`) — see "Long Image Export" above. Relay the privacy self-check result if it flags anything, and hand over the PNG plus the fallback HTML. If no browser is available on the machine, say so and deliver the long-image HTML instead.

### When to Generate a Public Web URL

Generate a public URL only when **all** of these hold:
- The user explicitly says "web" / "link" / "URL" / "公开链接"
- The user explicitly confirms deployment before anything is published
- The assistant has a trusted, temporary deploy tool available

Never generate a public URL silently. If deployment is not available, fall back to local HTML and explain why. `build_and_deploy.sh` is **off by default** — run it only after the user explicitly asks for a deployable folder.

## Batch Export · 批量导出（今天 / 本周）

When you're away from your computer and want **everything you made recently** readable on your phone, convert a whole folder in one pass. Triggered by "导出今天" / "导出本周" / "batch export today" **together with an explicitly named folder** — never guess a folder.

```bash
python3 md2share.py <目录>                    # 该目录下所有 .md（只扫一层）
python3 md2share.py <目录> --since=today      # 只转今天改过的
python3 md2share.py <目录> --since=week       # 只转本周（周一 00:00 起）改过的
python3 md2share.py <目录> --since=7d         # 最近 7 天
python3 md2share.py <目录> --since=2026-09-20 # 指定日期之后
python3 md2share.py <目录> <输出目录>          # 输出集中到另一个目录
```

Rules for batch mode:

- **Statically stateless.** The time filter reads each file's own modification time. No index file, no manifest, no `.md-out-of-chat/` state, nothing to go stale — this is why the skill stays a pure converter.
- **One level only.** Only `*.md` directly inside the named folder is converted. Subfolders are never walked, so pointing at a broad folder cannot cascade through your whole disk.
- **Explicit input.** The user names the folder. Do not pick a folder from history or infer it from context.
- **Output beside the source** by default (`note.md` → `note.html`), or into the second argument if given. Existing `.html` files are simply overwritten with the fresh render.
- **No silent scheduling.** This is a manual, on-demand action. The skill does not register cron jobs or background timers — if you want it to run on a schedule, that belongs to the host platform's own automation, configured by the user.
- Report the count and the list of written files so the user knows exactly what was produced.

## Mobile Responsive

- Body padding shrinks on `< 480px` width
- Container padding: 32px → 20px
- Code font shrinks: 14px → 13px
- Table font shrinks: 14px → 13px

## Privacy

- Runs **locally** by default. The core `md2share.py` only reads the input `.md` and writes a local `.html` file.
- **Batch mode is read-only on your source files.** It lists `*.md` in the folder you named, compares against each file's own modification time, and writes only `.html` output. It creates **no** state file, index, or tracking directory, and it never moves, renames, or deletes anything.
- `build_and_deploy.sh` only prepares a local `dist/` folder; it does not upload anything and is **off by default**.
- **Long-image mode reads no more than HTML mode does** — same input file, same local-image sandbox. Headless browser runs are pointed at a throwaway `user-data-dir` (never your logged-in Chrome profile), load only the local generated file via `file://`, and the profile directory is deleted afterwards.
- The privacy self-check reports **category + count only** and never prints the matched text, so scan logs cannot become a leak themselves.
- This skill never sends user content to external APIs without explicit consent, and long-image mode adds no network calls of its own (base64-embedded images stay inline; remote images are still never fetched).
- A public URL is produced **only** when the user explicitly requests it, explicitly confirms, and the assistant has a trusted deploy tool.
- **Local images** (`![alt](./image.png)`) are embedded as base64 **only** if they live in the same directory as the Markdown file or a subdirectory of it. **Absolute paths and directory traversal (`../`) are never embedded.** Image files are validated by content (magic bytes) before embedding, and every embedded file path is logged to stderr so the user can audit exactly what was read.
- **Remote images** are never fetched automatically; they are rendered as a link placeholder to avoid network requests.
- **Generated HTML is fully escaped.** All Markdown text, code content, and code-fence language labels are HTML-escaped before being written into the output page (language labels are additionally restricted to a safe character set), so untrusted Markdown cannot inject scripts into the generated page.
- The user does not need to register any account.
- This skill **never** sends user content to external APIs without explicit consent.

## Usage Example

```bash
# 1. Write or place your .md file
# 2. Generate a local HTML file (default: local images under .md dir are embedded)
python3 md2share.py my-notes.md

# 3. Long image: one PNG to forward, plus a fallback .long.html
python3 md2share.py my-notes.md --long-image

# 4. Batch: convert a whole folder, optionally only what changed recently
python3 md2share.py ~/notes --since=today

# 5. (Optional, only on explicit request) Build dist/ for deployment
./build_and_deploy.sh my-notes.md
```

## Files

- `md2share.py` — Core script (md → local html / long-image png; single file or one-level folder batch)
- `build_and_deploy.sh` — Optional local build helper (prepares `dist/`; off by default)
- `SKILL.md` — This file

## Limitations

- MD parser supports nested lists (any depth, mixed ordered/unordered) and images (local images embedded as base64 only from the Markdown file's directory or its subdirectories; absolute paths and `../` traversal are never embedded; image content is validated via magic bytes before embedding; every embedded path is logged to stderr; remote images rendered as a link placeholder so no network request is made)
- Long-image PNG requires a Chromium-family browser already on the machine; without one (or if both headless passes fail) the skill degrades to the long-image HTML and says so — it never installs or downloads a browser
- Long images are capped at 20000px height; longer documents are truncated (split the source and convert in parts)
- In long-image mode, tables and code blocks wrap instead of scrolling, external links print their URL after the text, and the TOC / theme toggle / copy buttons are omitted — all because an image cannot scroll or react
- Batch mode scans exactly one folder level (`*.md` beside each other); it does not recurse into subfolders, and it keeps no record of what it converted before — re-running simply re-renders
- Footnotes: `[^id]` refs render as superscript anchors, definitions collected into a NOTES section at the bottom with back-links
- Table of contents: when the document has 3+ h2 headings, a collapsible TOC with anchor links is generated at the top (mobile-friendly, dark-mode aware)
- Horizontal rules (`---`, `***`, `___`) render as styled dividers
- Dark mode: follows `prefers-color-scheme` with a manual toggle that remembers the choice
- Code highlighter covers python / javascript / typescript / bash / sql / java / c / cpp / go / rust / php / ruby / kotlin / swift / json / yaml / css out of the box (with common aliases: py, js, ts, sh, golang, rs, yml, kt, rb, c++); other languages render as plain text with a label
- Highlighter is regex-based (single-pass tokenize: comment → string → keyword → number, no nesting bugs)
