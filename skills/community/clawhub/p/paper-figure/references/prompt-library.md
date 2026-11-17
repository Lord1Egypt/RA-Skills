# 提示词库：概念图 / 封面 / TOC graphic

> 这套提示词只服务三件事：**给方向、给风格、给构图**。
> AI 图**不许当数据图**（见 `SKILL.md` 学术诚信边界）。所有 `concept` 产物旁都会落一份 `*.ai-generated.json`。

## 提示词的骨架

```
[主体与关系] + [视觉风格] + [构图与视角] + [配色] + [留白与画幅] + [负面词]
```

一句话写错，整张图就废。下面每段都可以直接抄，方括号换成你的内容。

**通用前缀（推荐每张都带）**

```
Flat vector scientific illustration, clean thin outlines, muted professional palette,
no text, no letters, no numbers, no arrows crossing each other, generous white space,
single panel, white background, suitable for a journal figure, 1024x1024
```

---

## 1. 概念示意图（concept / 方法示意）

**模板 A：抽象流程感**

```
A minimal flat-vector diagram suggesting a three-stage scientific workflow:
raw data shown as abstract shapes -> a processing core -> a structured result.
Use simple geometric forms, one accent colour for the core, two neutral tones elsewhere,
soft rounded rectangles, thin consistent strokes, generous spacing between stages,
left-to-right composition, no text, no numbers, no labels, no arrows, white background,
clean journal style, 1024x1024
```

**模板 B：尺度/层次感（适合"从微观到宏观"）**

```
A calm schematic illustration showing three nested scales of the same phenomenon,
from a small particle-like cluster to a larger network, arranged concentrically,
flat vector style, thin outlines, muted scientific palette, high contrast between
foreground and background, plenty of negative space, no text, no numerals,
no signs, no arrows, white background, 1024x1024
```

**模板 C：隐喻型（审稿友好，不抢信息）**

```
A restrained metaphorical illustration: a single abstract "engine" made of simple
geometric modules, suggesting modular composition and flow, flat vector, two colours
only, thin strokes, centred composition, lots of white space, no text, no symbols,
no numbers, white background, editorial journal style, 1024x1024
```

## 2. 封面（cover art）

```
Journal cover artwork, single dominant abstract subject occupying 60-70% of the frame,
flat vector with subtle paper texture, restrained palette of three colours,
dynamic but not busy, strong silhouette that stays readable as a small thumbnail,
generous white space at the top, no text, no typography, no logos, no numbers,
no arrows, white background, high contrast, 1024x1024
```

> 封面要"缩略图还能认出主体"。生成后缩小到 **30 mm 宽**看一遍，认不出就重画。

## 3. TOC graphic / graphical abstract

```
Graphical abstract for a journal table of contents: one clear visual metaphor for
[your topic], three simple elements maximum, strong contrast, bold simple shapes,
flat vector style, no gradients, no text, no words, no numbers, no arrows,
centred composition with generous margins, white background, 1024x1024
```

> 各刊对 graphical abstract 的尺寸/字数要求不同（本仓库 `journal-specs.md` 里 **Cell 一栏仍标待核**）。生成的是**素材**，最终尺寸要按目标刊裁。

---

## 风格词（挑一套，别混用）

| 想要的感觉 | 用的词 |
|---|---|
| 期刊插图（最安全） | `flat vector, thin consistent outlines, muted professional palette, white background` |
| 编辑插画感 | `editorial illustration, subtle grain, limited palette, hand-drawn line quality` |
| 等距示意 | `isometric, soft shadows, clean geometry, pastel accents, white background` |
| 极简符号 | `minimal pictogram, single-weight lines, two colours, high negative space` |
| 学术海报感 | `bold flat shapes, high contrast, three-colour palette, strong silhouette` |

**不要用**：`photorealistic, hyperdetailed, cinematic lighting, glowing neon, 3D render, cyberpunk, sci-fi HUD` —— 缩到 89 mm 全糊，而且一眼 AI。

## 构图词

| 想要 | 用的词 |
|---|---|
| 从左到右 | `left-to-right composition, horizontal flow` |
| 上到下 | `top-to-bottom composition, vertical stack` |
| 主次分明 | `single dominant focal element, rule of thirds` |
| 对称稳 | `centred, symmetrical composition` |
| 留白 | `generous negative space, clean margins, subject 60% of frame` |

## 负面词（每张都带）

```
no text, no letters, no words, no numbers, no labels, no captions, no watermarks,
no logos, no signatures, no arrows crossing, no cluttered details, no photographic
elements, no human faces, no 3D bevels, no neon glow, no rainbow gradients
```

---

## 可信边界：AI 图必错的三件事（文字、数字、箭头方向）

这一节同时是"AI 会翻成什么样"的**样例库** —— 我们不是笼统地说"AI 仅供参考"，而是把翻车点、翻车后的样子、以及怎么绕开写清楚。这三样是扩散模型的系统性弱项，不是"提示词写得好就能解决"。正确策略是**绕开**，而不是求它画对。

### ① 文字

- **翻车长这样**：`Sclentlst`、`Resuit`、`Tab1e 2`；中文直接变方块或臆造字。
- **规避写法**：提示词里写死 `no text, no letters, no words`；把要标的位置画成**空白框/色块**，后期在矢量软件或用 `render` 排字。
- **绝对不要**：让 AI 写中文标题、坐标轴标签、化学式、公式。
- **代价对比**：后期排 6 个标签 5 分钟；图里带错字被审稿人发现，是"作者没看自己的图"。

### ② 数字

- **翻车长这样**：`0.85` 变 `O.85` 或 `8.5`；坐标轴刻度随机跳（0, 3, 7, 12）。
- **规避写法**：提示词 `no numbers, no axes, no charts, no data plots`；**凡是带刻度的图一律用 `chart` 命令从真 CSV 画**。
- **硬边界**：AI 生成的"柱状图"即使数字碰巧对，也不是从你的数据来的 —— 那是造数据。

### ③ 箭头方向

- **翻车长这样**：想画 A→B，画成 B→A；箭头两端都有头；三条箭头汇进一个点却有一根是反向的。
- **规避写法**：
  1. 提示词里**明确方向**并把结构说死：`a single arrow pointing from left to right, arrowhead on the right end only, no bidirectional arrows`；
  2. 更好的是**根本不要 AI 画箭头**：提示词加 `no arrows`，用 `render` 的 `edge` 补，方向 100% 可控；
  3. 已经生成了就必须**逐根检查**：数一下几根、每根哪端有头、标签贴在头还是尾。
- **验收动作**：把图发给一个没看过你正文的人，让他用一句话说"从哪到哪"。他说反了，就是画反了。

### 三件事的统一兜底

```
生成（只出画面，不要文字/数字/箭头）→ 挑选 → 矢量化或重画 → 用代码补文字与箭头
```

本技能里对应的命令：`concept`（生成）→ `render`（用 `nodes` / `edges` 补结构和箭头）→ `check`（查文字溢出、字号、色盲）→ `review`（让人挑"图说的和我想说的是不是一回事"）。

---

## 生成多少张、怎么选

- 一次 `--n 2`：**只花 ¥0.06**，够看两个方向；不要一次刷十张。
- 选的标准顺序：**缩小能看懂 → 没有文字/数字 → 箭头方向对 → 风格贴期刊**。
- 选中之后把它当"草图"：结构自己用 `render` 重画一遍，风格参考它。这样图才是可改、可复现的。

## 一个可抄的完整会话

```bash
node scripts/fig.mjs init ./fig2
# 编辑 ./fig2/brief.md：写清"要一张概念示意图，主题是 XXX，横向三段式，不要文字"
node scripts/fig.mjs spec ./fig2
node scripts/fig.mjs concept ./fig2 --n 2        # ¥0.06，出两张草图 + .ai-generated.json
# 看图挑一张 → 用 render 把结构自己画一遍（nodes/edges），文字与箭头全部可控
node scripts/fig.mjs render ./fig2 --journal nature
node scripts/fig.mjs check ./fig2 --journal nature
```
