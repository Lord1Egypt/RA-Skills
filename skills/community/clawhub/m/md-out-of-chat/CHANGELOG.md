# Changelog

Markdown 转手机网页 · MD Out of Chat（`md-out-of-chat`）的版本变更记录。

- 最新版本：**1.9.0**（本地，未发布）
- 发布渠道：[ClawHub](https://clawhub.ai/bonniegeng-max/skills/md-out-of-chat)
- 版本数：21（含初始版本；1.7.0 / 1.7.1 为平台卡单占号，未实际上线）

> 本文件由 ClawHub registry 的逐版本发布记录回溯整理生成（2026-09-29）。此后每次发版请在此追加一条。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.9.0] - 2026-11-17

首屏重写 + 切图去留讲清 + 隐私边界成文 + 并入「对话→能发的一页」入口。功能零变更，全部是文案与边界。

- **首屏重写（场景先行）**：原首屏第一句是「把 Markdown 文件变成手机能直接打开的单页 HTML」——在讲格式转换，没说什么时候会用。改为「和 AI 聊完，先把它写成的那堆东西拿出来」，并给三个真实场景（躺床上再读一遍 / 今天写的笔记一次全转出来 / 结论转成图发群里）。
- **「长图之后怎么办」讲明白**：长图是**一张**、小红书图文是**一组 3:4**，这是两件事。**本 skill 只出长图、不做切割**，需要图组时明确指路到切割工具；并说明不要为迁就切图额外改宽度（750px @2x 是给手机滚动阅读调的）。
- **隐私边界单独成节**（原来散在长图段里）：三条纪律——① 自检结果必须转述，只报类别与数量、不说具体内容 ② 不联网核对，本地正则跑完即弃 ③ **不提供「一键删除敏感信息」**，只报不改（自动改写会让人误以为发出去的是原件，反而更危险）。
- **新增「对话 → 能发的一页」入口段**：把「我有文件」和「我刚聊出一堆东西」两种情况并进来。明确三段分工——**落成文件是宿主 agent 的事、转成能看的是本 skill 的事、发出去要用户显式确认**。混成一段就等于把隐私边界交出去了。
- 重申定位：这一页是「给自己的确认件」，不是「给别人的排版稿」。



## [1.8.0] - 2026-11-11

新增：**长图导出**（`--long-image`）。`.md` → 一张手机可读、可直接转发的长图 PNG（默认 750px 宽 @2x），同时保留长图版 HTML 作为兜底。

- **零安装**：截图用本机已有的 Chrome / Chromium / Edge / Brave 无头模式（先常规参数、失败才补 `--no-sandbox` 重试；一次性 user-data-dir，跑完即删，不碰用户已登录的浏览器配置）。没有浏览器时自动降级为长图版 HTML，绝不下载/安装任何东西。
- **两遍渲染测高**：第一遍 `--dump-dom` 读页面内联脚本写进 `<meta>` 的 `document.body.scrollHeight`（不用 `documentElement`——它会被视口高度托底，内容短时截出一大截空白），第二遍按此高度整页截图。
- **为图重排（独立 CSS，正文仍复用同一套渲染规则）**：固定宽度、正文字号加大到 17.5px；表格与代码块由横向滚动改为折行（图片里的滚动区等于被裁掉）；目录、主题切换、复制按钮隐藏（截图里是死的假 UI）；外链把网址以灰色小字印在文字后面（图片里的链接点不动）。
- **出图前隐私自检**：扫手机号 / 身份证号 / 邮箱 / 疑似密钥（sk-、ghp_、AKIA、AIza 前缀）/ 长卡号，只报类别与数量、不打印命中原文（日志不成为泄露源）；命中时打警告但照常出图，由用户决定。
- **无水印**：页脚只有文档标题 + 生成时间。
- 批量导出兼容：`--since` 过滤可与 `--long-image` 组合；`--long-image=宽度`（480–1600）、`--png-scale=1|2|3`、`--long-html-only`。
- 超长文档 20000px 封顶并提示分段。
- 文档同步：SKILL.md / SKILL.zh.md / README 移除「本 skill 不生成图片」的绝对化表述，改为「长图模式例外 + 定位仍是阅读/转发而非绘图」。

## [1.7.2] - 2026-10-27

重发版：内容 = 1.7.0（Mermaid 摘要卡 + 批量导出 --since）+ 发布前补充（"Not the same as" 增加 baoyu-markdown-to-html 差异化段；topics 移除「公众号排版」）。1.7.0 / 1.7.1 于 10-12 / 10-27 提交后卡在 ClawHub 扫描队列未上线且占住版本号，换号重发以绕开。

## [1.7.0] - 2026-10-26

Mermaid 图表降级显示——AI 生成的 md 里常见的流程图/时序图，手机端不再显示为一段裸代码。

- 识别 ` ```mermaid ` 代码块，渲染为专属「图表摘要卡」：图表类型徽章（流程图 / 时序图 / 甘特图等 20 种）、源码行数、图内节点文本 chips、可折叠源码 + 复制按钮
- 纯正则结构抽取，不执行图表代码、不加载外部渲染库、不上传任何内容，保持"本地、零依赖"原则
- 复用现有 copy-btn 交互与暗色主题；暗色态样式选择器加权避免被通用规则覆盖
- 普通代码块行为完全不变

## [1.6.1] - 2026-09-29

发布元数据修复，文件内容与行为无变化。

- 恢复 ClawHub 显示名为 `Markdown 转手机网页 · MD Out of Chat`。1.6.0 发布时未带 `--name`，ClawHub 回退成裸 slug，中文检索面丢失。
- 发版提醒：**务必带 `--name "Markdown 转手机网页 · MD Out of Chat"`**，命令为 `clawhub publish --name "Markdown 转手机网页 · MD Out of Chat" --slug md-out-of-chat --version <v>`。

## [1.6.0] - 2026-09-29

批量导出（轻量版）—— 一次把一个目录里「今天 / 本周」改动过的 `.md` 转成手机可读页面。

- `md2share.py`：第一个位置参数可以是**目录**，只扫一层 `*.md`，逐个渲染为同目录同名 `.html`；第二个位置参数为可选输出目录
- 新增 `--since=today|week|7d|YYYY-MM-DD`：按**文件自身修改时间**筛选，**不写任何状态文件、索引或跟踪目录**
- 批量模式只新增/覆盖 `.html`，对源 `.md` 严格只读，不移动/改名/删除；不递归子目录
- 明确"手动触发"边界：skill 不注册定时任务，定时属于宿主平台能力
- SKILL.md 新增 Batch Export 章节 + 触发条件补「批量导出需用户明确指定文件夹」；README 同步；description 补批量触发词
- 单文件调用方式与输出行为完全不变（向后兼容）

- 新增本 CHANGELOG.md，回溯整理 0.1.0 → 1.5.3 的历史版本记录（内容取自 ClawHub 逐版本发布记录，未改动代码）

## [1.5.3] - 2026-09-13

discoverability fix — categories and topics now set (was 'other'); description leads with a bilingual problem statement plus a Not-for clause; SKILL.md gains When-not-to-use / How-it-differs sections. No behavior change.

## [1.5.2] - 2026-09-07

md-out-of-chat v1.5.2

- Clarified activation rules: the skill now requires both explicit mention by name and explicit identification of an input file.
- Updated privacy and deployment instructions: never infer targets from chat history or invoke deployment/tools unless the user separately requests and confirms.
- Documentation improved to emphasize safety, explicit user consent, and strict scoping of file access.
- No functional/code changes; this is a documentation and behavior clarification release.

## [1.5.1] - 2026-09-07

- Improved HTML escaping for security: all Markdown text, code content, and code-fence language labels are now fully escaped to prevent injection of untrusted scripts into generated pages.
- Language labels in code blocks are further restricted to a safe character set.
- Updated privacy section to clarify HTML escaping and script-injection mitigation.
- Removed obsolete skill-card.md file.

## [1.5.0] - 2026-09-06

Differentiation release: syntax highlighting for 17 languages with aliases; auto-generated collapsible TOC for long documents. Security: image embedding fully sandboxed (all-mode removed, legacy flag deprecated), magic-bytes content validation, build script requires --force to wipe dist/.

## [1.4.0] - 2026-09-06

Security hardening: absolute local paths are never embedded as base64; --embed-local-images=all only relaxes relative traversal and every embedded path is logged to stderr. Docs aligned with implementation (no screenshot claims). SEO: keyword-rich description.

## [1.3.2] - 2026-08-30

Remove the bundled browser automation helper (screenshot.sh). Screenshots are now rendered by the host environment's own tools. Core converter unchanged.

## [1.3.1] - 2026-08-30

Sandbox local image embedding: default mode only embeds images inside the .md directory or its subdirectories; absolute paths and ../ traversal require --embed-local-images=all.

## [1.3.0] - 2026-08-30

Footnotes ([^id] superscript refs + bottom NOTES section with back-links, paper-friendly), styled horizontal rules (---/***/___), dark mode (follows system preference + manual toggle with saved choice)

## [1.2.0] - 2026-08-30

Nested lists (any depth, mixed ordered/unordered), image support (local files embedded as base64, remote images as link placeholder - no auto network request), no duplicate h1 when content already has a title, screenshot.sh auto-detects Chrome on macOS/Linux

## [1.1.4] - 2026-08-29

Fix security review findings: remove auto_push.sh, network-isolate screenshot.sh, narrow activation triggers, default to local HTML, update privacy claims

## [1.1.3] - 2026-08-29

Add clawdbot metadata JSON to SKILL.md; keep skill-card.md for review

## [1.1.2] - 2026-08-29

Publish with source-repo metadata so ClawHub can fetch skill-card.md

## [1.1.1] - 2026-08-29

Add skill-card.md for ClawHub security review; no functional changes

## [1.1.0] - 2026-08-29

Fix syntax-highlight span nesting bug; copy button reads from DOM (halves page size); add blockquote, ordered lists, task lists, styled links, inline formats and pipe escape in table cells; portable build script

## [1.0.0] - 2026-08-29

Initial publish: md to mobile-friendly HTML/screenshot skill

## [0.1.0] - 2026-08-29

Initial release — renders Markdown (.md) files into mobile-friendly web pages or images for easy sharing and viewing, especially in chat apps.

- Converts .md files to either public web URLs or phone-sized PNG screenshots.
- Web view is fully responsive: clean typography, beautiful tables, syntax-highlighted code, and mobile-first layout.
- Smart output selection: defaults to web for convenience, switches to screenshot only when clearly requested or needed.
- No cloud uploads for privacy; everything runs locally except for optional temporary link sharing.
- Simple, reliable, and designed specifically for chat and Chinese/overseas sharing scenarios.
