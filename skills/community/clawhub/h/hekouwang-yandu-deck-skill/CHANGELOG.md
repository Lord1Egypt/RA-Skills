# 更新日志 · hekouwang-yandu-deck-skill

本文件记录本 Skill 的所有版本变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`。

**变更分类**
- `功能` 新增能力 · `变更` 默认/行为调整 · `优化` 既有能力打磨 · `修复` 缺陷修正 · `移除` 删除

---

## [1.0.1]

### 变更
- **目录结构对齐官方 `anthropics/skills` 约定**：原先所有可移植副本都堆在 `reference/`（单数、且混入可执行脚本）。
  现按官方分目录——`scripts/publish.py`、`assets/templates/{deck-engine-暖黑,deck-engine-米白,home}.html`、
  `references/系统说明.md`、`examples/demo.html`。SKILL.md / README(中英) 的指针与结构树同步更新。
  注：`scripts/publish.py` 与 `assets/templates/home.html` 落地时仍须拷进同一个 `演读DECK/`（publish.py 用 `SELF/home.html` 找首页源），文档已注明。

## [1.0.0]

首个有记录的版本（此前以 git 历史维护，无 CHANGELOG）。

### 修复
- **字体路径可移植化**：① `reference/publish.py` 的 `localize()` 由写死的绝对前缀
  （硬编码家目录 + `assets/fonts/`）改为**正则 `FONT_ABS_RE`**，同时认「任意绝对路径」与未替换的
  `{{SKILL_DIR}}` 占位符，统一收成站内 `/fonts/`；② 引擎模板 `deck-engine-{暖黑,米白}.html` 的
  `@font-face` 硬编码字体路径改为占位符 `{{SKILL_DIR}}/assets/fonts/`，拷模板做 EP 时替换。
  不再绑定某台机器/用户名；同时修了 content-factory 改用 `{{SKILL_DIR}}` 占位后、源 HTML 字体前缀随机器变化会替换不中导致字体失效的隐患。

### 优化
- **SKILL.md 声明 `allowed-tools`**：收敛到本 skill 真正需要的工具集，减小越权面。

### 既有能力（首版基线）
- **演示版引擎**：零依赖（纯 CSS + 原生 JS）一屏一镜 keynote，暖黑/米白两套主色；导航（方向键/空格/点击/触屏/圆点/全屏）、自动播放、进度条、深链、`prefers-reduced-motion` 自适应。模板 `reference/deck-engine-{暖黑,米白}.html`。
- **进场动画钩子**：`.an/.bar/.tok/.draw/.grow/[data-count]` + 巨幅幽灵章节号。
- **字体自托管（零 CDN）**：`publish.py` 删外链、注入本地 `@font-face`、`pyftsubset` 子集化思源黑 4 字重 + 宋，preload 防 FOUT，`/fonts/*` 强缓存。
- **发布**：构建 `dist/` → `wrangler pages deploy` 到 Cloudflare Pages（hekouwang.pages.dev）；`MANIFEST`/`SERIES_META` 加期加系列。
- **踩坑沉淀**：dist 每构建清空、本地预览须起 http、CF 子域占用 + 本机 DNS 劫持、EdgeOne 死路、venv 移动失效、代理截断 >4MB 下载。
- 强依赖内容产线 `hekouwang-content-factory`（付费 skill，提供源文章/视觉规范/字体）；引擎可零依赖单独使用。
