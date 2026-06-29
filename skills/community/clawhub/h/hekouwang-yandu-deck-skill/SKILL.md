---
name: hekouwang-yandu-deck-skill
description: >
  会勇禾口王的AI笔记 ·「演读 DECK」沉浸式演示产线与发布 Skill。把一篇文章/选题做成「一屏一镜、可翻页、能自动播放」的 keynote 演示版网页（暖黑 或 米白 两套主色），并自托管字体、发布到 Cloudflare Pages（hekouwang.pages.dev）。
  当需要：① 把某篇文章/某期内容做成「演示版 / 演读 DECK / 翻页演示 / keynote 网页 / 沉浸式阅读页」；② 给「演读 DECK」站加一期演示、加一个系列、改首页；③ 发布/更新 hekouwang.pages.dev；④ 自托管字体、解决首屏字重跳变(FOUT)、子集化思源字体 时使用。
  触发词：演读DECK / 演读 deck / 演示版 / 翻页演示 / keynote 网页 / 沉浸式阅读 / 发布到 hekouwang / 加一期演示 / 演示版引擎。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# 演读 DECK · 沉浸式演示产线与发布

> 「演读 DECK」= 会勇禾口王的AI笔记出品的一款**沉浸式阅读产品**：介于长文和视频之间的第三种读法——一屏一镜、方向键/空格/点击翻页、能自动播放，把一个复杂主题安静完整地讲给你看。
> 线上：**https://hekouwang.pages.dev** ｜ 与图文产线 `hekouwang-content-factory` 配套（那是出文章/贴图/视频，这是把内容做成翻页演示 + 发布）。

## 0. 系统在哪（先认这个）

发布系统是项目里一个**自包含目录** `<项目根>/演读DECK/`：

```
演读DECK/
├── publish.py    # 发布脚本：构建 dist/ → 部署 CF Pages（零三方依赖，仅标准库 + 一个子集化 venv）
├── home.html     # 首页源（改首页改这个；dist/ 每次构建会清空，别在里面改）
├── fonts/src/    # 字体源：思源黑 NotoSansSC-{400,500,700,900}.woff2 + 宋 -700 + Anthropic Sans/Mono
├── fonts/cache/  # 子集化产物缓存（无字体源/无 venv 时回退）
├── tools/fenv/   # 子集化 venv(fonttools+brotli)；移动会失效，丢了重建
├── dist/         # 构建产物 = 部署目录（可整删重生）
└── README.md
```

本 Skill 按官方约定分目录带了**可移植副本**（新项目落地时拷过去）：
- `assets/templates/deck-engine-暖黑.html` / `deck-engine-米白.html`（两套引擎模板，按 EP 拷进内容目录）、`assets/templates/home.html`（首页源）
- `scripts/publish.py`（发布脚本）
- `references/系统说明.md`（系统说明文档）、`examples/demo.html`（零依赖最小示例）

> ⚠️ **`scripts/publish.py` 与 `assets/templates/home.html` 在实际项目里必须同目录**——落地时把这两个一起拷进项目根的 `演读DECK/`（`publish.py` 用 `SELF/home.html` 找首页源）。

## 1. 把文章做成「演示版 deck」⭐ 核心

一篇 V2 文章 → 一屏一镜的 keynote。**零依赖（纯 CSS + 原生 JS，不引 GSAP/外链，国内/CF 都快）。** 沿用源文章的 V2 视觉（暖黑 或 米白）、字体、grain/mesh/frame/幽灵章节号。

### 1.1 引擎（照抄模板，别重写）

样板：`assets/templates/deck-engine-暖黑.html`（数据/财经/科普暗调）、`assets/templates/deck-engine-米白.html`（人文/方法论亮调）。
**做新 EP = 拷一份对应主色的模板，`<head>` 的全部 CSS 和 `</main>` 之后的全部 `<script>` 逐字保留，只换内容 slide / 顶栏标签 / title / 片尾。** 引擎已实现：

> ⚠️ 模板 `@font-face` 里的字体路径是占位符 `{{SKILL_DIR}}/assets/fonts/...`——指向兄弟 skill `hekouwang-content-factory` 的字体。拷模板做 EP 时**把 `{{SKILL_DIR}}` 替换成 content-factory 的绝对 Base directory**（本地预览/截图才有字体）。发布时 `publish.py` 会把它统一收成站内 `/fonts/`，万一漏替换也能兜底。

- 全屏 `.slide`（一屏一镜），`.stage` 居中 + JS `fit()` 等比缩放防裁切；
- 导航：←/→/空格/点击/触屏滑动/底部圆点/Home/End/F 全屏；右下「▶ 自动播放」(7s/屏，像放视频)；顶部进度条 + `NN/总数`；`#N` 深链（可分享到某屏）；`prefers-reduced-motion` 自动关动画。

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

源文每个 section + 每张图表都要有对应镜头。**封面屏 + 速览屏（用源文 hero 的关键数据做 readout 仪表条）打头，片尾签收卡收尾**（含私域 CTA），一篇 9 节 → 约 12–24 屏。
**SVG 图表逐字搬运**（viewBox/坐标/配色/字体不改），只在外层 `.fig` 加 `an`、给数据条/节点/折线加动画钩子。源文的 `.fig.breakout` 破格在演示版里**去掉**（每屏已全宽居中，负 margin 会出问题）。文案可适度精简适配一屏，保意保语气、过 `hekouwang-content-factory` #6.6 去 AI 味。

### 1.4 两套主色（每个系列可有独立辨识度）

- **暖黑**（`#161514` + 黏土 `#e08a5f` + 石板蓝/赭石）：数据控制台感，适合财经/科普/数据密集。样例系列「算力账本」。
- **米白**（`#faf9f5` + 黏土 `#c15f3c`）：编辑/人文感，适合方法论/人物。样例系列「偷师AI大佬」。
- 暗→亮适配铁律（米白）：网格线改极淡深色、卡片靠 `--shadow` 投影不靠辉光、标题黏土渐变(深→浅)、幽灵号深色 `opacity:.05`、`.grain` 用 `mix-blend-mode:multiply`。引擎 JS 主题无关、逐字一致。

### 1.5 批量做（多 EP）

引擎相同、只内容不同 → 并行开多个 subagent，每个给「对应主色模板路径 + 源文章路径 + 本节规则」，要求 `<head>`CSS 与 `<script>`JS 与模板**逐字一致**，只换内容、按源文追加专属组件 CSS（滑块/时间线/对比/桥…，改用模板的 token）。产出后主控用 headless Chrome 截图核验各图表屏（`--virtual-time-budget=5000` 让动画跑完）。

## 2. 首页 `home.html`

演读 DECK 品牌落地页（暖黑）：masthead 品牌 + 「演读 ⟨DECK⟩」产品名、hero「把复杂的 AI，读成一场演示」、proof 三栏（第三种读法/翻页·自动播放/读完就懂）、两个系列卡片区、出品方 about（人设 + 禾口王=程）、订阅区（领《AI 内容流水线手册》三步）。**响应式**断点齐全（600/680/760/520）。
人设口径以记忆 `brand-persona-tagline` 三句为准（别自由改措辞）。**改首页改 `演读DECK/home.html`，不在 `dist/` 里改。**

## 3. 字体自托管（零 CDN）⭐ 关键

发布时 `publish.py` 的 `localize()` 把源 HTML 里所有 Google/loli 外链删掉、注入指向 `/fonts/` 的本地 `@font-face`；Anthropic 绝对路径也改写成 `/fonts/`。`subset_cjk()` 用 `tools/fenv` 的 `pyftsubset` 按**全站实际用字**把思源黑 4 字重（400/500/700/900，800 映射 900）+ 宋（金句衬线）子集化成小 woff2（各 ~180KB），连 Anthropic 一起打包进 `dist/fonts/`。

- **首屏字重跳变(FOUT)**：每页 `<head>` 注入 4 条 `<link rel=preload>`（900/400/Anthropic Sans/Mono）让关键字体高优先级先下；`dist/_headers` 给 `/fonts/*` 设一周强缓存。这两条**必须保留**，否则首屏会「先系统字、再换思源」肉眼可见跳一下。
- 字体源出处：思源来自 `@fontsource@5.0.0`（jsdelivr）逐字重静态 woff2；Anthropic 来自 `hekouwang-content-factory/assets/fonts/`（自用/演示授权）。
- venv 丢了重建：`cd 演读DECK && python3 -m venv tools/fenv && tools/fenv/bin/pip install fonttools brotli`。无 venv/字体源时 publish 回退用 `fonts/cache/`。

## 4. 发布

```bash
# 从项目根运行
python3 演读DECK/publish.py              # 构建 dist/ + 部署到 CF Pages（hekouwang）
python3 演读DECK/publish.py --build-only # 只构建 dist/，不部署
```

- **加一期**：在 `publish.py` 的 `MANIFEST` 加一行（源 HTML 相对项目根的路径 + slug 如 `suanli/ep04` + 系列 + EP + 分类 + 标题 + 简介 + 屏数）。**加一个系列**：再补 `SERIES_META` 一条。
- 干净 URL：演示版拷进 `dist/<slug>.html`，CF Pages 自动去 `.html`（`/suanli/ep01`）。
- 部署用 `wrangler pages deploy dist --project-name hekouwang`；首次需 `wrangler login`（用户自己 `! wrangler login`）。

## 5. 防踩坑（实测血泪）

1. **`dist/` 每次构建被清空**——别在里面改任何东西；首页改 `home.html`，演示版改各 EP 源。
2. **本地预览必须起 http 服务器**：`dist` 用站内 `/fonts/` 绝对路径，`file://` 双击打不出字体。`cd dist && python3 -m http.server 8000`。
3. **`keynote.pages.dev` / `keynotes` 等常用名全球已被占**——CF 会自动加随机后缀(`keynote-9z0`)。本机网络有透明代理劫持 DNS、返回 198.18.0.x 假 IP，**本地 nslookup 测不出子域可用性**；唯一可靠 = `wrangler pages project create <名>` 后看 `project list` 分配的子域有没有后缀。最终用 `hekouwang`。
4. **国内 EdgeOne 是死路**：免费自动域名一律带 token 鉴权、公网 401（ICP 备案要求），别再碰；直接 Cloudflare Pages。
5. **移动 venv 会失效**（shebang/pyvenv.cfg 写死原路径）——换位置就重建。
6. **本机代理会截断大文件下载(>~4MB)**：思源变量字体下不全 → 改用 @fontsource 逐字重静态 woff2(各 ~1.6MB)再子集化。
7. 截图核验演示版给足时间（`--virtual-time-budget=5000`），让 fit/动画跑完再截。

## 配套与依赖
- **内容产线（强依赖）：`hekouwang-content-factory`**——演示版的源文章 HTML、视觉规范(V1/V2/V3)、配色 token、字体方案都来自它；本 Skill 只做「内容→翻页演示+发布」这一半。**⚠️ 它是付费 Skill**（需作者授权），仓库不含其内容。只用引擎可直接拷 `assets/templates/deck-engine-*.html`（零依赖独立可用）。
- 示例：`examples/demo.html`（自包含、零依赖、双击即看的最小动画示例）。
- 记忆：`keynote-yanshi-site`（站点现状 + 发布链路）、`keynote-deck-engine`（引擎做法）、`brand-persona-tagline`（人设三句）。
