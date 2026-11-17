# 更新日志 · hekouwang-yandu-deck-skill

本文件记录本 Skill 的所有版本变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`。

**变更分类**
- `功能` 新增能力 · `变更` 默认/行为调整 · `优化` 既有能力打磨 · `修复` 缺陷修正 · `移除` 删除

---

## [1.3.5] - 2026-11-10

### 修复（ClawHub 复查）
- 部署强制 `YANDU_CF_PROJECT` 与 `wrangler.toml name` 一致，并用 `--project-name` 显式指定，避免发错站
- 留言板改表说明补「DROP 会删光已有留言，先备份」警告

## [1.3.4] - 2026-11-10

### 修复（ClawHub 复查）
- description / openclaw 明确声明可选留言板（访客昵称、正文、IP 哈希）与分析 token
- 留言板默认关闭：需 `YANDU_ENABLE_COMMENTS=1` 才注入页面
- 引擎模板与首页去掉 Google/loli 字体 CDN，改为自托管 `/fonts/` 声明

## [1.3.3] - 2026-10-15

### 修复（ClawHub 安全审查）
- `publish.py` 去掉硬编码的 Cloudflare Web Analytics token：改读 `YANDU_CF_BEACON_TOKEN`，留空不注入（此前同步真身时把 1.2.x 的去账号化覆盖掉了）
- `sync-from-harness.sh` 同步后检查账号绑定值与自动全局安装，命中即中止
- 留言板 IP 哈希盐改读 Pages 密钥 `IP_SALT`

### 变更
- `publish.py` 默认只构建，`--deploy` 才部署；项目名取 `YANDU_CF_PROJECT`，不再写死
- 不再自动 `npm i -g wrangler`，缺失时提示用户自行安装并锁版本
- SKILL.md：部署前需用户确认；披露 `home.html` 为作者站首页样例；片尾 CTA 改为可替换，不强制站外导流
- 留言板页脚去掉作者 GitHub 推广链，改为本站 D1 说明
- frontmatter 补 `metadata.openclaw`（bins / envVars）

### 移除
- `publish.py` 中未被调用的 `write_index()`（含作者私域 CTA）

## [1.3.2] - 2026-08-12

### 变更
- ClawHub 分类：`creative`

## [1.3.1] - 2026-08-12

### 优化
- README：30 秒验收 + 免费/付费表 + @huiyonghkw CTA
- summary 补英文 SEO 关键词（keynote deck / Cloudflare Pages）

## [1.3.0] - 2026-08-12

### 功能
- **`scripts/sync-from-harness.sh`**：从 harness `演读DECK/` 单向同步 `publish.py`、`home.html`、留言板模板到 skill 副本。

### 优化
- **副本追平真身**：`publish.py` 802 行与 harness 对齐（含 Harness 工程系列 / FastMCP / 股票识字等 MANIFEST）。
- **`references/mobile-and-comments.md`**：移动端 safe-area、留言板禁用步骤、与 HyperFrames 视频产线分工。

## [1.2.1] - 2026-08-12

### 变更
- **品牌人设对齐 memory `brand-persona-tagline`**：首页 `home.html` 与 `publish.py` 内嵌 about 段，
  「真会用 AI 的程序员」→ **「会勇禾口王 = AI 工作流 builder」**；补「会勇」谐音「会用」梗。
- about 文案微调：强调「不靠 PPT 教人，先在自己电脑上跑通再把 Skill 交到你手上」。

## [1.2.0]

### 修复
- **捆绑副本追平真身（本次最大的洞）**：skill 里的 `publish.py`（511 行）已落后项目真身（735 行）——**SKILL.md 白纸黑字写着「publish.py 已支持 Mozilla 字体打包」，而副本里 "mozilla" 出现 0 次**；`home.html` 也只有真身的一半（314/657）。已全量同步，并补上从未随 skill 分发的留言板子系统。承诺现在兑现得了。
- **主色口径追平线上**：description 与 第1.4节 还写着「暖黑/米白两套主色」，实际线上已是四套并存。**推测缺件正是漂移的成因**——占大头的 V6 焰彩黑没有模板（黑版是 flip 出来的），新 EP 无黑版可拷只能退回老模板，Harness（暖黑）/ 出行SaaS（米白）就是这么来的。
- **陈旧引用**：兄弟 skill 名补 `-skill` 后缀（真实目录是 `hekouwang-content-master-skill`，旧名照着找会扑空）；`ROOT` 注释里的旧项目名 `Pi.dev/`；`references/系统说明.md` 里的「后续会升级成 Skill」（早就是了）。
- **第2节 首页描述**：主色暖黑 → **米白**（2026-07-14 已改），系列卡「两个」→ **五个**，并点明系列卡是**静态手写**、不由 MANIFEST 生成（`write_index()` 是遗留死函数），加系列须三处一起动。

### 功能
- **留言板随 skill 分发**（`references/留言板-D1.md` + `assets/functions/api/comments.js` + `wrangler.toml` + `schema.sql`）：CF Pages Functions + D1，按页隔离，留言存自己的 CF 账号、无第三方。含建库三步、已有防护（限频/蜜罐/XSS/路径注入）、部署三坑（配置式部署不带 dist 参、验证跟随 308、curl 加 `--noproxy`）。
- **换肤专题**（`references/换肤-token-flip.md`）：白↔黑 token-flip 映射表 + 三条验收 + 六个坑。含「**原地覆盖脚本先读后写**」——`open(dst,'w')` 会先把文件截断成空，曾把 9 期全写空。

### 变更
- **第1.4节 主色规矩改为「米白是全站默认，V6 焰彩白是国标专属例外」**；暖黑 / V6焰彩黑降为**存量历史态、不再新做**（存量按计划 flip 回米白）。`deck-engine-暖黑.html` 仅为维护存量保留，标注「新 EP 别拷」。故**不再补 V6焰彩黑模板**——补了等于鼓励继续新做。

### 优化
- **副本去账号化**（skill 是公开分发的）：`CF_BEACON_TOKEN` 置空（留空则不注入 beacon，降级干净）、`wrangler.toml` 的 `database_id` 改占位符。否则别人用这个 skill 建的站，流量统计报到作者面板、留言写进作者的库。
- **删死代码**：`FONT_ABS_PREFIX` 指向一个不存在的目录（少 `-skill` 后缀），真正干活的是 `FONT_ABS_RE`。已删常量、采用 skill 版更通用的正则（同时认 `{{SKILL_DIR}}` 占位符与任意绝对路径，覆盖 Anthropic + Mozilla）。
- **第0节 加防漂移提示**：点明「项目里的是真身、skill 里的是副本，改完记得同步回来」，并记下这次漂移作为前车之鉴。

## [1.1.0]

### 功能
- **放映 / 提词器模块**（`assets/presenter/presenter-module.html`，第1.6节）：按 `S` 开「讲者视图」独立窗口——计时器 + 当前镜逐字稿 + 下一镜预览。主屏与讲者窗靠 **BroadcastChannel 双向同步**，**主屏保持干净可投影/录屏**；弹窗被拦（或无 BroadcastChannel）自动回退页内浮层。
- **真·双屏 + 反向遥控**：第二显示器另开 deck 窗口加 `?speaker=1` 即变讲者窗（免弹窗，`window.name`/`?speaker` 识别，绕开引擎深链冲 hash）；讲者窗按 `←/→` 遥控主屏翻镜、`P/R` 控计时（向主屏引擎派发方向键事件，不改引擎）。键位 `S/P/R/Esc`。
- 逐字稿写进每张 `.slide` 的 `<div class="notes">`（观众/录屏永不可见），**同时即该镜的配音/口播脚本**，可照念或喂 TTS——「演示稿 + 提词器 + 口播稿」三合一。
- 已注入两套引擎模板（暖黑/米白）与 `examples/demo.html`，拷模板即带，无需改引擎；靠 `.active` class（MutationObserver）与引擎解耦。无头截图验证浮层渲染通过。

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
  不再绑定某台机器/用户名；同时修了 content-master-skill 改用 `{{SKILL_DIR}}` 占位后、源 HTML 字体前缀随机器变化会替换不中导致字体失效的隐患。

### 优化
- **SKILL.md 声明 `allowed-tools`**：收敛到本 skill 真正需要的工具集，减小越权面。

### 既有能力（首版基线）
- **演示版引擎**：零依赖（纯 CSS + 原生 JS）一屏一镜 keynote，暖黑/米白两套主色；导航（方向键/空格/点击/触屏/圆点/全屏）、自动播放、进度条、深链、`prefers-reduced-motion` 自适应。模板 `reference/deck-engine-{暖黑,米白}.html`。
- **进场动画钩子**：`.an/.bar/.tok/.draw/.grow/[data-count]` + 巨幅幽灵章节号。
- **字体自托管（零 CDN）**：`publish.py` 删外链、注入本地 `@font-face`、`pyftsubset` 子集化思源黑 4 字重 + 宋，preload 防 FOUT，`/fonts/*` 强缓存。
- **发布**：构建 `dist/` → `wrangler pages deploy` 到 Cloudflare Pages（hekouwang.pages.dev）；`MANIFEST`/`SERIES_META` 加期加系列。
- **踩坑沉淀**：dist 每构建清空、本地预览须起 http、CF 子域占用 + 本机 DNS 劫持、EdgeOne 死路、venv 移动失效、代理截断 >4MB 下载。
- 强依赖内容产线 `hekouwang-content-master-skill`（付费 skill，提供源文章/视觉规范/字体）；引擎可零依赖单独使用。
