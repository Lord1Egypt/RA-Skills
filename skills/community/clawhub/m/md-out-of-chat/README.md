# md-out-of-chat

> **一句话定位**：纯本地、零依赖的 Markdown 转换器——把一个 `.md` 变成手机浏览器能直接打开、能直接发出去阅读的网页 / 长图；内容全程不离开你的电脑，无需 API Key、云账号或任何外部服务。

> **Pulling Markdown out of chat, into something people can actually read.**
> **把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

---

## 30-Second Pitch · 30 秒介绍

**中文**：在 IM 里（微信/飞书/Slack）跟 AI 聊，AI 给你写了一份 markdown，**但手机端根本看不了**。这个 skill 解决的就是这个 —— 把 .md 转成手机浏览器能直接打开的本地网页版：表格对齐、代码带语言标签 + 一键复制。告诉你的 AI "用 md-out-of-chat 转换这份 md"，**它生成一个本地 HTML 文件，手机上点开就能看**。本地跑，数据不外传。

**English**: Ever get a Markdown file in chat and not be able to read it on your phone? Code breaks, tables misalign, you can't copy a snippet. This skill turns any `.md` file into a mobile-friendly web page with proper tables, syntax-highlighted code blocks, and one-tap copy. Just say "use md-out-of-chat to convert this" to your AI agent, and you get a local HTML file that opens in any phone browser. Local by default, no data uploaded.

---

## The Problem · 问题

You (or your AI agent) wrote something in Markdown. It's sitting in your chat — WeChat, Feishu, Slack, Discord, iMessage, Telegram — and **you can't actually read it on your phone**.

- Code blocks lose indentation and break lines
- Tables misalign into a single column
- Long text scrolls forever
- You can't copy a snippet without manual selection

你在 IM 里（微信、飞书、Slack、Discord……）跟 AI 写了一份 `.md`，**但手机端根本看不了**：
- 代码错位、缩进丢失
- 表格对不齐
- 长文本滚不动
- 想复制一段代码 = **得手选每一行**

---

## The Fix · 解决

Run the file through this skill. It produces:

把文件过一遍这个 skill，你得到：

- **A local HTML file** — opens in any mobile browser, with proper tables, code blocks with language labels and **one-tap copy**

- **A share-ready long-image PNG** (v1.8.0) — one image to forward: `python3 md2share.py note.md --long-image`

- **一个本地 HTML 文件** — 任何手机浏览器都能打开，表格对齐、代码带语言标签 + **一键复制**

- **一张能直接转发的手机长图**（v1.8.0）— `--long-image` 一条命令出图

A public web URL is only generated when you explicitly ask for it and your agent has a trusted deploy tool.

---

## What md2share Produces · 输出效果

Try it on a sample file: see `demo.md` for the input.

- **Live web demo**: [Click to view](https://2uf0a7axwwwr.space.minimaxi.com) (h1/h2 headings, code blocks with language labels, copy buttons, mobile-friendly tables)
- **Long screenshot**: see `demo.png` in this repo (a 750×2750 phone-shaped snapshot, Chinese + English fully rendered)

| Element | Input (Markdown) | Output (HTML) |
|---------|------------------|----------------------------|
| Heading | `# Title` | Blue title with bottom border |
| Table | `\| col \| col \|` | Zebra-striped, mobile-friendly |
| Code | ` ```python ` | Dark header with language label, syntax highlight, one-tap copy |
| Chinese | `你好，世界` | Renders correctly (Noto CJK fonts pre-installed) |

| Element | Input (Markdown) | Output (HTML) |
|---------|------------------|---------------|
| Heading | `# Title` | Blue title with bottom border |
| Table | `\| col \| col \|` | Zebra-striped, mobile-friendly |
| Code | ` ```python ` | Dark header with language label, one-tap copy button |
| List | `- item` | Bulleted with proper spacing |

> **语法高亮支持范围（如实标注）**：`md2share.py` 内置 **17 种语言**的词法高亮——`python` / `javascript` / `typescript` / `bash` / `sql` / `java` / `c` / `cpp` / `go` / `rust` / `php` / `ruby` / `kotlin` / `swift` / `json` / `yaml` / `css`（关键字 + 注释 + 字符串 + 数字着色），并支持常用别名（`py`、`js`、`ts`、`sh`、`golang`、`rs`、`yml`、`kt`、`rb`、`c++` 等自动映射）。未列出的语言不会高亮：仍显示大写语言标签 + 一键复制按钮，内容退化为纯文本渲染（仅字符串/数字做简单着色）。

> **如何替换成你自己的案例**：把仓库根目录的 `demo.md` 换成你自己的 Markdown，`python3 md2share.py 你的文件.md` 生成 HTML 后（用宿主截图工具）另存为同名 `demo.png`；文件名保持不变，上面这些引用就会自动指向你的产物。

---

## How to Use · 怎么用

Once installed, talk to your AI agent with an explicit skill mention **and a concrete file**:

> "用 md-out-of-chat 把 `notes.md` 转成 HTML"
> "use md-out-of-chat to convert `report.md`"
> "把 `demo.md` 转成手机能看的 HTML"

**Trigger contract · 触发契约：**

- This skill only runs when the user names it explicitly AND identifies a concrete `.md` file (a path, an attached file, a file selected in the conversation) — or, for batch export, a named folder.
- The agent must **not** infer conversion targets from chat history, pick a folder on its own, or act on vague phrases like "转一下" / "convert this".
- Only the file(s) the user explicitly identifies are read; nothing else is touched.
- A public URL is **never** generated unless the user separately requests deployment AND confirms it.

The agent decides the right output based on your explicit request:

| 场景 · Scenario | 输出 · Output |
|-----------------|---------------|
| 没有特别说明 · No specific output requested | 本地 HTML · Local HTML file |
| "出长图 / 手机长图 / 转成长图" · "long image" | **长图 PNG（750px @2x）+ 兜底长图版 HTML** · Long-image PNG + fallback HTML（v1.8.0） |
| "公开链接/URL" 且有部署工具 · "public link/URL" with deploy tool | Web URL（需用户明确确认 · requires explicit confirmation） |
| "发给朋友" · "send to friend" | 长图 PNG 或 HTML，拿去就能转发 · Long-image PNG or HTML, ready to forward |

The default is always local-first. A public URL is never generated silently.

### Long image export · 长图导出（v1.8.0）

聊完的东西想直接转给朋友？一张长图比一段文本好用：微信里发图即读、排版不散、相册能存。

```bash
python3 md2share.py note.md --long-image            # 长图 PNG（750px @2x）+ 兜底 HTML
python3 md2share.py note.md --long-image=640        # 自定义宽度（480–1600）
python3 md2share.py ~/notes --since=today --long-image   # 批量长图
```

- **零安装 · Zero installs** — 截图用本机已有的 Chrome / Chromium / Edge / Brave 无头模式（只找，绝不下载安装）；没有浏览器就只出长图版 HTML，自己在浏览器里整页截图也行。 Uses a Chromium-family browser already on the machine; without one it degrades to the long-image HTML and says so.
- **为图重排 · Re-layouted for images** — 固定宽度、字号加大；表格和代码改为折行（图片里滚动区等于被裁掉）；目录 / 主题切换 / 复制按钮隐藏（截图里是死的假 UI）；外链把网址印在文字后面（图片里的链接点不动）。 Tables and code wrap instead of scrolling; TOC, theme toggle and copy buttons are omitted; external links print their URL.
- **出图前隐私自检 · Privacy gate** — 自动扫手机号 / 身份证 / 邮箱 / 疑似密钥 / 长卡号，只报类别和数量（不打印原文）。长图比文本更容易被随手转发，命中时先提醒再出图。
- **无水印 · No watermark** — 页脚只有文档标题和生成时间。

### Batch export · 批量导出（v1.6.0）

Away from your computer and want **everything you made today** readable on your phone? Point it at a folder:

> "用 md-out-of-chat 导出今天，文件夹 `~/notes`"
> "用 md-out-of-chat 导出本周 `~/projects/diary`"

```bash
python3 md2share.py ~/notes                   # 该目录下所有 .md（只扫一层）
python3 md2share.py ~/notes --since=today     # 只转今天改过的
python3 md2share.py ~/notes --since=week      # 本周（周一 00:00 起）
python3 md2share.py ~/notes --since=7d        # 最近 7 天
python3 md2share.py ~/notes ~/readable        # 输出集中到另一个目录
```

- **无状态**：时间过滤直接读文件自身的修改时间，不生成任何索引/清单/跟踪文件。
- **只扫一层**：只转该目录下的 `.md`，不递归进子目录——指错文件夹也不会滚遍整个硬盘。
- **手动触发**：本 skill 不注册定时任务；要"每天自动跑"属于宿主平台的自动化能力，由你自己配置。
- **只读源文件**：仅新增/覆盖 `.html`，绝不移动、改名或删除任何东西。

---

## Install · 安装

This is a standard skill. Drop the folder into your agent's skills directory:

标准 skill。把文件夹放到 agent 的 skills 目录：

| Agent | Path |
|-------|------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| GitHub Copilot | `.github/skills/` (per repo) |

```bash
cp -r md-out-of-chat ~/.claude/skills/
```

The agent picks it up automatically. No registration, no API key, no cloud account.

agent 自动识别。**不用注册、API key、云账号**。

---

## Who This Is For · 适合谁

- **You live in chat with your AI** — WeChat, Feishu, Slack, Discord, iMessage, Telegram
- **Your AI writes Markdown** — research summaries, code snippets, comparison tables, strategy docs
- **You read on your phone** — and Markdown doesn't render well there
- **You want copy-able code** — not screenshots of code

你跟 AI 在 IM 里聊、**AI 用 markdown 给你写东西**、**你在手机上看**、**想复制代码**。

Not for: pure desktop workflows, or if you never read on mobile.

不适合：纯桌面工作流，或者你从来不在手机上看。

---

## What Makes It Different · 跟别的区别

There are other "md to html" skills (`awesome-copilot/markdown-to-html`, `haidang1810/md2html`). md-out-of-chat is different because:

- **Built for IM** — not for "I want to publish a blog post". The output is sized for chat-shared links.
- **Local-first** — default output is a local HTML file; public URL only with explicit opt-in.
- **Copy button on every code block** — read the code on your phone, copy with one tap.
- **Multi-agent** — same SKILL.md works for Claude Code, Codex, OpenClaw, Copilot, etc.
- **No analytics, no cloud, no login**.

---

## Files · 文件

- `SKILL.md` — English spec (the one the agent reads)
- `SKILL.zh.md` — 中文 spec (你读这个)
- `md2share.py` — the core script: md → local mobile-friendly HTML
- `build_and_deploy.sh` — helper to build a local `dist/` folder
- `demo.md` — a tiny example to test with
- `LICENSE` — MIT
- `README.md` — 你现在看的这个

---

## Privacy · 隐私

- **Local by default** — `md2share.py` only produces a `.html` file. Nothing leaves your machine unless you explicitly ask for a public URL.
- **No browser automation shipped** — the skill generates HTML only and contains no Puppeteer/Chrome code; no PNG output.
- **Web deploy is opt-in** — only when you explicitly request it, explicitly confirm, and your agent has a trusted deploy tool.
- **Sandboxed local images** — local images are embedded as base64 only when they live in the same directory as the `.md` file or a subdirectory of it. **Absolute paths and `../` traversal are never embedded.** Image content is validated via magic bytes before embedding, and every embedded file path is logged to stderr for auditing.
- **Remote images never auto-fetch** — they render as a link placeholder, so no network request is made.
- **No telemetry** — the script does not phone home.

- **默认本地跑** — `md2share.py` 只生成 `.html` 文件，**数据不出你电脑**
- **不内置浏览器自动化** — skill 只生成 HTML，不含 Puppeteer/Chrome 代码，不输出 PNG
- **公开链接需明确授权** — 只有在你明确要求、明确确认、且有可信部署工具时才生成
- **本地图片沙箱** — 只有与 `.md` 同目录或其子目录下的图片才会内嵌为 base64；**绝对路径和 `../` 遍历一律不内嵌**；内嵌前按文件头校验真实类型，每个内嵌路径都打到 stderr 供审计
- **远程图片不自动下载** — 只渲染为链接占位，不会发起网络请求
- **无任何统计上报**

---

## Status · 状态

✅ Core features done:
- 标题 / 段落 / 表格 / 代码块（带语言标签 + 语法高亮）/ 列表 / 粗体 / 斜体
- 引用 blockquote / 有序列表 / 任务列表 `- [ ]` / 链接样式化
- 表格 cell 内联格式（粗体/斜体/行内代码/链接）+ `\|` 转义
- 代码块一键复制按钮（3 状态：Copy → Copying... → Copied! → 2 秒回 Copy）
- 语法高亮重写为单遍 tokenize（注释→字符串→关键字→数字），修复了字符串内关键字误高亮和 span 嵌套错乱
- 默认本地 HTML 输出，公开链接需用户明确授权
- 蓝白灰简约风格
- 移动端适配
- 中文字体（Noto CJK）
- 嵌套列表（任意层级，有序/无序混排）
- 图片支持：本地图片内嵌 base64（离线可看），沙箱到 .md 同目录及子目录，绝对路径和 `../` 一律不内嵌，内嵌前校验文件头类型并打印内嵌路径；远程图片渲染为链接占位（不自动发请求，保护隐私）
- 正文自带 `# 标题` 时不再叠加文件名标题
- 截图输出由宿主环境自带工具完成（v1.3.2 起不再内置 screenshot.sh，避免浏览器自动化代码）
- 脚注 `[^id]`：正文渲染为上标角标，可点击跳转，底部 NOTES 区汇总并支持回跳（论文/技术文档友好）
- 分隔线 `---` / `***` / `___` 渲染为渐变样式分隔线
- 暗色模式：跟随系统 `prefers-color-scheme`，右上角可手动切换并记住选择

🟡 Coming next:
- Mermaid 图表渲染

---

## Why "out of chat"? · 为什么叫 "out of chat"

Because that's exactly what it does. Markdown **lives well** in chat (AI writes it freely), but **dies** in chat rendering. This skill gets it out, into somewhere a human can actually read it.

因为这就是它做的事。Markdown **在聊天里写得很爽**（AI 信手拈来），但在聊天里**渲染得很惨**。这个 skill 把它拿出来，放到一个人能好好看的地方。

---

## License

MIT — see `LICENSE`.
