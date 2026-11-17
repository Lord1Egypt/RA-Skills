# 期刊图片规格（逐条带出处 · 核实日期 2026-11-03）

> **怎么用这份表**：先按目标期刊查这一行，再让 `check --journal <id>` 用同一套预置去验。
> 每条都写了官方页面 URL 和核实日期。**没有把握的写「待核」，不写数字** —— 编一个 89 mm 出来，用户照着交稿被打回，比没有这张表更糟。
> 期刊的 Guide for Authors 年年改，投稿前**再点一次链接**；期刊专属说明永远压过通用说明。

## 一句话总览

| 预置 id | 期刊 | 单栏宽 | 双栏宽 | 最大高度 | 最小字号 | 分辨率 | 状态 |
|---|---|---|---|---|---|---|---|
| `nature` | Nature（及 Nature Portfolio 研究刊） | 89 mm | 183 mm | 170 mm | 5 pt（上限 7 pt） | 主图为矢量；Extended Data ≤300 dpi | ✅ 已核实 |
| `elsevier` | Elsevier 通用（多数 Elsevier 刊） | 90 mm | 190 mm（1.5 栏 140 mm） | 待核 | 正文 7 pt（上下标 ≥6 pt） | 半调 300 / 混合 500 / 线稿 1000 dpi | ✅ 已核实（部分项待核） |
| `ieee` | IEEE 期刊/会议 | 88.9 mm（3.5 in） | 182 mm（7.16 in） | 待核 | 待核 | 彩色/灰度 >300 dpi；黑白线稿 >600 dpi | ✅ 已核实（部分项待核） |
| `plos` | PLOS ONE（及 PLOS 系列） | 789–2250 px @300 dpi 之间（≈66.8–190.5 mm） | 同左（宽度上限即整幅） | 2625 px @300 dpi（222.3 mm） | 8 pt（范围 8–12 pt） | 300–600 dpi | ✅ 已核实 |
| `acm` | ACM（TAPS 模板） | sigconf/sigplan 3.42 in（≈86.9 mm） | 7 in（177.8 mm） | 待核 | 待核 | >300 dpi | ✅ 已核实（部分项待核） |
| `science` | Science（AAAS） | 待核 | 待核 | 待核 | 待核 | 待核 | ⚠️ 待核 |
| `cell` | Cell / Cell Press | 待核 | 待核 | 待核 | 待核 | 待核 | ⚠️ 待核 |
| `springer` | Springer（期刊/图书） | 待核 | 待核 | 待核 | 待核 | 待核 | ⚠️ 待核 |
| `thesis-cn` | 中文学位论文 | 随学校模板 | — | — | 待核 | 待核 | ⚠️ 待核 |
| `custom` | 中文核心期刊 / 自定义 | 随刊物投稿须知 | — | — | 待核 | 待核 | ⚠️ 待核 |

---

## Nature（含 Nature Portfolio 研究刊）

- 来源：[Nature research figure guide — Building and exporting figure panels](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
- 核实日期：2026-11-03
- **栏宽**：单栏 **89 mm**，双栏 **183 mm**
- **最大高度**：**170 mm**（要给图注留位置）
- **字号**：**最小 5 pt，最大 7 pt**；字体 Arial / Helvetica 等标准字体；**文字不要转曲**，嵌入字体（TrueType 2 或 42）；避免彩色文字
- **主图格式**：要**矢量为准、保留可编辑图层**。首选 `.ai` `.eps` `.pdf`；可接受分层 PSD、PPT 先存 PDF、Inkscape 存的 **plain SVG**、Excel、`.ps`
- **不接受**：`.jpeg` `.tiff` `.png`、Canvas、DeltaGraph、Tex、ChemDraw、SigmaPlot、CorelDraw
- **文件大小**：尽量 ≤50 MB，所有组件**嵌入**不要链接
- **Extended Data（在线补充）**：**RGB**（不是 CMYK），**最高 300 dpi**，单图 ≤10 MB，只收 `.jpeg`（首选）`.tiff` `.eps`；表格一栏 8.9 cm / 两栏 18 cm；文件名 `姓_EDfig1.jpg`
- **色彩/色盲**：明确给了一套色盲友好调色板（与 Okabe–Ito 同源：`#000000 #E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7`），要求避免红/绿组合和彩虹色阶；用图内图例或引线，别把颜色解释塞进图注
- 面板：按字母顺序（a、b、c）紧凑排列，别乱放留白

> 注意：Nature **主图不接受位图**，所以“多少 DPI”这件事对主图不适用；别拿 300 dpi 的 PNG 去投 Nature 主图。

## Elsevier（通用政策）

- 来源：[Elsevier policy — Artwork sizing](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing)
- 核实日期：2026-11-03
- **宽度**：最小 30 mm；单栏 **90 mm**；1.5 栏 **140 mm**；双栏 **190 mm**
- **字号**：成品印刷尺寸正文 **7 pt**，上下标**不小于 6 pt**（官方口径是 rule-of-thumb，不是硬规则；有底纹/网点时可能要 10 pt）
- **分辨率**：半调图（照片、显微图）**300 dpi**；图文混合 **500 dpi**；线条图 **1000 dpi**
- **像素换算**：像素 = DPI × 英寸；90 mm 单栏在 300 dpi 下 ≈1063 px，1000 dpi 线稿 ≈3543 px
- **最大高度**：**待核**（该页未给统一高度限制；以具体期刊 Guide for Authors 为准）
- **接受格式 / 字体 / 色彩模式**：**待核**（同在 artwork instructions 系列的其他子页，本次未逐页核实；不同期刊另有要求）
- **重要**：Elsevier 每个刊都在通用规范之上追加自己的要求，**先看目标刊的 Guide for Authors**

> 待核实项建议路径：Elsevier `Artwork and media instructions` 的 “Artwork file formats / Colour / Fonts” 子页，以及目标期刊的 Guide for Authors（`elsevier.com/journals/<刊名>/<ISSN>/guide-for-authors`）。

## IEEE（期刊与会议）

- 来源：[IEEE Author Center — Resolution and Size](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/)；色盲建议见 [Create Graphics for Your Article](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/)
- 核实日期：2026-11-03
- **栏宽**：单栏 **3.5 in = 88.9 mm = 21 picas**；双栏 **7.16 in = 182 mm = 43 picas**；不建议做得比单栏还窄
- **分辨率**：非矢量彩色/灰度图 **>300 dpi**；黑白线条图 **>600 dpi**；事后调分辨率救不回来
- **矢量格式**：**PS / EPS / PDF**（可自由缩放）
- **最大高度 / 最小字号 / 字体 / 色彩模式**：**待核**（该页未规定字号与高度；字号随 IEEEtran 模板与刊别而异）
- **色盲**：官方建议**灰度打印能读**；颜色 + 形状/线型双编码；线加粗并给不同的数据点符号；标签贴着线而不是只靠颜色图例

> 待核实项建议路径：IEEE 各刊 `Author Information` / `IEEEtran` 模板说明，以及 `File Formatting` 子页。

## PLOS（PLOS ONE 及 PLOS 系列）

- 来源：[PLOS ONE — Figures](https://journals.plos.org/plosone/s/figures)
- 核实日期：2026-11-03
- **尺寸**：宽度 **789–2250 px**（300 dpi 下即 6.68–19.05 cm）；高度上限 **2625 px**（22.23 cm，占满整页且不含图注）；想跟正文栏对齐就 **≤5.2 in（13.2 cm）**
- **分辨率**：**300–600 dpi**（高于 600 可能被缩；低于 300 会判糊）
- **文件**：**TIFF 或 EPS**；≤10 MB；TIFF 要**展平、无图层、无 alpha 通道、LZW 压缩**；EPS 要嵌字体或转曲
- **图内文字**：只用 **Arial / Times / Symbol**，**8–12 pt**；图里不要放作者名、标题、图号、图注
- **色彩模式**：**RGB（8 bit/通道）或灰度**
- **多面板**：所有面板放进**一个文件、一页**；建议图四周留 2 pt 白边防裁切
- 命名 `Fig1.tif`、`Fig2.eps`…，与图注、正文引用一致；图注写正文里，不写进图文件

## ACM（TAPS 模板）

- 来源：[ACM — TAPS Image Specifications](https://authors.acm.org/proceedings/production-information/taps-image-specifications)
- 核实日期：2026-11-03
- **宽度**：`acmsmall` 33 picas / 396 pt / **5.5 in**；`acmlarge` 37.5 picas / 450 pt / **6.25 in**；`sigconf`、`sigplan` 单栏 **20.5 picas / 246 pt / 3.42 in**，双栏 **42 picas / 504 pt / 7 in**
- **分辨率**：**>300 dpi**；黑白图用灰度给
- **格式**：**SVG / PS / EPS / PDF / PNG / JPG / EMF / TIFF** 都收；**不收** Word 里画的图形对象（形状、流程图、WordArt），要先转成上面某一种；不用 Word 的裁剪功能；**标签要画进图里**；去掉图片周围多余白边
- **字体**：EPS/PS/PDF 里要**嵌字体或全部转曲**，否则别的机器打开会丢字；可编辑矢量里黑色文字设为叠印（overprint）
- **最小字号 / 最大高度 / 色彩模式**：**待核**（该页未规定；按模板栏宽与正文字号自行保证可读）

## Science（AAAS）—— 待核

- 官方入口：[Science — Information for Authors](https://www.science.org/content/page/science-information-authors)
- 核实日期：2026-11-03
- **状态：待核。** 本次核实访问被 Cloudflare 挡下（HTTP 403），页面内容未取到，因此**不给出任何栏宽/字号/DPI 数字**。
- 已知确定的部分：Science 与 Nature 一样以**矢量图**为主，投稿前必须去看它当期的 Author Guidelines。
- 待核项建议路径：上表 URL → “Figures and Tables” 一节；或期刊 PDF 版 `Science Information for Authors`。

## Cell / Cell Press —— 待核

- 官方入口：[Cell — Information for Authors](https://www.cell.com/cell/authors)
- 核实日期：2026-11-03
- **状态：待核。** cell.com 本次返回 Cloudflare 403（ScienceDirect 同类页面亦 403），未取到官方数字。
- 可用的替代口径：Cell Press 属 Elsevier 系，**通用规范可先套 Elsevier 那一节**；但 Cell 对示意图、图形摘要（graphical abstract）另有专门要求，**以 Cell 自家 Guide for Authors 为准**。
- 待核项建议路径：cell.com 目标刊 → “Authors” → “Figure Guidelines / Graphical Abstract”。

## Springer（期刊与图书）—— 待核

- 官方入口：Springer 期刊 `link.springer.com/journal/<刊号>/submission-guidelines` 的 “Preparing figures” 一节
- 核实日期：2026-11-03
- **状态：待核。** 本次访问 springer.com 与 link.springer.com 的对应页面时被重定向到登录（`idp.springer.com`），未取到正文，**不给出数字**。
- 注意区分：**Nature Portfolio 属于 Springer Nature，但用的是本文件 `nature` 那一行**（已核实）；这里的 `springer` 预置指 Springer 自有期刊/图书。
- 待核项建议路径：`link.springer.com/journal/<刊号>/submission-guidelines` → “Preparing figures”；图书走 `springer.com` 的 Book Manuscript Guidelines。

## 中文学位论文（thesis-cn）—— 待核

- 依据：GB/T 7713.1《学位论文编写规则》规定**组成要素与编排**，**不给具体栏宽和字号**；版式细节由各校研究生院模板规定。
- 核实日期：2026-11-03
- **状态：待核。** 各校差异极大（页边距、图题字号、是否要求中英双语图题）。**必须用你自己学校的《学位论文格式要求》**。
- 实操建议：先用 `check --journal thesis-cn` 只做通用项（字号 ≥ 正文小一号、DPI ≥300、不红绿并置、文字不溢出），版式尺寸按学校模板改 `figure.json`。

## 中文核心期刊 / 自定义（custom）—— 待核

- 依据：中文期刊普遍在《投稿须知》里另附图片要求，栏宽/字号/字体差异大（不少刊物仍要求 **宋体/黑体 + Times New Roman 混排**，且只收 TIFF/JPG）。
- 核实日期：2026-11-03
- **状态：待核。** 没有统一国标可引用。
- 实操建议：把目标刊的投稿须知里的要求抄进 `figure.json`（`width`、`height_mm`、`font`、`font_size_pt`、`dpi`），用 `check --journal custom` 按你填的数值验。

---

## 图内字体：期刊接受什么

| 期刊 | 明示接受的字体 | 出处 |
|---|---|---|
| Nature | Arial / Helvetica 等标准字体，嵌字体、不转曲 | 上方 Nature 链接 |
| PLOS | Arial / Times / Symbol（8–12 pt） | 上方 PLOS 链接 |
| Elsevier | 待核（官方示意图通用规范未在该页点名字体） | 同上 |
| IEEE | 待核 | 同上 |
| ACM | 不限，但必须嵌入或转曲 | 上方 ACM 链接 |

**通用做法**：正文里 Latin 字符用 Arial/Helvetica（无衬线），中文用思源黑体/微软雅黑一类无衬线；同一张图**别中英文各用一套衬线**，那是最常见的"一眼业余"。

## 色彩：为什么默认推 Okabe–Ito

- Nature 官方给的色盲友好色板与 **Okabe–Ito** 基本一致（8 色，含便于区分的橙/天蓝/蓝绿/黄/蓝/朱红/红紫）。
- 本技能默认调色板 `okabe-ito` 就是这个；`grayscale-safe` 更保守（灰度打印仍可分）。
- 三条硬要求：
  1. **红绿不要并置**（红绿色盲约 8% 男性）；
  2. **颜色之外再给一个通道**：线型（实/虚）、形状（方/圆/三角）、直接标注；
  3. **灰度打印能读** —— IEEE 和 Nature 都明确这么要求。

## 与本技能内置预置的关系

- 代码里渲染/检查实际用的数值在 `assets/journals.json`（由 render-core 维护），本文件是**出处记录 + 待核清单**。
- 两者不一致时：**以官方页面为准**，并把差异报给项目；不要为了"对得上代码"去改官方数字。
- 复核节奏：每季度重跑一次链接；`check` 报告会标出期刊预置与核实状态，方便判断这条规则有多旧。

### 已知差异（内置预置 vs 官方核实，2026-11-03）

| 项 | 内置预置 `assets/journals.json` | 官方核实（本文件） | 影响 / 建议 |
|---|---|---|---|
| Nature 最大高度 | `max_height_mm: 247` | **170 mm**（要给图注留位置） | `check` 会放过 171–247 mm 的图，期刊排版时再缩，字号跟着缩水。**需要把预置改成 170**；本文件不跟随 247 |
| Nature 主图格式 | `formats: eps/pdf/tif` | 主图**只收矢量**（首选 `.ai` `.eps` `.pdf`，另收分层 PSD、PPT→PDF、plain SVG、Excel、.ps），**不收** tiff/png/jpeg | 别按预置给 Nature 主图导 TIFF；本文件按官方口径写 |
| Nature 出处 URL | `nature.com/nature/for-authors/final-submission`（会跳登录） | `research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/` | 预置里的 `source` 建议换成可访问的官方图指南页 |
| ACM 单栏宽 | 84.7 mm（≈3.33 in） | **3.42 in = 86.9 mm**（20.5 picas / 246 pt） | 差约 2 mm，不致命；若要精确对齐 `sigconf`，改成 86.9 |
| PLOS 格式 | `formats` 含 png | 官方只收 **TIFF / EPS** | png 只能当草稿，正式投别再导 png |
| IEEE 最小字号 / 最大高度 | `min_font_pt: 8`、`max_height_mm: 234` | 官方页**未给**这两项（待核） | 8 pt / 234 mm 是内部保守默认值，对外别说成"IEEE 要求 8 pt" |
| Science / Cell / Springer / 学位论文 | 有数值但 `verified: false` | 本文件同样标**待核** | 两边口径一致：这些数字只用于排版默认，不得当合规承诺 |

> 另注：`scripts/check.mjs` 里带一份**兜底预置表**（`journals.json` 读不到时用），其数值与 `assets/journals.json` 不同（例如 PLOS 兜底用 83 mm）。兜底只在文件缺失时触发，一旦触发合规判定会变松，建议实现侧统一到同一份数据。
