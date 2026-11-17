---
name: hekouwang-yandu-deck-skill
slug: hekouwang-yandu-deck-skill
displayName: 演读 DECK 产线与发布
summary: Immersive keynote-style HTML deck publisher — flip pages, auto-play, Cloudflare Pages. yandu-deck / hekouwang.pages.dev.
license: MIT
homepage: https://github.com/huiyonghkw/hekouwang-yandu-deck-skill
version: 1.3.6
description: "演读 DECK：把文章做成可翻页可自动播放的 keynote 网页，自托管字体并发布到 Cloudflare Pages；可选启用访客留言板（D1 存昵称/正文/IP 哈希）与站点分析 token"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
metadata:
  openclaw:
    homepage: https://github.com/huiyonghkw/hekouwang-yandu-deck-skill
    requires:
      bins:
        - python3
      anyBins:
        - node
        - wrangler
    envVars:
      - name: YANDU_CF_PROJECT
        required: false
        description: Cloudflare Pages 项目名；仅 --deploy 时必填
      - name: YANDU_CF_BEACON_TOKEN
        required: false
        description: Cloudflare Web Analytics token；留空则不注入统计脚本
      - name: YANDU_ENABLE_COMMENTS
        required: false
        description: 设为 1/true 才向页面注入留言板；默认关闭
      - name: IP_SALT
        required: false
        description: Pages 密钥，用于留言 IP 哈希限频
---

# 演读 DECK · 沉浸式演示产线与发布

> 「演读 DECK」= 会勇禾口王的AI笔记出品的一款**沉浸式阅读产品**：介于长文和视频之间的第三种读法——一屏一镜、方向键/空格/点击翻页、能自动播放，把一个复杂主题安静完整地讲给你看。
> 线上：**https://hekouwang.pages.dev** ｜ 与图文产线 `hekouwang-content-master-skill` 配套（那是出文章/贴图/视频，这是把内容做成翻页演示 + 发布）。

## 0. 系统在哪（先认这个）

发布系统是项目里一个**自包含目录** `<项目根>/演读DECK/`：

```
演读DECK/
├── publish.py       # 发布脚本：构建 dist/ → 部署 CF Pages（零三方依赖，仅标准库 + 一个子集化 venv）
├── home.html        # 首页源（改首页改这个；dist/ 每次构建会清空，别在里面改）
├── wrangler.toml    # CF Pages 配置 + D1 绑定（留言板用；不做留言板可删）
├── schema.sql       # 留言板 D1 表结构
├── functions/api/comments.js   # 留言板后端（Pages Functions，按目录约定生效）
├── fonts/src/       # 字体源：思源黑 NotoSansSC-{400,500,700,900}.woff2 + 宋 -700 + Anthropic Sans/Mono + Mozilla VF
├── fonts/cache/     # 子集化产物缓存（无字体源/无 venv 时回退）
├── tools/fenv/      # 子集化 venv(fonttools+brotli)；移动会失效，丢了重建
├── dist/            # 构建产物 = 部署目录（可整删重生）
└── README.md
```

> ⚠️ **上面这套是「真身」，本 skill 里的是可移植副本**。日常在项目里改的是真身；**改完跑 `bash scripts/sync-from-harness.sh <演读DECK路径>` 同步回 skill**，否则副本很快过时。

本 Skill 按官方约定分目录带了**可移植副本**（新项目落地时拷过去）：
- `assets/templates/` — `deck-engine-米白.html`（⭐默认）/ `deck-engine-V6焰彩白.html`（国标）/ `deck-engine-暖黑.html`（仅维护存量）、`home.html`（首页源）、`wrangler.toml` + `schema.sql`（留言板，**database_id 是占位符，落地填自己的**）
- `scripts/publish.py`（发布脚本）、`scripts/sync-from-harness.sh`（真身→副本单向同步）、`assets/functions/api/comments.js`（留言板后端）
- `references/换肤-token-flip.md`（换肤）、`references/留言板-D1.md`（留言板）、`references/mobile-and-comments.md`（移动端 safe-area / 留言板开关 / 视频交叉引用）、`references/系统说明.md`（**落地 README 模板**，拷进 `演读DECK/README.md` 给人看）、`examples/demo.html`（零依赖最小示例）

> ⚠️ **落地时 `publish.py` 与 `home.html` 必须同目录**（`publish.py` 用 `SELF/home.html` 找首页源）；`functions/` 要放成 `演读DECK/functions/api/comments.js`。
> ⚠️ 副本里**不带任何账号绑定值**：统计 token 取 `YANDU_CF_BEACON_TOKEN`（留空则不注入统计脚本）、Pages 项目名取 `YANDU_CF_PROJECT`、`wrangler.toml` 的 database_id 是占位符、留言 IP 哈希盐取 Pages 密钥 `IP_SALT`。落地新站时填自己的，别沿用他人的。`sync-from-harness.sh` 同步时会拦下带账号值的真身。
> ⚠️ `assets/templates/home.html` 是作者站点的首页样例，含作者署名、联系方式与订阅引导；落地前替换成你自己的。

## 1. 把文章做成「演示版 deck」⭐ 核心

一篇 V2 文章 → 一屏一镜的 keynote。**零依赖（纯 CSS + 原生 JS，不引 GSAP/外链，国内/CF 都快）。** 沿用源文章的视觉（默认米白，国标走 V6 焰彩白，见 第1.4节）、字体、grain/mesh/frame/幽灵章节号。

### 1.1 引擎（照抄模板，别重写）

样板（**默认拷米白**，选哪套见 第1.4节）：
- `assets/templates/deck-engine-米白.html` — ⭐ **默认**，人文/方法论亮调。
- `assets/templates/deck-engine-V6焰彩白.html` — 国标系列专属：紫主色+焰橙/粉，Mozilla 可变字体（`publish.py` 的 `MOZILLA_FILES` 已打包 Mozilla 字体、按页面含 "Mozilla" 注入 `PRELOAD_LINKS_V6`）。
- `assets/templates/deck-engine-暖黑.html` — 🕰️ 仅维护存量（Harness），**新 EP 别拷**。
**做新 EP = 拷一份对应主色的模板，`<head>` 的全部 CSS 和 `</main>` 之后的全部 `<script>` 逐字保留，只换内容 slide / 顶栏标签 / title / 片尾。** 引擎已实现：

> ⚠️ 模板 `@font-face` 里的字体路径是占位符 `{{SKILL_DIR}}/assets/fonts/...`——指向兄弟 skill `hekouwang-content-master-skill` 的字体。拷模板做 EP 时**把 `{{SKILL_DIR}}` 替换成 hekouwang-content-master-skill 的绝对 Base directory**（本地预览/截图才有字体）。发布时 `publish.py` 会把它统一收成站内 `/fonts/`，万一漏替换也能兜底。

- 全屏 `.slide`（一屏一镜），`.stage` 居中 + JS `fit()` 等比缩放防裁切；
- 导航：←/→/空格/点击/触屏滑动/底部圆点/Home/End/F 全屏；右下「▶ 自动播放」(7s/屏，像放视频)；顶部进度条 + `NN/总数`；`#N` 深链（可分享到某屏）；`prefers-reduced-motion` 自动关动画。
- **S 放映 / 提词器**（讲者视图：计时器 + 当前镜逐字稿 + 下一镜预览，详见 第1.6节）。模板已内置该模块，拷模板即带。

### 1.2 进场动画钩子（只加 class + `--i` 递增控错峰，CSS 已定义）

| 钩子 | 效果 | 用在 |
|---|---|---|
| `.an` / `.an.scale` | 淡入上浮 / 带放大 | 任何要进场的块；按出现顺序 `style="--i:0"`、`--i:1`… |
| `.bar` | 横向条 scaleX 从左生长 | 柱状/条形数据条（只给数据条，不给坐标轴） |
| `.tok` | SVG 节点组逐个淡入 | 流程/关系/漏斗/桥的节点 `<g>` |
| `.draw` | 折线/箭头描线(JS getTotalLength) | 连接线 `<line>`/`<path>` |
| `.grow` | 弹性放大 | stat 数据卡 |
| `[data-count]`+`data-suffix` | 纯数字 0→N 滚动 | 纯数字读数（初始文本写 `0`；**含箭头/汉字/百分号的别用**） |

每个 slide `data-g="章节号"` → 背景自动生成巨幅幽灵数字（封面/速览/片尾用 `data-g="·"`）。

### 1.3 内容映射铁律（一图一镜）

源文每个 section + 每张图表都要有对应镜头。**封面屏 + 速览屏（用源文 hero 的关键数据做 readout 仪表条）打头，片尾签收卡收尾**（默认选题征集；作者自有 CTA 可替换，不强制站外导流），一篇 9 节 → 约 12–24 屏。
**SVG 图表逐字搬运**（viewBox/坐标/配色/字体不改），只在外层 `.fig` 加 `an`、给数据条/节点/折线加动画钩子。源文的 `.fig.breakout` 破格在演示版里**去掉**（每屏已全宽居中，负 margin 会出问题）。文案可适度精简适配一屏，保意保语气、过 `hekouwang-content-master-skill` #6.6 去 AI 味。

### 1.4 主色：**米白是全站默认**，焰彩白是国标专属例外

新做任何一期，**默认拷米白引擎**。只有两种情况例外，别自作主张换调：

| 系列 | 主色 | 拷哪个模板 |
|---|---|---|
| **默认 / 首页 / 出行SaaS** | **米白** `#faf9f5` + 黏土 `#c15f3c`（编辑/人文感） | `deck-engine-米白.html` |
| **智能体互联国标** | **V6 焰彩白** `#fbfaff` + 紫 `#7c3aed` + 焰橙/粉，Mozilla 可变字体（大厂发布感） | `deck-engine-V6焰彩白.html` |

- ⚠️ **暖黑 `#161514` / V6焰彩黑 `#170a30` = 历史过渡态，不再新做**。线上尚有存量（算力账本·偷师=焰彩黑，Harness=暖黑），按计划逐步 flip 回米白；`deck-engine-暖黑.html` 仅为维护存量保留，**新 EP 不要拷它**。
- 亮底适配铁律（米白/焰彩白）：网格线改极淡深色、卡片靠 `--shadow` 投影不靠辉光、标题黏土渐变(深→浅)、幽灵号深色 `opacity:.05`、`.grain` 用 `mix-blend-mode:multiply`。引擎 JS 主题无关、逐字一致。
- **给存量 deck 换肤（黑→米白）→ 读 [`references/换肤-token-flip.md`](references/换肤-token-flip.md)**：脚本会截空文件、半成品会留残色，踩过的坑都在里面，别凭感觉改。

### 1.5 批量做（多 EP）

引擎相同、只内容不同 → 并行开多个 subagent，每个给「对应主色模板路径 + 源文章路径 + 本节规则」，要求 `<head>`CSS 与 `<script>`JS 与模板**逐字一致**，只换内容、按源文追加专属组件 CSS（滑块/时间线/对比/桥…，改用模板的 token）。产出后主控用 headless Chrome 截图核验各图表屏（`--virtual-time-budget=5000` 让动画跑完）。

## 1.6 放映 / 提词器（讲 + 录 双用）⭐

模块：`assets/presenter/presenter-module.html`（自包含 `<style>+<div>+<script>`，已注入三套引擎模板与 `examples/demo.html`，**拷模板即带，无需改引擎**）。

- **按 `S`** 开「讲者视图」：**独立窗口**（计时器 + 当前镜逐字稿 + 下一镜预览），主屏与讲者窗靠 **BroadcastChannel 双向同步**——**主屏保持干净，可投影 / 录屏**。弹窗被拦（或无 BroadcastChannel）时自动回退为页内全屏浮层（单屏排练也能用）。
- **真·双屏**：把 deck 在第二显示器再开一个窗口、地址后加 `?speaker=1` 即变讲者窗，免弹窗。讲者窗可**反向遥控主屏**：在讲者窗按 `←/→` 翻镜、`P` 计时、`R` 归零、`Esc/S` 关（靠向主屏引擎派发方向键事件，不改引擎）。
- **键位**：`S` 开/关 · `P` 计时启停 · `R` 归零 · `Esc` 关 · `←/→` 翻镜（主屏与讲者窗都认）。
- **逐字稿 = 配音 / 口播脚本**：在每张 `.slide` 里加 `<div class="notes">这一镜要讲的话…</div>`（观众/录屏**永不可见**，模块强制 `display:none`）。这份 notes 同时就是该镜的口播稿——录屏时主屏放干净 deck、讲者窗当提词器照念；也可直接喂 TTS（云扬）。
- 取数靠 `#deck .slide` 的 `.active` class（`MutationObserver` 监听），与引擎解耦；无 `.notes` 的镜回退显示标题。讲者信号用 `window.name`/`?speaker`（**不用 `#speaker`**——引擎深链 `replaceState('#N')` 会把 hash 冲掉）。
- ⚠️ 本地 `file://` 双击时 `window.open` 可能被拦、且 BroadcastChannel 跨窗不通（opaque origin）——**用 `python3 -m http.server` 起本地服务**预览（与字体本地化要求一致）；发布到 CF Pages(https) 后正常。

> 一图一镜 + 每镜一段 notes ⇒ 写完 deck 就同时有了「演示稿 + 提词器 + 口播稿」三合一。

## 2. 首页 `home.html`

演读 DECK 品牌落地页（**米白 `#faf9f5`**，2026-07-14 起；此前为暖黑）：masthead 品牌 + 「演读 ⟨DECK⟩」产品名、hero「把复杂的 AI，读成一场演示」、proof 三栏（第三种读法/翻页·自动播放/读完就懂）、系列卡片区（现 5 个：国标 / 算力账本 / 偷师AI大佬 / Harness工程 / 出行SaaS工程手记）、出品方 about（人设 + 禾口王=程）、订阅区（领《AI 内容流水线手册》三步）、底部内联留言板（`.talk-*`，`page='home'`）。**响应式**断点齐全（600/680/760/520）。
- ⚠️ **系列卡是静态手写的**，不由 `MANIFEST` 生成（`write_index()` 是遗留死函数）——加系列要**手改 `home.html`** + 补 `MANIFEST`/`SERIES_META` 三处一起动。
- 人设口径以记忆 `brand-persona-tagline` 三句为准（别自由改措辞）。**改首页改 `演读DECK/home.html`，不在 `dist/` 里改。**

## 3. 字体自托管（零 CDN）⭐ 关键

发布时 `publish.py` 的 `localize()` 把源 HTML 里所有 Google/loli 外链删掉、注入指向 `/fonts/` 的本地 `@font-face`；Anthropic 绝对路径也改写成 `/fonts/`。`subset_cjk()` 用 `tools/fenv` 的 `pyftsubset` 按**全站实际用字**把思源黑 4 字重（400/500/700/900，800 映射 900）+ 宋（金句衬线）子集化成小 woff2（各 ~180KB），连 Anthropic 一起打包进 `dist/fonts/`。

- **首屏字重跳变(FOUT)**：每页 `<head>` 注入 4 条 `<link rel=preload>`（900/400/Anthropic Sans/Mono）让关键字体高优先级先下；`dist/_headers` 给 `/fonts/*` 设一周强缓存。这两条**必须保留**，否则首屏会「先系统字、再换思源」肉眼可见跳一下。
- 字体源出处：思源来自 `@fontsource@5.0.0`（jsdelivr）逐字重静态 woff2；Anthropic 来自 `hekouwang-content-master-skill/assets/fonts/`（自用/演示授权）；Mozilla Headline/Text VF 为 Mozilla 官方开源（OFL），可自由使用。
- venv 丢了重建：`cd 演读DECK && python3 -m venv tools/fenv && tools/fenv/bin/pip install fonttools brotli`。无 venv/字体源时 publish 回退用 `fonts/cache/`。

## 4. 发布

```bash
# 从项目根运行
python3 演读DECK/publish.py                                        # 只构建 dist/（默认不部署）
YANDU_CF_PROJECT=<项目名> python3 演读DECK/publish.py --deploy      # 构建 + 部署到 CF Pages
```

- **部署会把内容公开到公网**：只有用户明确要求发布时才加 `--deploy`，部署前先让用户确认项目名和本次要上线的期数。Wrangler 需用户自行安装（脚本不会自动全局安装）。
- **加一期**：在 `publish.py` 的 `MANIFEST` 加一行（源 HTML 相对项目根的路径 + slug 如 `suanli/ep04` + 系列 + EP + 分类 + 标题 + 简介 + 屏数）。**加一个系列**：再补 `SERIES_META` 一条，**并手改 `home.html` 的系列卡**——首页系列卡是**静态手写**的，不由 MANIFEST 生成（旧的 `write_index()` 已删除）。
- **留言板**（Pages Functions + D1）默认不注入页面。需要时设 `YANDU_ENABLE_COMMENTS=1` 再构建；会收集访客昵称、留言正文，并在服务端存 IP 加盐哈希做限频。**加装/排错 → 读 [`references/留言板-D1.md`](references/留言板-D1.md)**：部署得用配置式（不带 `dist` 参数）+ `cwd=SELF`，日志出现 `Uploading Functions bundle` 才算带上后端。
- 干净 URL：演示版拷进 `dist/<slug>.html`，CF Pages 自动去 `.html`（`/suanli/ep01`）。
- 部署走 `publish.py --deploy`（内部用配置式 `wrangler pages deploy`）；首次需 `wrangler login`（用户自己 `! wrangler login`）。

## 5. 防踩坑（实测血泪）

1. **`dist/` 每次构建被清空**——别在里面改任何东西；首页改 `home.html`，演示版改各 EP 源。
2. **本地预览必须起 http 服务器**：`dist` 用站内 `/fonts/` 绝对路径，`file://` 双击打不出字体。`cd dist && python3 -m http.server 8000`。
3. **`keynote.pages.dev` / `keynotes` 等常用名全球已被占**——CF 会自动加随机后缀(`keynote-9z0`)。本机网络有透明代理劫持 DNS、返回 198.18.0.x 假 IP，**本地 nslookup 测不出子域可用性**；唯一可靠 = `wrangler pages project create <名>` 后看 `project list` 分配的子域有没有后缀。最终用 `hekouwang`。
4. **国内 EdgeOne 是死路**：免费自动域名一律带 token 鉴权、公网 401（ICP 备案要求），别再碰；直接 Cloudflare Pages。
5. **移动 venv 会失效**（shebang/pyvenv.cfg 写死原路径）——换位置就重建。
6. **本机代理会截断大文件下载(>~4MB)**：思源变量字体下不全 → 改用 @fontsource 逐字重静态 woff2(各 ~1.6MB)再子集化。
7. 截图核验演示版给足时间（`--virtual-time-budget=5000`），让 fit/动画跑完再截。

## 配套与依赖
- **内容产线（强依赖）：`hekouwang-content-master-skill`**——演示版的源文章 HTML、视觉规范(V1/V2/V3)、配色 token、字体方案都来自它；本 Skill 只做「内容→翻页演示+发布」这一半。**⚠️ 它是付费 Skill**（需作者授权），仓库不含其内容。只用引擎可直接拷 `assets/templates/deck-engine-*.html`（零依赖独立可用）。
- 示例：`examples/demo.html`（自包含、零依赖、双击即看的最小动画示例）。
- 记忆：`keynote-yanshi-site`（站点现状 + 发布链路）、`keynote-deck-engine`（引擎做法）、`brand-persona-tagline`（人设三句）。
