# 可投稿的论文图 · paper-figure

**图不是画出来的，是算出来的。**

**期刊合规排版 + 硬校验 + 会审清单。** 把「图被期刊退回重画」变成一条命令：结构图、流程图、数据图按目标刊的栏宽/字号/DPI/格式出矢量，本机免费自检，多 AI 只给「能照着改的清单」。

装一次，本地渲染和检查一分钱不花，**论文数据不上传**。

---

## 30 秒看懂

### 三句痛点

1. 用 PPT / draw.io 拼的框架图，投出去被一句 "figures do not meet our specifications" 退回来 —— 单栏要 89 mm 你交了 120 mm，字号 4 pt，导出 150 dpi。
2. 用 Origin / matplotlib 出的数据图，默认样式丑、图例挤、红绿两条线色盲分不出、坐标轴连单位都没写，EPS 里字体还没嵌。
3. 让 AI 一键生成"论文配图"，图里文字是乱的、箭头方向是反的、数字是编的 —— 这比丑严重得多，这是学术诚信问题。

> 这批人愿不愿意反复用工具？参考口径：同类**免费**学术审查类技能在 WorkBuddy 上装机 538、调用 4,596 次（这是免费工具的使用量，**不代表付费转化**，只能当"愿意反复使用"的留存信号）。

### 这张图以前 vs 现在

| 项目 | 以前（PPT / 默认样式 / AI 一键图） | 现在（本技能） |
|---|---|---|
| 尺寸 | 随手画，超栏宽，被要求缩图后字全糊 | 按期刊栏宽排版（Nature 89/183 mm、Elsevier 90/190 mm…），每条带官方链接与核实日期 |
| 字号 | 4 pt，缩到栏宽后更小 | 落在期刊下限以上（Nature 5–7 pt、Elsevier 正文 7 pt、PLOS 8–12 pt） |
| 分辨率 | 屏幕截图 72 dpi 拼进去 | 矢量优先；要位图就按最终尺寸导 300/600/1000 dpi |
| 嵌入与格式 | EPS 里字体没嵌，别的机器打开变字体 | 字体嵌入/转曲、按刊选格式（Nature 主图矢量、PLOS TIFF/EPS） |
| 配色 | 红绿并置，灰度打印分不出 | 默认色盲安全调色板（Okabe–Ito，与 Nature 官方色板同源） |
| 文字 | 溢出框、被画布裁掉、中英两套字体 | 自动估算溢出 + 统一字体策略 |
| 可复现 | 改一个字要重画半张图 | 改 `figure.json` 一行，重跑一条命令 |
| AI 图 | 文字乱码 / 数字造假 / 冒充结果图 | AI 只出概念示意/封面/TOC，产物强制带 `*.ai-generated.json` |

一眼就想看懂的差别：**不能投的图，箭头穿框、图例压曲线、字小到要放大；能投的图，箭头只朝一个方向、图例在图内、缩到 89 mm 还读得出来。**

### 为什么不是"让大模型写段 matplotlib 代码"

大模型能给你一段跑得起来的 matplotlib，但画不出**合规格**的图。它不知道 Nature 单栏 89 mm、图高上限 170 mm，不知道主图只收矢量不收 TIFF，也不会替你嵌字体、核色盲、对面板顺序。我们给的是**对着官方作者指南逐条核过的模板**（单双栏宽、最小字号、字体嵌入、色彩模式、300/600/1000 dpi、面板 a/b/c、色盲配色、EPS/PDF/TIFF），每条规范都带**官方 URL 和核实日期**（`references/journal-specs.md`）—— 这是大模型给不了、也背不下来的东西。

### 可信边界：AI 在哪一步会翻车

不是"AI 不够强"，是**我们知道它一定错在哪，所以不让它碰那一步**：

| AI 会翻的车 | 翻车长这样 |
|---|---|
| 图里的文字 | `Sclentlst`、`Resuit`，中文变方块或臆造字 |
| 图里的数字 | `0.85` 变 `O.85`，坐标轴刻度随机跳（0, 3, 7, 12） |
| 箭头方向 | 想画 A→B 画成 B→A，两端都有头，三箭头汇入却有一根反向 |
| 数据 | 看着像柱状图/曲线图，但数值是编的 —— 撤稿级问题 |

所以顺序是：**能确定性表达的（结构/流程/机制/对比/数据）用代码画；只有要给感觉的（概念示意/封面/TOC）才让 AI 出草图，标好来源，文字和箭头后期补。** 更多样例见 `references/prompt-library.md` 与 `references/failure-modes.md`。

**反面教材（有出处，二手报道）**：2026-04-18 NEJM《Images in Clinical Medicine》一张病例照片里，皮尺刻度被 AI 处理后读起来是「1, 3, ?, 4, ?, ?, ?, ?, 9」；作者承认用 AI 把皮尺移到顶部、且未按该刊要求披露，4-29 撤稿，距发表 11 天（[澎湃·湃客报道](https://m.thepaper.cn/newsDetail_forward_33178035)，2026-11-03 采集；NEJM 原文与 PubPeer 帖未直接核实，**待核**）。这就是"AI 图不许当数据图"最硬的一条理由。

---

## 数据不出本机

- `init` `spec` `chart` `render` `check` `export` **全部本机执行、不联网**；你的 CSV、图注、未发表结果**不会上传**。
- 只有两处会走网络：`concept` 发**英文提示词**；`review` 发**图注文本 + 合规检查摘要**（可选，不跑就不发）。
- 生成的 SVG/PNG/PDF/TIFF 都在 `out/`，自己保管。投稿前把 `out/` 加进 `.gitignore`，别把未发表图推上公开仓库。

---

## 安装

要求：**Node ≥ 18**（自带 fetch 就够），**不需要 npm install，不需要 Python，不需要 Illustrator**。

```bash
git clone https://github.com/u-claw-os/paper-figure.git
cd paper-figure
node scripts/fig.mjs wallet        # 免费：看密钥来源和余额
```

想在 AI 助手里直接用（Claude Code / Codex / Cursor / DSH 等）：把整个目录放进技能库，例如

```bash
cp -r paper-figure ~/.dsh/skills/paper-figure
```

之后说「帮我画论文里的框架图，投 Nature 子刊」就会触发。

---

## 四条命令就能出图

```bash
# 1) 建工作区（brief.md / figure.json / data/ / out/）
node scripts/fig.mjs init ./fig1

# 2) 把 brief.md 里的大白话变成结构化 figure.json（本地解析，不调模型，免费）
node scripts/fig.mjs spec ./fig1

# 3) 出图：结构/流程/机制/对比用 render；有 CSV 的数据图用 chart
node scripts/fig.mjs render ./fig1 --journal nature
node scripts/fig.mjs chart  ./fig1

# 4) 投稿前自检（免费，每条报错都带"怎么改"），然后按期刊规格导出
node scripts/fig.mjs check  ./fig1 --journal nature
node scripts/fig.mjs export ./fig1 --formats png,pdf --dpi 600
```

`check` 全绿但还想知道"编辑/审稿人会挑什么"，再花几分钱：

```bash
node scripts/fig.mjs review  ./fig1 --tier econ   # 多 AI 会审：先给修改清单，分数仅用于比较
node scripts/fig.mjs concept ./fig1 --n 2         # 只有概念图/封面/TOC 才用，¥0.03/张
```

会审的产出是**动词开头的修改清单**（"把 panel b 图例字号从 4 pt 改成 7 pt"），不是一句"8 分，还行"。三维分数（视觉 40 / 信息 40 / 合规 20）只用来比较两版谁更稳；成员输出被 token 截断的会标 `truncated`，不采信。

所有命令都是"正常结果走 stdout 的 JSON，人话提示走 stderr，失败给 `{ok:false,error,fix}` 且非 0 退出"，方便自己接自动化。

---

## 多少钱

| 动作 | 费用 |
|---|---|
| 渲染 / 检查 / 导出 / 看钱包 | **¥0**（纯本地） |
| AI 概念图（`concept`） | 约 **¥0.03/张** |
| 多 AI 会审（`review --tier econ`） | **¥0.01–0.07/轮** |
| 一张图从草稿到能投 | 约 **¥0.05–0.15** |

**¥1 大概能做十张图的完整打磨。** 不装 Illustrator（订阅费）、不买 Origin、不用四张外币卡。

价格锚点（**2026-11 官方页面价**）：[BioRender](https://www.biorender.com/pricing) 免费版明文禁止用于发表、个人版 **$35/月**起；[Origin 官方店](https://store.originlab.com/) OriginPro 2026b 个人年订 **$310/年**；[Illustrator 官方方案页](https://www.adobe.com/products/illustrator/plans.html) **$22.99/月**起（促销档，档位与单应用/全套的对应关系**待核**）。

密钥按这个顺序自动找：`--key` > `$XIAPAN_API_KEY` > `~/.dsh/aigc-wallet.json` > `~/.uking/device.json`。都没有就先绑一个（余额 0），然后到这里充值（支付宝）：

```
https://u-claw.org.cn/recharge?key=<你的key>
```

一个钱包通用于同系列的会诊、出图、出歌等技能。

---

## 可信边界与学术诚信（这是产品的一部分，不是免责声明）

- **AI 生成的图只能做概念示意、封面、TOC graphic、答辩/基金本子示意图。**
- **AI 图不许当数据图、结果图、统计图。** 用 AI 画"柱状图"投出去 = 编数据，是撤稿级别的问题。
- 每张 AI 产物旁边落一份 `*.ai-generated.json`（模型、提示词、时间、费用、建议图注）；投稿时按目标期刊的 AI 政策声明。
- 不生成假数据、不伪造显著性、不修饰实验原图。
- `check` 会主动报"AI 图被当数据图用"这一类 error，直接阻断。
- 图注和图的对齐靠你和会审的人判 —— `check` 只做确定性硬指标（尺寸/字号/DPI/溢出/色盲/字体），不比对自然语言图注内容。

投稿前请自己再看一遍目标期刊当期的 *Guide for Authors* —— 图标规范会改。`references/journal-specs.md` 里每条都标了核实日期，查不到的写「待核」并说明去哪儿查，我们不放没出处的数字。

---

## 谁不该用

- **没有数据，却想先"出一张数据图"**：那是造数据，这里没有变通。
- **要插画级美术图或图标素材**（细胞、器材、分子图形）：用 BioRender / Figdraw / Illustrator，我们不卖素材库。
- **要在线拖拽画布**：用 Figma / draw.io。
- **要"保证一次过审"**：期刊规范会变，我们只保证**可查、可改、有出处**（每条规范都有官方 URL 和核实日期，投稿前你能自己再核一遍）。

---

## 常见问题

**`Invalid token`，但 key 是刚复制的**
余额为 0，不是密钥坏了。跑 `node scripts/fig.mjs wallet` 看余额 → 去充值页充 ¥1。

**`No available channel` / 上游无可用渠道**
这个模型在网关当前没有渠道（图像模型比对话模型更容易没渠道）。用默认的 `gpt-image-2.5-1k`，或换时间再试，别反复重试烧钱。

**导出 PNG 失败，说没有栅格化工具**
机器上没有 Chrome 也没有 ImageMagick。先交矢量（PDF/EPS/SVG，多数期刊直接收，Nature 主图首选 PDF/EPS）；装好 Chrome 后重跑 `export`。

**字号被判太小**
图是按大画布画的、缩到栏宽后字号跟着缩小。改 `figure.json` 的 `font_size_pt` 调大再 `render` + `check`。

**会审说了一堆，我该信哪条**
信 `fixes`，不信分数；标了 `truncated: true` 的那几条跳过。改完先跑免费的 `check` 复验。

---

## 目录

```
scripts/            CLI 与渲染/检查/导出/AI 桥（零依赖）
references/         六类图、期刊规格、提示词库、会审清单规则、失败模式
assets/             journals.json / palettes.json / journal.mplstyle
examples/           示例工作区（生成后可直接改）
```

先看这三篇再动手：`references/figure-types.md`（选错图类型最致命）、`references/journal-specs.md`（官方链接 + 核实日期，核心资产）、`references/failure-modes.md`（被打回的图长什么样）。

## 同钱包的其他技能

- [dsh-aigc](https://github.com/hfshfg/dsh-aigc) —— 出图 / 出歌
- [dsh-panel](https://github.com/hfshfg/dsh-panel) —— 多 AI 会审面板
- 全球模型会诊（model-consult）—— 同一个问题多家模型独立作答 + 裁判汇总
- 虾盘云充值：[u-claw.org.cn](https://u-claw.org.cn)

## 许可

MIT。版权人：he fangsheng（hfshfg）。
用这个技能出的图，版权归你（和你所在单位）——我们只写了排版的代码。
