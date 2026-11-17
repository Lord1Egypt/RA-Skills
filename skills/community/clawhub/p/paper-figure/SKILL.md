---
name: paper-figure
slug: paper-figure
displayName: "论文配图"
display_name: "论文配图"
display_name_en: "Paper Figure"
version: "1.0.0"
author: "he fangsheng <hefangsheng@gmail.com>"
license: MIT
homepage: "https://github.com/u-claw-os/paper-figure"
tags: [academic-figures, journal-compliance, scientific-visualization]
description: "可投稿的论文图：把「合规格、不被退稿」变成一条命令。期刊栏宽、最小字号、字体嵌入、色彩模式、300/600/1000 dpi、面板 a/b/c 逐条对着官方作者指南核过（每条带官方 URL 与核实日期）；结构图/流程图/机制图/对比图用代码排成矢量，数据图从你的真 CSV 出；本机免费跑硬校验（尺寸/字号/DPI/文字溢出/色盲），多 AI 低价会审只给「可执行的修改清单」。AI 出图只限概念示意/封面/TOC，并强制标注。当用户说「论文配图」「帮我画个架构图」「画流程图/机制图」「这数据图不好看」「图被期刊退回重画」「做个封面图」「TOC graphic」「答辩 PPT 里的框架图」「基金本子配图」「这张图能投吗」时使用。安装免费，本地渲染/检查/导出不花钱、论文数据不上传；只有 AI 概念图（¥0.03/张）和会审（¥0.01–0.07/轮）从虾盘云钱包按次扣费。"
description_zh: "可投稿的论文图：期刊栏宽、最小字号、字体嵌入、色彩模式、300/600/1000 dpi 逐条对着官方作者指南核过（带 URL 与核实日期），结构图/流程图/机制图/对比图用代码排成矢量、数据图从真 CSV 出，本机免费硬校验（尺寸/字号/DPI/溢出/色盲），多 AI 会审只给可执行修改清单；AI 只做概念示意/封面/TOC 并强制标注。当用户说「论文配图」「画架构图」「画流程图」「数据图不好看」「被期刊退回重画」「封面图」「TOC graphic」「答辩图」「基金本子配图」时使用。安装免费，本地渲染/检查/导出不花钱、数据不上传；AI 概念图 ¥0.03/张、会审 ¥0.01–0.07/轮，从虾盘云钱包按次扣费。"
description_en: "Submission-ready paper figures: journal-compliant layout plus a hard check and an actionable fix list. Column widths, minimum type size, font embedding, colour mode and 300/600/1000 dpi are taken from the publisher's own author guidelines, each rule carrying the official URL and verification date; pipeline, architecture, mechanism and comparison figures are rendered as vectors by code, data figures come from your real CSV, and local render/check/export all run on your machine so paper data is never uploaded. Multi-model review returns a fix list rather than a score. AI images are limited to concept sketches, cover art and TOC graphics and are always labelled."
examples_zh:
  - "帮我画论文里的方法总览图，投 Nature 子刊，单栏。"
  - "把 data/main.csv 画成带误差棒的柱状图，坐标轴要带单位。"
  - "这张图投稿前帮我查合规：栏宽、字号、DPI、色盲，哪儿不对给改法。"
examples_en:
  - "Draw the pipeline overview for my paper as a Nature single-column figure."
  - "Plot data/main.csv as a bar chart with error bars and labelled axes."
  - "Check this figure against the journal specs before I submit, and tell me how to fix each issue."
---

# 可投稿的论文图（Paper Figure）

**图不是画出来的，是算出来的。** 我们卖的不是"好看"，是"能投" —— 图被编辑部退回重画，八成不是因为审美不行，是因为规范不对：单栏 89 mm 你交了 120 mm，字号 4 pt，导出 150 dpi，EPS 里字体没嵌，红绿两条线色盲分不出。

这个技能跟"让大模型画张漂亮的论文图"是两件事：

- **规范逐条对过官方指南** —— 单/双栏宽、最小字号、字体嵌入、色彩模式、300/600/1000 dpi、面板 a/b/c；每条都带官方 URL 与核实日期（见 `references/journal-specs.md`），不是模型记忆里的"大概是 300 dpi"；
- **结构图 / 数据图用代码画** —— mm 精确、真字体、真数据、矢量、改一行就重出；
- **本机免费跑硬校验** —— 尺寸、字号、DPI、文字溢出、色盲、字体、元素出画布，每条报错都带"怎么改"；
- **AI 只做方向探索** —— 概念示意 / 封面 / TOC graphic，产物强制打标，**不许冒充数据图**；
- **会审卖清单不卖分数** —— 多 AI 低价会审的产出是动词开头的修改清单，不是一句"8 分，还行"。

**安装免费。** 本地渲染、检查、导出全 ¥0，**论文数据不上传**；只有 AI 概念图（¥0.03/张）和多 AI 会审（¥0.01–0.07/轮）从虾盘云钱包按次扣费。一张图从草稿做到能投，大约 **¥0.05–0.15**；¥1 能做十来张的完整打磨。

## 什么时候用

- 论文/学位论文里的**框架图、流程图、方法总览图**（"画个 pipeline"）
- 有 CSV 结果要出**柱状/折线/散点/分组/误差棒**图，但默认样式丑、图例挤、配色不安全
- **投稿前自检**："这张图能投 Nature 子刊吗？"（栏宽、字号、DPI、格式）
- 图已被**退回重画**，但没说清哪儿不对
- **AI 概念图**：摘要图、封面候选、TOC graphic、答辩 PPT/基金本子的示意图（允许示意，不允许当数据）
- 想让几个模型**以审稿人+美术总监的视角挑毛病**，给一份能照着改的清单

## 什么时候不用（谁不该用）

- **没有数据，却要"出一张数据图"**：那是造数据，本技能拒绝，没有变通做法
- 需要**真实照片/显微图/电镜图/实验原图**：那是数据完整性范畴，本技能不生成、不修饰
- 需要**插画级美术图 / 图标素材库**（细胞、器材、分子那类现成图形）：去用 BioRender / Figdraw / Illustrator，我们没有素材商城
- 想要**在线拖拽画布**：用 Figma / draw.io / Illustrator
- 要求"**保证一次过审**"：期刊规范会变，我们只保证**可查、可改、有出处** —— 每条规则带官方 URL 与核实日期，你可以在投稿前自己再核一遍

## 命令表

所有命令都长这样：`node scripts/fig.mjs <cmd> <工作目录> [参数]`。正常结果走 stdout 的 JSON，进度和人话提示走 stderr，失败返回 `{ok:false,error,fix}` 且退出码非 0。

| 命令 | 干什么 | 示例 |
|---|---|---|
| `init` | 建工作区：`brief.md` `figure.json` `data/` `out/` | `node scripts/fig.mjs init ./fig1` |
| `spec` | 把 `brief.md` 里的大白话解析成结构化 `figure.json`（本地规则，不调模型） | `node scripts/fig.mjs spec ./fig1` |
| `chart` | `data/*.csv` + figure.json 里的 data 段 → 期刊风格图表 SVG | `node scripts/fig.mjs chart ./fig1` |
| `render` | `figure.json` → `out/<name>.svg`（pipeline/architecture/mechanism/comparison/concept/toc 排版） | `node scripts/fig.mjs render ./fig1 --journal nature` |
| `check` | 确定性合规检查 → `out/check.json` + 人话报告（每条带 fix） | `node scripts/fig.mjs check ./fig1 --journal ieee` |
| `export` | 按期刊规格导出 PNG/PDF/TIFF | `node scripts/fig.mjs export ./fig1 --formats png,pdf,tif --dpi 600` |
| `concept` | AI 概念示意图/封面/TOC 草稿（默认 `gpt-image-2.5-1k`） | `node scripts/fig.mjs concept ./fig1 --n 2` |
| `review` | 多 AI 会审 → `out/review.json`（**先给修改清单**，分数仅参考） | `node scripts/fig.mjs review ./fig1 --tier econ` |
| `wallet` | 看密钥来源、余额、充值链接（只读，不花钱） | `node scripts/fig.mjs wallet` |

典型一口气：`init → spec → render（或 chart）→ check → export`；`check` 全绿但还想知道"审稿人/编辑会挑什么"，再加 `review`；要封面/TOC 才用 `concept`。

## 成本（2026-11-03 网关实测口径）

| 动作 | 费用 |
|---|---|
| `init` `spec` `chart` `render` `check` `export` `wallet` | **¥0**（纯本地，不联网） |
| `concept` AI 概念图 | 约 **¥0.03/张**（1024×1024，默认 `gpt-image-2.5-1k`；换 `gpt-image-2` 约 ¥0.32/张，贵 10 倍，不建议） |
| `review` 多 AI 会审 | **¥0.01–0.07/轮**（econ 档；卖的是修改清单，分数只用来比较两版谁更稳） |
| 一张图全流程（渲染 + 检查 + 会审 ± 一张概念图） | 约 **¥0.05–0.15** |

用户 90% 的时间都在免费层。要花钱的恰好是"从能看变成能投"的两步，别自动重试烧钱：一次 `concept` 出一张不满意就改提示词，别连着刷十张。

## 密钥从哪来

按优先级自动取，前一个没有就往下走：

1. 命令行 `--key sk-...`
2. 环境变量 `XIAPAN_API_KEY`
3. `~/.dsh/aigc-wallet.json` 的 `apiKey`（`bind` 之后写在这里）
4. `~/.uking/device.json` 的 `key`（装了 U-King / U-Claw 就有）

四个都没有，先绑一个（余额 0 的新钱包）：

```bash
node scripts/fig.mjs wallet        # 会告诉你缺 key 和下一步
```

充值：`https://u-claw.org.cn/recharge?key=<你的key>`，支付宝，¥1 起。钥匙记在钱包上，换 key 余额不丢。

## 数据不出本机

- `init` `spec` `chart` `render` `check` `export` **全部在你本机跑**，不联网；你的 CSV、图注、未发表结果**不会上传到任何服务器**。
- 只有两种情况会走网络：
  1. `concept`：提示词（几张图的英文描述）发到虾盘云网关；
  2. `review`：发给会审模型的**只有图注文本和合规检查摘要**（可选、可关，不跑就不发）。
- 生成的 SVG/PNG/PDF/TIFF 全在 `out/` 下，自己保管。审稿前把 `out/` 加进 `.gitignore`，别把未发表图推到公开仓库。

## 可信边界与学术诚信

我们明确告诉你**哪一步 AI 会翻车、翻车长什么样**，而不是含糊地说"AI 仅供参考"：

| AI 会翻的车 | 实际长什么样 |
|---|---|
| 图里的文字 | `Sclentlst`、`Resuit`、中文变方块或臆造字 |
| 图里的数字 | `0.85` 变 `O.85`，坐标轴刻度随机跳（0, 3, 7, 12） |
| 箭头方向 | 想画 A→B 画成 B→A；两端都有头；三箭头汇入却有一根反向 |
| 数据 | 看着像柱状图/曲线图，但数值是编的 —— 这是撤稿级问题，不是"不够准" |

所以边界是硬边界：

- **AI 图只能做概念示意、封面、TOC graphic**；**绝对不能当数据图、结果图、统计图**。要数据图就 `chart` 从真 CSV 画。
- 任何 AI 生成的图，产物旁边一定写一份 `*.ai-generated.json`（提示词、模型、时间、费用、建议图注）；投稿时按目标期刊的 AI 政策声明。
- 不生成假数据、不伪造显著性星号、不动实验原图、不改 P 值。
- 图注和图要对得上：这一项**靠你和会审的人**判（`check` 只做确定性硬指标，不比对自然语言图注内容）。
- 拿不准目标期刊对 AI 图的态度时，走代码画矢量图这条路 —— 这条永远安全。

想先看"AI 图会错成什么样"，直接看 `references/prompt-library.md` 的「AI 图必错的三件事」和 `references/failure-modes.md` 的样例。

## 常见失败恢复

| 症状 | 真实原因 | 怎么办 |
|---|---|---|
| 付费接口报 `Invalid token`，但 key 明明是刚复制的 | **余额为 0**，不是密钥坏了（网关就这样回） | `node scripts/fig.mjs wallet` 看余额 → 去充值页充 ¥1 再试 |
| `No available channel` / 上游无可用渠道 | 这个模型在当前网关没渠道（图片模型比对话模型更容易没渠道） | 别换 key 重试；用 `--models` 换成默认 `gpt-image-2.5-1k`，或过一会儿再试 |
| `export` 说导不出 PNG | 机器上没有 Chrome，也没有 ImageMagick | 先交矢量：SVG/PDF 大多数期刊直接收（Nature 首选 PDF/EPS）。装 Chrome 后重跑 `export` |
| `check` 报"字号小于期刊下限" | 图是缩放进栏宽的，原始字号跟着缩小了 | 改 `figure.json` 的 `font_size_pt` 调大（Nature 5–7 pt、Elsevier 正文 7 pt），再 `render` + `check` |
| `check` 报"红绿同图且无色盲兜底" | 用了默认红/绿 | 换 `palette: "okabe-ito"` 或给红绿加线型/形状区分，再 `check` |
| 文字溢出节点/画布被裁 | 字数太多、节点太窄 | 缩短 `label`、把细节挪进 `sub`、或加大 `layout.node_w_mm` / `gap_mm` |
| `review` 里个别成员没答上来 | 单模型超时或该模型无渠道 | 看 `review.json` 的 `failed`，不影响整体结论；重要结论自己再核一遍 |
| `review` 某条输出明显没说完 | 成员模型被 token 上限截断 | `review.json` 里该条会标 `truncated: true`；这条建议别采信，自己再判 |

## 六类图怎么选（详见 `references/figure-types.md`）

| 你要表达 | 用哪类 | 面板数 |
|---|---|---|
| 一条处理流水线、方法总览 | `pipeline` | 3–6 段 |
| 系统/模块之间的组成与依赖 | `architecture` | 4–9 个块 |
| 一个机制"为什么这样起作用" | `mechanism` | 1 主图 + 2–4 辅 |
| A 和 B 谁更好、几组对比 | `comparison` | 2–4 组 |
| 概念示意（AI 或代码均可） | `concept` | 1 |
| 封面 / TOC graphic | `toc` | 1 |

期刊规格（栏宽/最大高度/最小字号/DPI/格式/字体/色彩）逐条带官方链接和核实日期，在 `references/journal-specs.md`；拿不准的都标了「待核」，没有编数字。

## 配套文件

- `references/figure-types.md` —— 六类图：适合什么内容、好坏对照、常见错误、面板数与阅读顺序
- `references/journal-specs.md` —— Nature/Science/Cell/IEEE/Elsevier/Springer/ACM/PLOS/中文核心/学位论文
- `references/prompt-library.md` —— 概念图/封面/TOC 英文提示词模板 + "AI 图必错三件事"的规避写法
- `references/review-rubric.md` —— 修改清单格式（第一位）+ 三维打分口径（视觉 40 / 信息 40 / 合规 20，仅作比较）
- `references/failure-modes.md` —— 被打回的图长什么样：症状 → 原因 → 改法 → 对应命令
- `assets/journal.mplstyle` —— 用 matplotlib 的人可以 `plt.style.use(...)` 直接套期刊风格

## 铁律

1. **数据图必须由真数据画出**，AI 出的图不许当数据图，这是投出去会被撤稿的事。
2. **引用官方规范别背数字**：不确定就标「待核」，让用户去看期刊当年的 Guide for Authors。`journal-specs.md` 里每条都写了核实日期。
3. **报错必须带下一步**：`check` 的每条 issue 都有 `fix`，没有 fix 的报告等于没报。
4. **不要拿用户的余额做"验证"**：想确认能不能用，跑免费的 `check`/`render`/`wallet`，别去刷 `concept`。
5. **会审只信清单，不信分数**：分数用来比较两版谁更稳，能照着改的是清单；成员被截断的条目标了 `truncated`，别采信。
6. **别把"合规"说成"好看"**：对外一句话永远是"能投、不被退稿"，不是"漂亮"；夸画风是别的工具的赛道。
7. **不替用户上传文件**：除 `concept` 的提示词和 `review` 的图注/检查摘要之外，任何用户数据不得离开本机；新增这类行为必须先写进文档。
