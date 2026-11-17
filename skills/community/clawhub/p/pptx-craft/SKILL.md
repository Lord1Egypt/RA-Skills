---
name: pptx-craft
description: "把结构化数据/看板/报表/标准HTML渲染成【可编辑】PowerPoint(.pptx), 重点=高质量排版(不重叠/有气口/不裁切)。引擎用文本优先多遍布局+模板克隆——你给PPT模板路径, 它自动测量可用区、原生生成内容填进去(零复制粘贴, 继承主题)。另附通用HTML→PPT解析器(html2ppt.py, 契约驱动三层检测, 零专属类名)。触发词: 做一份可编辑PPT / 用我的模板生成PPT / 把这个看板导出成PPT / HTML转PPT / pptx-craft。"
version: 1.2.3
slug: pptx-craft
displayName: PPT Craft · 可编辑PPT渲染引擎
summary: 把结构化数据/看板/标准HTML渲染成可编辑PowerPoint，文本优先多遍布局+模板克隆，不重叠/不裁切/有气口。
license: MIT
category: 办公效率
platforms:
  - WorkBuddy
agent_created: true
---

# PPT 渲染引擎 (数据模型/标准HTML → 可编辑PPT · 模板克隆 / 尺寸锚定)

> 本技能包含两层: **① 纯原语引擎 `pptx_flex_engine.py`**(吃数据模型, 文本优先多遍布局+校验) 和
> **② 通用 HTML→PPT 解析器 `scripts/html2ppt.py`**(契约驱动三层检测, 把任意标准 HTML 解析成数据模型再走引擎)。

## Positioning (价值观: 主流程 = 资料 → HTML(浏览器验收) → PPT)

- **主工作流(已与用户锁定)**: 资料汇总目录 → 生成 HTML(浏览器里验收版面) → 转 PPT(演讲+归档)。
  **HTML 是一等输入**, 不是模式违背; 画布轴是互补通道。
- **引擎内核只认数据模型** —— HTML 由 `html2ppt.py` 通用解析成数据模型, 再交引擎渲染。
  解耦保证: 引擎可独立复用(画布/表单/JSON 都能上车), 解析器可独立演进。
- **PPT 模板是尺寸锚点**。收到请求第一步就确认"有没有专用模板"; 有模板则内容以模板真实可用区为准**原生生成**, HTML/PPT 尺寸天然一致。
- **"尺寸不匹配能不能自适应"是个伪问题**: 当模板作锚点、内容原生生成时, 没有第二个尺寸需要去匹配 —— 自适应 = 以模板为准直接生成, 而非事后缩放去凑。

## 通用 HTML→PPT 解析契约 (html2ppt.py · HTML 编写规范)

`scripts/html2ppt.py` 是**通用**解析器: 零专属类名、只认标准 HTML 结构 + 通用契约 class。
用法: `python scripts/html2ppt.py input.html --out out.pptx --preview-dir previews --qa qa.json`

**三层检测(优先级从高到低)**:
- **T1 语义元素直判**: `h1-h3`(页标题) / `table`(表格) / `ul,ol`(列表) / `section`或含标题的顶级`div`(分章)。
- **T2 通用契约 class**(正则模糊匹配, 写 HTML 时用这些词可获最稳解析):
  | 契约词 | 识别为 | 示例 class |
  |--------|--------|-----------|
  | `hero / cover / title` | 封面页 | `class="hero"` |
  | `head / header / kicker / sub` | 页眉区(眉标+标题+副题) | `class="head"` |
  | `card / box / item / panel / tile` | 卡片 | `class="card"` |
  | `grid / cards / row / cols / wrap` | 卡片栅格容器 | `class="grid"` |
  | `timeline / steps / stage / phase` | 时间线/阶段(竖向序列) | `class="timeline"` |
  | `contain / container / body / content` | 正文包裹容器(下钻) | `class="contain"` |
- **T3 几何/文本启发兜底**: ≥2 个相似兄弟 div → 栅格; 有边框感+内部标题 → 卡片;
  行首日期(`2024.06`/`2024-06`)或编号正则 → 时间线/编号序列; 其余 → 文本块。

**硬规则**:
- 解析器内 **严禁出现任何单一 HTML 文件的专属类名**(如 `.rv`/`.pit`/`.conv`) —— 一旦需要, 说明契约或启发层有缺口, 应补契约而不是补特例。
- 分页/高度铁律: 估算公式必须与渲染公式**严格一致**(同 pad/同 breath/同 min 字号);
  竖向序列(timeline/numbered)与 grid **超页高时拆页, 绝不压缩**(压缩=重叠之源)。
- QA 双层: L1 几何(0 错误才算过) + L2 填充率(<55% 标空白风险; hero 与纯文本陈述页豁免)。

## Overview

Generate editable, pixel-precise PowerPoint files **without hand-computing absolute
coordinates**. The root cause of "PPT 永远做不好排版、永远元素重复、永远没气口" is that
PPT / pptxgenjs is an absolute-positioning engine: 50+ elements = 200+ hand-written
`(x,y,w,h)`, and one miscalculation cascades into overlap/truncation. Worse, even when
coordinates are correct, the gaps (气口) between elements end up too tight because the
layout is a single sequential pass that packs elements to "minimal fit".

This skill replaces hand coordinates with a **text-first multi-pass layout** that
simulates how a human actually builds a slide:

```
人类工作流                        引擎对应 Pass
─────────────────────────────    ──────────────────────────────
1. 按尺寸/比例画区域边框          Pass0   flex 容器(区域框)
2. 先放文字(占地最大),四周留白;    Pass1   文本优先放置(字体度量测高 + pad 气口)
   放不下则缩字号(不删内容)        Pass2   字号自适应(溢出按比例缩,保最小字号)
3. 再放装饰(条/图)填空余空间       Pass3   装饰按"文字块底部+气口"定位(填空者)
4. 初稿→QA→二稿→QA→终稿           Pass4-5 QA 迭代(留白不足全局缩字号重排,最多3轮)
```

Key guarantee: **no overlap, no truncation, and measured breathing room (气口)** — the
validator refuses to write the file unless every element is in-bounds, non-overlapping
across groups, and cross-group gaps meet a `MIN_BREATH` floor.

## When to use

- User needs an **editable** PPT (not a screenshot image) with **high layout fidelity + 气口**.
- User explicitly wants "方法3" (text-first flex engine + validator) over "方法1" (screenshot).
- User has a dashboard / report / data page — designed in HTML, a design canvas, OR just a
  data model / spreadsheet — and wants it re-rendered as a clean editable slide with proper spacing.
- **模板克隆场景**: 用户有现成 PPT 模板(公司汇报模板等), 要把内容填进去且继承主题/页脚/logo。
- Do NOT use for one-off quick mockups where a screenshot (方法1) is acceptable — that
  is faster and lower-cost.

## Architecture (6 layers)

```
① 输入层   : 数据模型(真相源) + 设计令牌(TOKENS) + 间距令牌(SP) + 密度(DENSITY)
             —— HTML/画布是可选的可视化兄弟产物, 不进引擎输入
② 虚拟画布 : 1440×680 px 抽象坐标空间(可随目标比例重设 VW/VH), 均匀缩放+居中 映射目标可用区
③ 容器系统 : Row/Column + flex 权重, 仅用于"区域框"层级(区域内部改文本优先)
④ 组件库   : KpiCard / CompareCard / build_chart / build_progress  —— 内部文本优先, 装饰填空
⑤ 文本优先布局 : layout_texts() 字体度量测高 + 上下左右 pad 气口 + 字号自适应(保最小,不删内容)
⑥ 校验层   : 写文件前强制 越界 + 跨组重叠 + 留白下限(防拥挤) 检测; 不过则拒绝产出(终稿轮)
⑦ QA迭代器 : 初稿→二稿→终稿, 用留白提示驱动全局字号缩放(G_TS)
```

> **气口(呼吸感)是怎么解决的 (v3 三条杠杆)**:
> 1. **文本优先 + 字体度量**: 文字先"占地"，上下左右按 `pad` 留气口、多文字间按 `breath` 留气口，
>    尺寸由字体度量真实估算（宁多勿少，文字绝不裁切），不再"塞满即止"。
> 2. **间距令牌 + 密度系数**: 所有 gap/padding 取自 `SP` 阶梯表，由 `DENSITY` 整体缩放
>    （1.0 紧凑 / 1.2 舒适 / 1.4 宽松）—— 调一个旋钮即可整体松紧，不用逐块挪。
> 3. **QA 迭代器**: 若终稿仍有留白提示，全局缩小字号 `G_TS`（每轮 -0.06）重排，最多 3 轮，
>    用"规则+迭代"替代"人眼反复截图调"。

## Workflow

### ⚠️ Step 0 — 确认有无专用 PPT 模板 (MANDATORY, 任何技能请求的第一步)
收到技能请求时, **第一件事**就是问用户: **"你有没有专用 PPT 模板？"**
不要先谈 HTML 尺寸、不要先问画布比例 —— 模板才是唯一锚点。这个回答决定整个输入契约与引擎首动作。

**为什么先问模板 (尺寸一致性的根因)**:
PPT 翻车第一因是"生成物与目标模板尺寸/比例不一致 → 复制进去变小/错位"。当模板作锚点,
内容永远按模板本身的真实可用区**原生生成**, 不存在"另一个尺寸去匹配"的对象 ——
于是"HTML尺寸和PPT尺寸不匹配、能不能自适应"这个伪问题从根上消失: **自适应不是去匹配, 而是以模板为准直接生成。**

**Branch A — 无专用模板 (`use_generic: true`)**
- WB 自行设计/加载**内置通用模板**(默认标准16:9, 33.87×19.05cm, 含内置主题token)。
- 引擎动作: 新建 `Presentation` + 设尺寸 + 文本优先多遍 + QA。
- 仅需确认输出比例(默认16:9), 无需路径。

**Branch B — 有专用模板 (`has_template: true`)** — 用户只需提供:
1. **`template_path`** (必填): 真实 `.pptx` 模板路径。
2. **`start_page`** (可选, 默认自动探测首个"正文页"): 内容从这一页开始生成; 模板封面/目录/结构页(P1-3等)一律不动。
- **可用区由 WB 自动测量, 用户无需画框、无需报尺寸**:
  引擎加载模板 → 扫描目标页**及其版式(layout)/母版(master)的已有形状** → 按规则算可用区:
  - 左右: 按 PPT 模板尺寸各留 `MARGIN_CM`(默认1cm) → `x∈[M, W-M]`。
  - 上下: 在模板已有元素基础上算(内容不得压已有元素), 各留 `MARGIN_CM`:
    * 排除面积≈整页的形状(全屏背景图), 避免误判为障碍物;
    * 形状中心在上半=页眉区取 `max(页眉底)+M`, 在下半=页脚区取 `min(页脚顶)-M`;
    * 无页脚页 bottom 回退 `H-M`; 溢出续页时对后续页用同规则重算。
  - **必须同时扫描 `slide.shapes` + `slide.slide_layout.shapes`**(页眉页脚通常在版式上, 漏扫会压页脚)。
- 引擎动作: `Presentation(template_path)` → 克隆 → 在算出的可用区**原生生成**内容(直接 add 进 spTree, 零复制粘贴)。主题/字体/页脚/logo 全继承。
- (可选硬覆盖) 极少数模板自动测量不准时, 才退化为用户在模板里标命名形状 `CONTENT_AREA` 或手填包围盒 `(x_cm,y_cm,w_cm,h_cm)`。

> 经验: 曾用「缩放粘贴」(整页生成→×0.796缩放进可用区) 导致"整体小一圈"; 正确范式是**虚拟画布直接映射到可用区 + 原生生成**, 字号走 px→pt 不随区域缩小。

Reference sizes (used by Branch A default or as sanity check):
| Type | Width × Height | Ruler range | Aspect |
|------|---------------|-------------|--------|
| Standard 16:9 | 33.87 × 19.05 cm | -16~+16 / -9~+9 | 1.78:1 |
| Standard 4:3 | 25.4 × 19.05 cm | -12~+12 / -9~+9 | 1.33:1 |
| Custom ultra-wide | 31 × 14 cm | -15~+15 / -6~+6 | 2.21:1 |

### Step 1 — Define tokens and data (single source)
Set `TOKENS` (colors/fonts/radii) and a `DASHBOARD_DATA`-style model. This is the **single
source of truth** — keep it consistent with any HTML/canvas sibling so all outputs stay
aligned (but HTML/canvas are optional previews, not inputs). If the data is "live", pass a
snapshot at export time (PPT is a period snapshot, not realtime).

### Step 2 — Build the virtual canvas + coordinate mapper
Use `VW,VH` as the virtual pixel canvas. **VW/VH should be derived from the target available
area's aspect ratio** (not hardcoded to one size) so the layout re-flows natively:
- **Branch A (generic)**: `VW,VH` → slide size aspect; `SCALE = min(SLIDE_W/VW, SLIDE_H/VH)`, `OFFX` centers.
- **Branch B (template clone)**: set `VW=1440, VH=round(area_h/area_w*1440)`, `SCALE=area_w/VW`,
  and `OFFX/OFFY` = available-area top-left EMU — content placed *inside the frame*, natively.
Map with **uniform scale + area anchoring** (no vertical squeeze). Helpers `X/Y/W_/H_/FS` convert virtual px → EMU/pt.
Slide size: `prs.slide_width = Emu(target_cm * 360000)` (Branch A only; Branch B reuses template size).

### Step 3 — Lay out regions with flex containers (never raw coordinates)
Use `hbox(deck, box, items, gap, pad)` and `vbox(deck, box, items, gap, pad)` to carve
**region frames** only. Each item is `{"flex": n, "size": px, "group": "g", "build": fn}`.
The engine computes child positions from weights — change a parent's height and children
reflow. **Note**: flex is used for the region level; inside each card the layout switches
to text-first (Step 4).

### Step 4 — Compose with the component library (TEXT-FIRST inside)
Call `KpiCard`, `CompareCard`, `build_progress`, `build_chart`. Each card:
1. draws its background rect,
2. calls `layout_texts(deck, items, box, pad, breath, ...)` which:
   - measures each text block height via `text_h()` (font metrics, CJK-aware),
   - places text top-down with `pad` (outer) + `breath` (between) 气口,
   - if total exceeds box height, binary-searches a uniform `scale` to shrink all fonts
     (each keeps its `min_fs` — **content never deleted**),
   - returns the `leftover` space below the text,
3. draws decorative elements (bars/chips/legend) into that `leftover` space — decorations
   are "fillers", never the cause of overlap.

This is the core fix for "标题贴边 / 标签没气口 / 批次条拥挤": text owns the space first,
decorations fill what's left.

### Step 5 — Run the validator BEFORE saving
`validate(deck.recs)` returns `(errors, warnings)` and checks three things:
1. **越界** — every element within the target area bounds;
2. **跨组重叠** — any two elements of *different* groups that geometrically intersect
   (same-group = text nested in its card, which is allowed);
3. **留白下限 (防拥挤)** — any two *adjacent* cross-group elements whose edge-to-edge gap
   is `< MIN_BREATH` (default 10px) is reported as a warning.

If `errors` non-empty → **raise, do not write the file**. Warnings do not block (tuning
hints for `DENSITY`/`G_TS`) but a clean run reports "留白校验通过".

### Step 5b — Tune 气口 (no coordinate edits)
Three knobs, in increasing strength:
- `SP_RAW` ladder + `DENSITY` (1.0/1.2/1.4) — global spacing scale; `sp(k)` = `SP_RAW[k]*DENSITY`.
- `pad` / `breath` args inside `layout_texts` — per-card inner 气口.
- `G_TS` (driven by QA iterator) — global font-size scale when gaps still too tight.

The engine also emits `preview.svg` (virtual-coord 1:1) so you can
eyeball 气口 without opening PowerPoint.

### Step 6 — Render and save
`deck.render(slide)` iterates recorded ops into python-pptx shapes. Set slide background
fill, then `prs.save(out)`.
- **Branch A**: save as a new standalone file.
- **Branch B**: save the cloned template (content already inside the available area) — the
  output file is the user's template, filled.

## The bundled engine

`scripts/pptx_flex_engine.py` is a complete, runnable reference implementation (the
switch-migration dashboard case) using the v3 text-first multi-pass architecture.

- Run directly: `python scripts/pptx_flex_engine.py` → produces `migration-dashboard-m3-v4.pptx`
  + `migration-dashboard-m3-preview.svg` (standard 16:9, 33.87×19.05cm single-page editable deck).
- **Before running, resolve Step 0**:
  - Branch A (no template): the script's defaults already target standard 16:9 — just run.
  - Branch B (has template): pass `template_path` (+ optional `start_page`); the engine
    **auto-measures the template's available area** (scans slide + layout shapes) and fills
    it natively — no `CONTENT_AREA` box or manual dimensions needed.
- Adapt: replace `KPI / CMP / BATCHES / DAYS` data + `build_*` functions with target content;
  keep `TOKENS`, `hbox/vbox`, `layout_texts`, `Deck`, and `validate` unchanged.
- Prereqs: `python-pptx` (`pip install python-pptx`). Uses `Microsoft YaHei` for editable
  Chinese text on Windows.

### 声明式驱动层 `scripts/engine_runner.py` （M1–M4 已落地 · 2026-07-27）

`pptx_flex_engine.py` 是**纯原语库**（命令式 API）。`engine_runner.py` 是它之上的**声明式调度层**：读三份 JSON（数据模型 / 版式策略 / 主题规范）→ 渲染成可编辑 PPTX。这是"通用引擎"承诺的落地形态——**不再需要为每份内容手写 py**。

- 用法：`python scripts/engine_runner.py --data data.json --layout layout.json --theme theme.json --out out.pptx [--preview-dir previews]`
- **M1 纯函数**：`render_model(data, layout, theme)` 无副作用、可重入；只写文件是预期输出。
- **M2 八坑防御**：`direction` 必填断言 / 负尺寸硬拦截（引擎层 `Deck.render`）/ `layout_index` 合法校验 / 键值对同行（组件实现）/ CJK 系数 ≥1.0（防换行爆炸）。任一几何错误 → L1 闸门拒绝产出。
- **M3 阶段产物落盘**：三 JSON 由 data/layout/theme 三个专家独立产出落盘；runner 只读三文件，支持**单阶段重跑**（改某阶段只需重跑本脚本，不动其他专家产出）。`layout.json` 可选携带 `area`（layout-expert 实测死区），避免每次重测模板。
- **M4 输入快照**：运行前对三输入文件做 sha256，写入 `<out>.snapshot.json`，打回时精确回退。

> 设计要点：P6 beta 曾用 `gen_p6_py.py` 硬编码（绝对坐标 + 手写 py），正是"易错漏/连锁崩"的反面教材。现统一走 `engine_runner.py` 声明式入口。

## Key rules (non-obvious, learned from real failures)

- **🔴 Step 0 is mandatory — 第一件事就问"有专用模板吗?"**: 模板是尺寸锚点。Branch A 自设计通用16:9;
  Branch B 用户给 `template_path`(+可选 `start_page`), **WB 自动扫描模板算可用区**(无需画框/报尺寸),
  原生生成进 spTree。模板克隆让 PowerPoint 复制粘贴过时(无坐标漂移, 风格自动继承)。
  → 因此"画布/HTML/PPT 尺寸一致性"由模板锚点天然保证, "尺寸不匹配"伪问题消失。
- **可用区自动测量规则**: 扫描 `slide.shapes` + `slide.slide_layout.shapes` + (必要时) `slide.master.shapes`;
  排除全屏背景; 上下按已有元素留 `MARGIN_CM`; **漏扫 layout 会压页脚**(页眉页脚多在版式上)。
- **content_area 是盒不是尺寸**(仅当自动测量不准时作硬覆盖): 手填须问左上偏移。
- **Never hand-write `(x,y,w,h)` for leaf elements** — declare structure, let the engine compute.
- **Text-first, not decoration-first**: always place text (with 气口) before bars/chips;
  decorations fill leftover space. This is what killed the "标题贴边/标签没气口" bugs.
- **Font metrics over eyeballing**: `text_h()` estimates CJK-aware line height; tune the
  `0.98/0.55/0.30` width factors if a font renders differently, but keep them conservative
  (prefer slightly-too-tall over clipping).
- **Auto-shrink but never delete**: `min_fs` per text item guarantees content survives
  even when the frame is tight — the QA iterator then relaxes spacing globally.
- **Always give each card a distinct `group`** so the validator can tell nested-text from
  real overlap. Forgetting this yields false overlap errors or missed collisions.
- **Uniform scale + area anchoring** (not non-uniform): prevents the vertical
  squeeze that makes PPT feel tighter than the HTML source.
- **Method 1 vs 3 split**: method 1 (screenshot) for urgent/low-stakes reporting;
  method 3 (this engine) for anything where the user must edit text in PowerPoint or
  demands zero-drift layout with proper 气口.

### HTML→PPTX 布局保真四法则（layout-expert 铁律 · 2026-07-24 实战沉淀）

> 背景：真实项目里把"横排 HTML"移植成 python-pptx 时，反复出现 **横排变竖排 / 内容顶出模板可用区 / 间距膨胀** 三类翻车。根因是版式策略缺失、测宽偏差、可用区未固化。下列四条为 **layout-expert（范章成）主责铁律**，配合 data / qa / visual 三专家在 SOP 前置拦截。

**法则 ① 方向声明（direction 必填）**
- 数据模型每个区块必须带 `layout.direction: row | column`，**禁止依赖默认竖排**。
- 源是 HTML `flex-row` / `grid` / 卡片并排 → 渲染必须 `hbox` 横排；源是 `flex-column` / 时间线 / 列表 → 才竖排。
- 🔴 反例：`timeline` 的 tags 本应横排小标签，却被写成 `break:True` 强制每 tag 一行 → 单卡高度暴增 +0.35"、三阶段合计溢出 +1.05"。

**法则 ② 测宽校准（CJK 系数按渲染引擎实测）**
- `char_w_pt` 中文字宽系数必须贴近 Microsoft YaHei 真实渲染（≈1.0×fs），**宁高估勿低估**（估算偏低→文本框给矮→真实 wrap 溢出）。
- 改一次系数要重测所有 card 高度，避免连锁膨胀。

**法则 ③ 可用区测量 + 死线（模板基底路线必做）**
- 模板基底路线（`Presentation(tpl)` → 删原 slide → `add_slide(layout[1])`）必须**实测 layout 页眉/页脚占位**，算死可用区 `[x, y, w, h]`。
- 所有 `cy` 累加必须 `≤ 可用区.bottom`；`roi_h` 等动态高度用 `max(剩余空间, 0.45)`，**禁止硬塞 0.75+ 把内容顶出画面**。
- 漏扫 `slide_layout.shapes` 会压页脚（页眉页脚多在版式上）。

**法则 ④ 单一间距源（GAP 只定义一次）**
- 所有区块间距取自**唯一常量**（如 `GAP=0.06`）；**严禁后续重复赋值覆盖**（曾出现第55行 `GAP=0.22` 静默覆盖第45行 `GAP=0.06`，4处累加多吃 0.64"）。
- 改间距只动定义点，不动散落各处的 `+GAP`。

**配套职责（其他专家）**：
| 专家 | 在 SOP 哪一步补强 |
|------|------------------|
| **data-expert（苏通达）** | P1 数据模型加 `layout.direction` 字段，源 HTML 横排信息固化入模型 |
| **qa-expert（严过关）** | L1 几何加 ①方向一致性（渲染 row 数 vs 模型声明）②可用区溢出（元素底缘 ≤ 模板可用区） |
| **visual-review-expert（沈定稿）** | L2 视觉加「横排密度 / 换行合理性」目检（方向对但换行过多也判不合格） |

---

## 实战踩坑经验库（v5→v12 迭代沉淀 · 2026-07-27 定稿）

> **定位**：这是 pptx-craft 引擎在真实项目中从"能跑"到"95%可用"的全部教训。
> 每条记录格式：**现象 → 根因 → 修复 → 归属专家 → 预防规则**。
> 目标读者：任何使用本技能/专家团的人（包括用户本人和同流程同事）。
> 质量标准：**95% 自动化 + 5% 手工微调 = 可交付**。

---

### 🔴 P0 — 必修课（不修则 PowerPoint 弹修复/无法打开）

#### Pitfall #1：负高度文本框

| 字段 | 内容 |
|------|------|
| **现象** | PowerPoint 打开文件弹"修复"提示；修复后样式异常/元素消失 |
| **版本** | v5→v7（最终 v7 修复） |
| **根因** | 动态高度公式 `CT_H - cy + CT_Y - offset` 在 cy 累积过大时 < 文本框内部下限 → `add_text(h=负值)` → 负 EMU shape |
| **触发条件** | 任何用 `max(剩余空间, 下限)` 计算高度的组件（roi_box、info_card、mod_card）；当上方内容多、剩余空间<下限时必触发 |
| **修复** | `add_text()` 入口全局防护 `h = max(h, 0.05)`；各组件内部高度也加 `max(..., 下限)` |
| **归属** | **qa-expert（严过关）L1 几何必查项**：扫描所有 shape，`h < 0` 或 `h < 10000 EMU` 直接 FAIL |
| **预防规则** | **① 所有高度计算出口必须 max(h, 正下限) ② qa 几何检查增加"负高度检测"为第一检查项 ③ 分段测试必须用真实数据量（简化数据会掩盖此 bug）** |

#### Pitfall #2：模板 Layout 选错（带背景图 vs 无背景图）

| 字段 | 内容 |
|------|------|
| **现象** | 用户说"没用我的模板"——生成的 PPT 有背景图或没有继承模板主题 |
| **版本** | v7→v8（最终 v8 修复） |
| **根因** | 用了 `slide_layouts[6]`（空白 layout，带背景图 bgPr+blipFill）而非目标页 P4 用的 `slide_layouts[1]`（标题和内容 layout，无 bg 元素） |
| **触发条件** | 模板有多個 layout；未确认目标页用的是哪个 layout 就随意选 |
| **修复** | 打开模板 PPT → 选中目标页 → `slide.slide_layout` 确认 index → 生成时用同一个 index |
| **归属** | **theme-expert（朱润色）P3 主题适配必查项**：加载模板后立即 dump 所有 layout 的名称/是否有背景图/占位符数量 |
| **预防规则** | **① Step 0 加载模板后输出 layout 清单给用户确认 ② 默认不用 layout[6](空白)，优先用带内容的 layout[1] ③ 若用户指定"用 P4 那页"，直接读 P4 的 slide_layout index** |

#### Pitfall #3：内容坐标超出模板可用区（压页眉/压页脚）

| 字段 | 内容 |
|------|------|
| **现象** | 内容整体偏下，底部被模板页脚截断；或顶部被 logo 遮挡 |
| **版本** | v8→v9（最终 v9 修复） |
| **根因** | 坐标按全画布（13.33×7.5"）计算，没避开模板的页眉（右上 logo y≈0.10~0.77"）和页脚（公司栏 y≈6.49~6.85"）。实际可用区仅 y∈[0.88, 6.40]，高 5.52" |
| **触发条件** | 模板基底路线 + 未测量可用区就直接用全画布坐标 |
| **修复** | 测量模板 layout 的已有元素位置 → 算出可用区 → CT_Y/CT_H 改为可用区参数 |
| **归属** | **layout-expert（范章成）核心职责**：可用区测量是布局的第一步输入 |
| **预防规则** | **① 模板路线必做可用区测量（见法则③）② cy 累加的终点必须 < 可用区.bottom - 余量 ③ roi_h 等动态高度的下限要随剩余空间自适应，不要硬编码大值** |

---

### 🟠 P1 — 高频翻车（不影响打开但排版质量差）

#### Pitfall #4：GAP 变量静默覆盖

| 字段 | 内容 |
|------|------|
| **现象** | 明明设了 GAP=0.06 紧凑间距，渲染出来却稀松 |
| **版本** | v9→v10（最终 v10 修复） |
| **根因** | 第45行 `GAP=0.06` 被第55行 `GAP=0.22` 静默覆盖；Python 无常量保护机制 |
| **触发条件** | 任何有"多处引用同一参数"的代码；多人/多轮编辑时极易出现 |
| **修复** | 删除重复赋值；只保留一个定义点；IDE 搜索确认无其他赋值 |
| **归属** | **layout-expert（范章成）**：间距是布局的核心参数 |
| **预防规则** | 见**法则 ④ 单一间距源**。扩展：**所有全局布局参数（GAP/PAD/MARGIN/DENSITY）都只定义一次，用 UPPER_CASE 标记为常量** |

#### Pitfall #5：横排元素被写成了竖排（break 滥用）

| 字段 | 内容 |
|------|------|
| **现象** | HTML 中一行内的小标签/关键词，在 PPTX 中变成每 tag 一行的竖列表 |
| **版本** | v9→v10（最终 v10 修复） |
| **根因** | `timeline()` 的 tags 循环里用了 `break: True` 分隔每个 tag；应该用空格拼接成单段文本 |
| **触发条件** | 任何把"数组→文本"的逻辑；开发者习惯性用 break 分隔数组元素 |
| **修复** | tags 用空格（或多空格）拼接成一个 run；或保留 break 但字号缩到 7pt 以下 + line_spacing=1.0 |
| **归属** | **data-expert（苏通达）+ layout-expert（范章成）**：数据模型的 direction 字段 + 渲染的方向实现 |
| **预防规则** | 见**法则 ① 方向声明**。扩展：**① 数据模型标注 direction=row ② 渲染时 direction=row 禁止用 break 分隔 ③ 多个短文本同行时用空格拼接为一个 seg** |

#### Pitfall #6：ROI / 键值对卡片 —— 一行两字段变成一行一字段

| 字段 | 内容 |
|------|------|
| **现象** | HTML 中 `标签          值` 左右排列在一行，PPTX 中标签占一行、值占下一行，4条数据撑出12+行 |
| **版本** | v11→v12（最终 v12 修复，用户一针见血指出） |
| **根因 | roi_box() 的 segs 拼装三重罪：(a)item间双换行（两个 break:True）(b)label 和 value 之间有隐式换行（value 后 break:True）(c) line_spacing=1.3 太松 |
| **触发条件** | 任何键值对/明细列表类组件；开发者把 label 和 value 当作独立段落处理 |
| **修复** | label 和 value 合并为**同一行的两个 run**（中间用空格分隔）；item间只保留单换行；line_spacing 降到 1.15 |
| **归属** | **layout-expert（范章成）**：键值对的行内布局是基础能力 |
| **预防规则** | **① 键值对数据默认渲染为"label + 空格 + value"同行 ② 只有超长 value（>可用宽度60%）才折到下行 ③ item 间单换行足够，禁止双换行 ④ line_spacing 键值对区域用 1.1~1.15** |

#### Pitfall #7：区块自身高度未参照源（HTML/PNG）校准

| 字段 | 内容 |
|------|------|
| **现象** | 每个 highlight/KPI/timeline/mod_card 都比 HTML 版高 10~20%，累积后严重溢出 |
| **版本** | v10→v11（最终 v11 全面压缩） |
| **根因** | 高度参数"拍脑袋"给值（highlight=0.50, kpi=0.70, timeline=0.85），没有对照 HTML 实际像素尺寸 |
| **触发条件** | 任何不参照源尺寸就设定组件高度的渲染逻辑 |
| **修复** | 对照 HTML 截图逐块测量实际高度；统一压缩 15~20%；字体/行距/padding 同步收紧 |
| **归属** | **layout-expert（范章成）+ visual-review-expert（沈定稿）**：布局尺寸 + 视觉验收 |
| **预防规则** | **① 组件高度必须有参照物（HTML截图/设计稿）② 无参照时用测高算法动态计算而非硬编码 ③ cy 累加的增量 ≈ 组件实高 + 微余量(0.02~0.04)，不要多加 0.05+ 的水份** |

#### Pitfall #8：mod_card / info_card 描述文本换行爆炸

| 字段 | 内容 |
|------|------|
| **现象** | 同一段中文描述，HTML 占 2 行但 PPTX 占 4~5 行；单个卡片高度膨胀 30%+ |
| **版本** | v10→v11（最终 v11 三管齐下修复） |
| **根因** | 三因素叠加：(a) CJK 字宽系数 0.98 偏小（测出来"放得下"→实际 wrap 更多）(b) 字体 9pt 偏大 (c) line_spacing 1.25 太松 |
| **触发条件** | 任何含中文长文本的卡片组件；中文字体不同环境下渲染宽度差异大 |
| **修复** | CJK 系数 0.98→1.05（宁高估）；desc 字体 9→8；line_spacing 1.25→1.12 |
| **归属** | **layout-expert（范章成）**：文本测高是布局的核心算法 |
| **预防规则** | 见**法则 ② 测宽校准**。扩展：**① CJK 系数 ≥1.0（保守估计）② 中文卡片 desc 字体 ≤8.5pt ③ line_spacing 中文区域 ≤1.15 ④ 同等宽度下 PPTX 换行数通常比 HTML/CSS 多 20~30%，预留余量** |

---

### 📊 经验汇总矩阵（快速查阅）

| # | 严重度 | 类型 | 一句话 | 修于 | 归属专家 |
|---|--------|------|--------|------|----------|
| 1 | 🔴P0 | 几何 | 负高度→PowerPoint弹修复 | v7 | qa-expert |
| 2 | 🔴P0 | 模板 | layout选错→背景图/无主题 | v8 | theme-expert |
| 3 | 🔴P0 | 可用区 | 坐标按全画布算→压页脚 | v9 | layout-expert |
| 4 | 🟠P1 | 参数 | GAP被覆盖→间距膨胀 | v10 | layout-expert |
| 5 | 🟠P1 | 方向 | break滥用→横排变竖排 | v10 | data+layout |
| 6 | 🟠P1 | 布局 | 键值对分行→ROI撑爆 | v12 | layout-expert |
| 7 | 🟠P1 | 尺寸 | 高度拍脑袋→全面偏大 | v11 | layout+visual |
| 8 | 🟠P1 | 文本 | CJK系数偏差→换行爆炸 | v11 | layout-expert |

### 🎯 质量承诺与 95% 原则

> 用户明确的质量预期：**95% 自动化可交付 + 5% 手工微调 = 成功**。
> 上述 8 条 pitfall 全部纳入专家团 SOP 后，P0 类问题（弹修复/打不开）应降到 **0**；
> P1 类问题（排版瑕疵）应控制在 **5% 以内**（如 v12 的顶部轻微重叠）。

**自动化覆盖范围（目标 95%）**：
- ✅ 不弹修复（Pitfall #1 全局防护）
- ✅ 模板正确套用（Pitfall #2 layout 确认流程）
- ✅ 内容在画面内（Pitfall #3 可用区测量）
- ✅ 横排不竖排（Pitfall #5 direction 声明）
- ✅ 键值对同行（Pitfall #6 默认同行布局）
- ✅ 高度有参照（Pitfall #7 测高算法）
- ✅ 换行可控（Pitfall #8 CJK 校准）

**已知局限（需手工调的 5%）**：
- ⚠️ 极端内容密度下可能存在 0.02~0.05" 的微小重叠（如 v12 顶部标题/highlight 区）
- ⚠️ 特殊字符（emoji/BMP dingbat）在某些 PowerPoint 版本显示异常
- ⚠️ 模板母版的复杂组合形状（如非标准页眉）可能需要微调 CT_Y

## 产品命名体系 (上传 WB 用, 2026-07-22 定稿)

为把"个人孵化 → 多场景覆盖 → 产品/专家化"这条路径固化, 命名分三层, 彼此解耦:

| 层级 | 名称 (id) | 显示名 | 角色 |
|------|-----------|--------|------|
| **SKILL** (引擎) | `pptx-craft` | PPT匠·可编辑生成引擎 | 数据模型→可编辑PPT + 文本优先多遍 + QA + 模板克隆 |
| **EXPERT TEAM** (专家团) | `ppt-studio` | PPT工作室 | 编排多个子专家, 拆解需求并派活 |
| 子专家 (团队内角色) | 见下 | 版式专家 / 数据专家 / QA专家 / 主题专家 | 各管布局 / 适配 / 校验 / 美化 |

- **技能 `pptx-craft` 是地基**: 不挑使用者, 只吃结构化数据 (人格无关)。
- **专家团 `ppt-studio` 是人格封装**: 同一引擎, 不同上车点 ——
  - `技术流专家` (吃 HTML / 数据模型, 适合你本人)
  - `零代码专家` (吃画布 / 表单, 适合非技术同事)
- **子专家 = 把"文本优先多遍"的每一遍拆成独立角色**, 由 `ppt-studio` 编排专家串起来:
  - 版式专家 (布局/flex/气口) · 数据专家 (源适配器: HTML/画布/表单→数据模型) ·
    QA专家 (校验/迭代) · 主题专家 (美化/模板主题 token)。

> 命名原则: 名称落到"能力本质"(数据驱动 / 可编辑 / 工艺感), 而非"输入介质"(HTML);
> 因此**强烈建议不要回退到 html2ppt 这类介质名**, 以免重新埋下"引擎解析 HTML"的预期坑。

---

## 引擎 API 参考 (#5)

### A. 纯原语引擎 `pptx_flex_engine.py`

| 函数 / 类 | 签名 | 说明 |
|-----------|------|------|
| `configure` | `configure(vw=1440, vh=680, slide_w_cm=33.867, slide_h_cm=19.05, density=1.20, tokens=None)` | 设虚拟画布与目标幻灯片尺寸；`density` 整体缩放间距。 |
| `Box` | `Box(x, y, w, h)` | 矩形区域（虚拟 px 坐标）。 |
| `hbox` / `vbox` | `hbox(deck, box, items, gap=16, pad=0)` / `vbox(...)` | 仅用于"区域框"层级 flex 布局；`items=[{"flex":n,"size":px,"group":g,"build":fn}]`。 |
| `Deck` | `Deck()` | 渲染记录器。方法：`.rect(b,fill,line=None,radius=0,group)`、`.ellipse(b,fill,group)`、`.text(b,content,fs,color,bold=False,align,group)`、`.render(slide)`；属性 `.recs`（校验用 VRec 列表）。 |
| `validate` | `validate(recs)` → `(errors, warnings)` | L1 几何校验：越界 / 跨组重叠 / 拥挤(<`MIN_BREATH`=10px)。**errors 非空即不可交付**。 |
| `layout_texts` | `layout_texts(deck, items, box, pad, breath, align="left", group="g", ts=None)` → `(leftover, scale)` | 文本优先多遍：上下左右 `pad` + 行间 `breath` 气口；溢出则二分缩字号（保 `min_fs`，不删内容）；返回文字下方剩余空间 `leftover`（供装饰填空）。`items=[{"content","fs","min_fs","color","bold"}]`。 |
| `KpiCard` | `KpiCard(deck, box, group, kpi)` | KPI 卡。`kpi={"label","value","sub",可选"color"}`。 |
| `CompareCard` | `CompareCard(deck, box, group, cmp)` | 对比卡。`cmp={"label","value","sub"}`。 |
| `emit_svg` | `emit_svg(deck, path)` | 出 SVG 预览（虚拟坐标 1:1）。 |
| `render_deck_png` | `render_deck_png(deck, path, scale_px=1.4, font_path=None)` | 出 PNG 预览（CJK 字体路径）。 |
| `add_slide_from_deck` | `add_slide_from_deck(prs, deck, bg=None)` | 把 deck 落成一页可编辑 slide。 |
| `new_presentation` | `new_presentation(slide_w_cm=None, slide_h_cm=None)` | 新建 `python-pptx` Presentation。 |
| 辅助 | `X/Y/W_/H_`(虚拟px→EMU)、`FS(px)`(px→pt)、`rgb(hex)`、`sp(k)`(间距令牌)、`TOK()`(设计令牌)、`PAD_CARD()`/`PAD_CARD_LG()` | 坐标/字号/颜色/间距换算。 |

**最小调用顺序**：`configure()` → `prs=new_presentation()` → `deck=Deck()` → 画 `rect/text/KpiCard` → `validate(deck.recs)`（0 errors）→ `add_slide_from_deck(prs, deck)` → `prs.save()`。参考 `scripts/examples/skeleton_data.py`。

### B. 通用 HTML→PPT 解析器 `scripts/html2ppt.py`

**CLI**：
```bash
python scripts/html2ppt.py <input.html> --out out.pptx --preview-dir previews --qa qa.json
```
- 退出码：`0` = QA PASS（0 几何错误）；`2` = **QA FAIL**（几何错误>0，硬闸门，不可交付）。
- 输出：可编辑 `.pptx` + 每页 `slide_NN.svg` / `slide_NN.png` 预览 + `qa.json` 报告（每页填充率、空白风险、几何错误、schema 告警）。

**关键函数**：
| 函数 | 说明 |
|------|------|
| `convert(html, out, preview_dir, qa)` | 主入口：解析→逐页渲染→校验→预览→报告。 |
| `parse_pages(soup)` | 章节切分（T1：`<section>`/带标题顶级 div → 一页）。 |
| `extract_header(el)` | 提取页眉（kicker + title + sub，通用检测）。 |
| `extract_blocks(el)` | 提取正文块（跳过标题，下钻包裹容器）。 |
| `classify_block(el)` | 块分类（容器优先于单卡），返回 `kind`。 |
| `check_blocks_schema(ptype, header, blocks)` | **#3 schema 强校验**：缺标题/空卡/空时间线/空栅格 → 返回告警列表，并入 QA。 |
| `qa_gate(qa)` | **#1 几何闸门**：`(passed, msg)`；errors>0 → `passed=False`。 |

**逐页目检规则（L2 呈现校验 · 不可抽样）**：每页必须出 SVG+PNG 预览并由人眼逐页确认（尤其时间线/栅格/低填充页）；填充率 <55% 标空白风险（hero 与纯文本陈述页豁免）。自动化只兜底几何，视觉丰满度靠人眼。

### C. 最小骨架（#6）

- HTML 起点：`scripts/examples/skeleton.html`（含 hero/contain/card/grid/timeline/文本 五类版式，带契约 class 注释）。
- 数据模型起点：`scripts/examples/skeleton_data.py`（不写 HTML，直接引擎生成一页）。
- 惯例：**任何新 PPT 先从骨架起步**，而非从零设计；结构对、再换内容。

### D. 视觉增强原语（#9）· 编排效率（#7）· 画布轴桥接（#10）

#### #9 视觉增强组件库
`Deck.rect` 在原语层新增两个可选参数（仅视觉、不进几何校验、不影响 0 重叠承诺）：
- `gradient=(color1, color2)`：竖向双色渐变填充（PPTX 原生 gradient / SVG `linearGradient` / PNG 逐行插值）。
- `shadow=True`：柔和外阴影（PPTX `shadow` / SVG `feDropShadow` / PNG 偏移近似）。

装饰辅助函数（纯装饰，登记为独立 group，被 `validate` 的 contains 规则跳过，不触发重叠/拥挤）：
- `eng.accent_bar(deck, box, color, thickness=6, vertical=True, group="accent")`：卡片左/顶强调条。
- `eng.divider(deck, x, y, w, color, thickness=2, group="div")`：分隔细线。

`html2ppt.py` 已默认挂接：① 卡片 = 柔和阴影 + 左侧蓝色强调条（warn 内容转琥珀色）；② 页眉底部金色分隔线；③ `hero` 页整幅渐变面板（`#EEF2FF→#F4F5F8`）拉高封面丰满度与填充率。

#### #7 编排效率
- 字体缓存：引擎 `_FONT_CACHE`（按 `size/font_path/index` 复用 `ImageFont`）。
- 并行预览：`convert()` 先顺序构建全部 deck（保证页码稳定），再用 `concurrent.futures.ProcessPoolExecutor` 把每页的 SVG+PNG 渲染 + L1 校验并行化；**任意异常（含子进程崩溃）自动回退顺序渲染**，保证健壮性。CLI 支持 `--workers N`（默认按 CPU 核数，上限 8）。
- PPTX 装配仍顺序（单 `Presentation` 对象不可并行）。

#### #10 画布轴桥接（Ardot 画布 → PPT）
`scripts/ardot2ppt.py` 把 Ardot 设计画布导出的节点树（与 `ardot-design-core` 节点 schema 对齐）直接映射为引擎原语，复用同一套 L1 校验 + QA 闸门。映射规则（零专属结构、纯几何/属性驱动）：

| Ardot 节点 | 引擎原语 |
|---|---|
| `RECTANGLE` / `FRAME`(有 fill) | `deck.rect`（实色/渐变 fill、cornerRadius、strokes 描边） |
| `FRAME`(无 fill) / `GROUP` / `SECTION` | 仅容器，递归子节点（子节点用绝对坐标） |
| `ELLIPSE` | `deck.ellipse` |
| `TEXT` | `deck.text`（characters / fontSize / fontWeight≥600→bold / textAlignHorizontal / 颜色） |
| `LINE` | 细分隔条 `divider` |

坐标：每页按 `PAGE.width/height` 等比 letterbox 居中映射到虚拟画布 `1440×680`。

**用法**：
```bash
python scripts/ardot2ppt.py <canvas.json> --out out.pptx --preview-dir previews --qa qa.json
```
样例：`scripts/examples/sample_canvas.json`（1 页：蓝色 hero 带 + 两张卡片 FRAME + 分隔线，已验证 0 几何错误）。画布轴与 HTML 轴并列为一等输入——同一引擎、同一 QA。

