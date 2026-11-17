---
name: 检验气泡标注
description: 机械图纸(矢量/扫描PDF或图片)检验气泡标注一体化工具：生成红色圆圈+编号的"检验气泡标注图"(PDF+PNG)，并产出单一合并检验表(5 sheet：检验记录表/标注图纸(气泡图)/未注公差基准/汇总/关键特性专项)。当用户要求"做气泡图/检验气泡图""标关键尺寸/形位公差""生成检验表/首件检验清单(FAI)/全尺寸检验报告/IQC-OQC检验表""尺寸与公差 Excel 报表"时使用。自动高分辨率渲染、多方向OCR精确定位、编号自动避让+吸附、一般公差(GB/T1804-f / GB/T1184-H)套用、覆盖性自检。关键词：检验气泡图 气泡标注 首件检验 FAI 全尺寸检验 品质QC 公差 GD&T OCR Excel报表 图纸标注 balloon drawing inspection。
tags:
  - 机械图纸
  - 检验气泡图
  - 气泡标注
  - 首件检验
  - 全尺寸检验
  - 品质QC
  - 公差
  - GD&T
  - OCR
  - Excel报表
  - 图纸标注
---

# 检验气泡标注（Inspection Balloon Annotation）

把机械图纸上的关键尺寸、公差、形位公差用**带编号的红色圆圈气泡**标注出来，并生成与气泡序号一一对应的**两份检验表**，作为品质/QC 首件检验(FAI)、全尺寸检验、IQC/OQC 的标准交付物。

本技能由「图纸气泡标准助手」(标注图方案) 与「检验气泡图」(QC 检验表方案) 合并而成：
- **标注图**：采用图纸气泡标准助手的 PyMuPDF 矢量叠加方案（红圈+引线+编号，程序化避让布局）。
- **检验表 A（18 列明细）**：图纸气泡标准助手规格。
- **检验表 B（3 表式检验记录）**：检验气泡图规格（检验记录表 + 内嵌气泡图 + 未注公差基准）。
- 两份表均从**同一份尺寸主数据 `dims_table.py` / `balloons.json`** 生成，不维护双数据模型。

## 0. 角色与铁律

资深产品工程师 + 质量工程师，精通 GB/T 14689、GB/T 1804、GB/T 1184、ISO 2768、ASME Y14.5 与主机厂特性体系。

1. **绝不猜测**：不确定标"待确认"，不擅自填值。
2. **显式优于隐式**：显式公差 > 一般公差；客户配置 > 视觉检测。
3. **气泡尺寸定义在输出纸张空间（mm）**，与图纸比例尺无关。
4. **可追溯**：每个尺寸记录视图、公称、公差来源、特性分类。
5. **保留人工复核**：AI 做初筛，工程师签字确认。
6. **统一形状**：所有气泡一律红色圆圈+数字，不用形状/线型/颜色区分内容（特性分类只写进检验表）。

## 1. 何时使用

- 用户给出零件图纸（PDF 或图片），要求"做气泡图/检验气泡图""标关键尺寸/形位公差""生成检验表/首件检验清单/全尺寸报告"。
- 需要一张气泡号与检验表行号对应的图纸，连同两份可下发检验员的 Excel。

## 2. 产出物（全部交付）

| 产出 | 文件 | 说明 |
|------|------|------|
| 标注图（矢量，可选） | `<图号>_气泡标注图_p1.pdf` | PyMuPDF 矢量叠加，原图不位图化；加 `--no-pdf` 可不输出 |
| 标注图（位图，默认） | `<图号>_气泡标注图_p1.png` | 300 DPI，用于目视复核与内嵌检验表 |
| 合并检验表 | `<图号>_检验记录表.xlsx` | 单一 xlsx，5 个 sheet：**检验记录表 / 标注图纸(气泡图) / 未注公差基准 / 汇总 / 关键特性专项**（原"尺寸明细检验表"的汇总与关键特性专项已并入；18 列"尺寸明细"sheet 不再单独输出，因检验记录表已逐条列出） |
| 自检报告 | `work/coverage_report.json` | 覆盖性 + 布局校验 + 待确认清单 + 交付前 10 项 |

> 交付时用 `present_files` 一并给出标注图(PDF/PNG) + 合并检验表，并说明：① 气泡号与检验记录表序号一一对应；② 未注公差基准来源；③ 坐标由 OCR 定位，正式使用前建议目视复核关键项。

## 3. 统一工作流

### 3.1 极速模式（推荐）：收到图纸一条命令全自动出齐
适用绝大多数图纸。脚本依次自动完成：渲染 → 多方向OCR → **自动抽取尺寸(初稿)** → 气泡标注图(PDF/PNG) → **合并检验表(单一 xlsx：检验记录表+气泡图+未注公差基准+汇总+关键特性专项，尺寸明细不输出)** → 覆盖性自检 + 交付前10项。无需手工逐步操作。

```bash
python scripts/auto_run.py --pdf <图纸.pdf> --base <输出根目录> [--name 输出主名] [--dims 已有dims_table.py] [--cp 控制计划编号] [--force-render] [--force-ocr] [--render-dpi 300] [--no-pdf] [--no-png]
# 例（默认：300dpi+白边裁切+同时出 PDF 与 PNG）：
python scripts/auto_run.py --pdf "腔体 A3.pdf" --base ./out
```

- `--base` 下自动建 `work/`（中间产物：render.png / labels.json / dims_table.py / balloons.json / coverage_report.json）与 `outputs/`（标注图 PNG + 两份检验表 + 自检报告）。
- **效率要点（重要）**：流水线最慢的是 OCR 步骤——`ocr_labels.py` 对 0°/90°/270° **三个方向各跑一遍** rapidocr 再合并（竖排尺寸需在 90°/270° 才能识别），所以 OCR 实际是 3 遍。两项固定优化已内置（不丢精度）：
  - **白边裁切（默认开启）**：`ocr_labels.py` 自动裁掉图纸外围空白边再 OCR，**分辨率不变、文字一个不少**，像素量通常减半 → OCR 约快 2 倍；加 `--no-crop` 可关闭。
  - `--render-dpi`（默认 **300**）：底图仅用于障碍检测/OCR 输入；**标注图本身仍以 300 DPI 矢量出图**，清晰度不受影响。配合白边裁切已足够；调高到 400 可提升极小字识别率但更慢，调低到 200 更快但可能漏标小尺寸（实测 F810 在 200 漏标 6/22 个尺寸，故不建议低于 300）。
  - `--no-pdf`：**跳过输出 PDF、只出 PNG**（省去 PDF deflate 约 3–4s；PNG 已够目视复核与内嵌表 B）。
  - `--no-png`：**跳过输出 PNG、只出 PDF**（省去 300dpi 栅格化约 4s）。**注意**：表 B 的"内嵌气泡图"需要位图，PNG 缺失时 `build_inspection_xlsx` 会自动跳过嵌入（不崩溃），即表 B 将没有内嵌气泡图——这是取舍，不是 bug。
  - **PDF 并不比 PNG 更快**：实测 build 步骤中 PDF deflate ≈ 3.7s、PNG 栅格化 ≈ 4.1s，几乎一样；而真正的大头是 OCR（三方向 rapidocr，约 25s，与出图格式无关）。所以"换成 PDF 出图"本身并不能显著提速；只有在"连表 B 内嵌图也去掉"时才能省下那 ~4s 栅格化（代价：表 B 无内嵌图）。需要矢量 PDF 用于打印/归档时再用 `--no-png`。
  - 各步耗时与"最慢步骤"会在运行结束自动打印，便于继续优化。
- **自动抽取为 AI 初筛**：`work/dims_table.py` 中 CC/SC/NC 均带【初判X,待复核】；自动抽取可能含少量非尺寸文本或漏掉个别尺寸，**正式下发前须工程师复核**（依据 `coverage_report.json` 的待确认清单 + 目视）。
- 若已有精修好的尺寸主数据，加 `--dims 路径` 跳过自动抽取直接复用（即"精细模式"的数据）。
- 编号数字一律**正立居中于圆圈内**（已修复旋转页 /Rotate 导致数字倒立/出圈的缺陷）。

### 3.2 精细模式（逐步骤 / 人工精修尺寸主数据）
等价于极速模式内部流程，用于自动抽取不理想、需逐个核对尺寸时：

```bash
# 0) 渲染（400 DPI；自动应用页面旋转，后续坐标均以该 PNG 为准）
python scripts/render_pdf.py  in.pdf  work/render.png  --dpi 400

# 1) 多方向 OCR 定位标注文字（0°/90°/270° 合并，竖排尺寸也能识别）
python scripts/ocr_labels.py  work/render.png  work/labels.json
#    查某段文字坐标，反复用直到每个尺寸都定位到：
python scripts/find_label.py   work/labels.json  "19"
python scripts/find_label.py   work/labels.json  "0\.1|0\.05"

# 2) 建立尺寸主数据（复制模板填写；ax,ay 取该标注文字框中心，来自 OCR 坐标）
#    cp scripts/dims_table_template.py work/dims_table.py  然后编辑
#    可选：work/drawing_meta.json 提供表 B 的零件/图号/材料/未注公差声明等信息

# 3) 生成标注图（输出 PDF/PNG + work/balloons.json）
python scripts/build_balloons.py --dims work/dims_table.py --pdf in.pdf \
       --png work/render.png --ocr work/labels.json --out outputs

# 4) 合并检验表（单一 xlsx：检验记录表+气泡图+未注公差基准+汇总+关键特性专项；尺寸明细不输出）
python scripts/gen_combined.py --balloons work/balloons.json \
       --png outputs/<图号>_气泡标注图_p1.png --meta work/drawing_meta.json \
       [--cp MEST/Q/CP-xxx] --out outputs/检验记录表.xlsx
#    如需单独一份 18 列"尺寸明细检验表"（含 汇总/尺寸明细/关键特性专项），可另跑：
python scripts/gen_excel.py --balloons work/balloons.json --out outputs/尺寸明细检验表.xlsx

# 6) 自检（覆盖性 + 布局 + 交付前 10 项）
python scripts/validate_layout.py --balloons work/balloons.json --ocr work/labels.json \
       --pdf in.pdf --png work/render.png --out work/coverage_report.json
python scripts/finalize_report.py --report work/coverage_report.json
```

- **坐标系唯一**：所有 `ax,ay` 坐标必须与 `work/render.png` 同坐标系，中途不换图/不改分辨率（见 `references/workflow.md` 常见坑 3）。
- **扫描位图无文字层**：直接走 OCR（第 1 步）；矢量 PDF 亦可先试 `page.get_text("rawdict")`，无则返回 0 段，仍回退 OCR。
- **中间产物落盘**：JSON 写文件，不在对话打印全文，只报统计摘要（尺寸数、特性分布、待确认数）。

## 4. 气泡样式（硬）

**统一规格：红色圆圈 + 数字。全部尺寸一律圆形，不用形状/线型/线宽区分任何内容。**

| 项 | 规格 |
|----|------|
| 形状 | 圆形（所有尺寸、所有特性分类统一） |
| 颜色 | 描边、数字、引线全部红色 |
| 外圈线宽 | 0.35mm（≈1.0pt） |
| 外圈直径 | 默认 6mm（≥5mm）；编号 ≥100 放大到 8mm（R 由 8.5pt→11.3pt） |
| 数字字号 | 默认 4mm（≥3.5mm = 9.9pt） |
| 数字 | 与两份检验表"气泡号/序号"逐条一致 |

- 特性分类**不在图纸表达**（不用五角星/三角/虚线）；分类只写入检验表列。
- 唯一允许变化是整体尺寸（直径/字号），禁止改变形状。

## 5. 引线与避让（硬）

- 气泡初始位置优先图纸空白区/视图外围，不是先压尺寸再避让。
- 气泡与尺寸文本至少留 2mm 间隙；空间不足移到空白区或走局部放大。
- 引线红色三角箭头，尖端距尺寸文本边界框 0.5mm、指向文本方向；严禁压盖数字。
- 引线严禁跨越任何尺寸数字文本；绕不开则把气泡移到另一侧。
- 标注图与检验表序号逐条一致，放大图沿用同一号。

## 6. 编号规则（硬）

- **纯数字、无前导零**（`1`、`2`、`10`；禁止 `01`、`1-01`），**不拼接页号**。
- 顺序：视图内从上到下、从左到右；`build_balloons.py` 按 `dims_table.py` 的 `VIEW_ORDER`（或出现顺序）自动编号。
- 形位框格独立成号（类型=形位）；尺寸与框格同串时拆号并用"关联气泡号"互链。
- 基准符号 A/B/C **不编号**，列入汇总/表 B 信息区。
- 交付前核对：气泡号集合 == 尺寸集合，无重号、跳号、错位。

## 7. 一般公差与特性分类

- **显式公差优先**：`ext` 非空 → 用图纸值；否则套一般公差。
- **一般公差**：线性/角度 GB/T 1804-2000 f 级（≤3→±0.05；≤6→±0.05；≤30→±0.1；≤120→±0.15；≤400→±0.2；>400→±0.3；角度短边≤10→±1°）。形位 GB/T 1184-1996 H 级。
- **圆角/倒角/半径**适配一般公差需公司标准确认 → "待确认"（见 `references/gbt_tolerances.md` 与 `references/tolerance-and-symbols.md`）。
- **特性分类**：`cls=CC` 关键 / `SC` 重要 / `NC` 一般。表 A 用 ◆/○(★)；表 B 用 A红/B黄/C绿。

## 8. 合并检验表（默认输出，单一 xlsx · 5 sheet）

`gen_combined.py` 产出单一 Excel 文件（默认 `<图号>_检验记录表.xlsx`），含 5 个 sheet，顺序固定：

1. **检验记录表**（由 `gen_qc_items.py` / `build_inspection_xlsx.py` 生成）：零件信息区 + 逐条检验项目（序号=气泡号 / 视图 / 检验项目 / 基本尺寸 / 上偏差 / 下偏差 / 公差带 / 量具 / 方法 / 重要度 / 实测值×3 / 判定）+ 结论签字行。
2. **标注图纸(气泡图)**：内嵌标注图 PNG（来自 `--png`；若用 `--no-png` 则自动跳过嵌入，不崩溃）。
3. **未注公差基准**：GB/T1804-2000 f 级 + GB/T1184-1996 H 级标准值表（来自 `references/gbt_tolerances.md`）；图纸显式公差列于表末优先项。
4. **汇总**（原表 A 汇总 sheet 并入）：图号 / 材料 / 特性分布 / 尺寸总数等统计。
5. **关键特性专项**（原表 A 关键特性专项 sheet 并入）：仅 CC/SC 项逐条列出，便于关键特性控制。

- 信息区内容来自 `work/drawing_meta.json`：`{"title","part","drawing_no","material","treatment","tolerance_note","inspection_type"}`，缺则占位待填。
- **原"尺寸明细检验表"的「汇总」与「关键特性专项」已并入本表**；18 列逐条「尺寸明细」sheet 不再单独输出（检验记录表已逐条列出，重复无意义且可提速）。

## 9. 18 列尺寸明细检验表（按需单独生成，可选）

若需一份含「汇总 / 尺寸明细（18 列逐条）/ 关键特性专项」三 sheet 的明细表（如工艺 / 研发归档），单独运行 `gen_excel.py`：

```bash
python scripts/gen_excel.py --balloons work/balloons.json --out outputs/尺寸明细检验表.xlsx
```

18 列：气泡号、图纸页码、分区、视图、公称尺寸、单位、类型、显式公差、一般公差声明、最终公差、公差来源、特性分类、特性符号、检验要求、关联气泡号、出现位置、控制计划编号、备注。出现位置 = 图纸原始标注文字（便于检验员对照）。

## 10. 覆盖性自检与交付前校验

`validate_layout.py` + `finalize_report.py` 产出 `coverage_report.json`，必过项：
1. 覆盖性：应标未标 = 0。
2. 气泡互不重叠（程序校验圆心距 ≥ 2R+1）。
3. 圆盘不碰文字 bbox（外扩 2mm）；引线不穿非自身文字。
4. 编号连续无缺号/重号、纯数字无前导零、未拼页号。
5. 显式公差优先、一般公差已套用；无遗留"待确认"或已列清单。
6. 气泡为红色圆圈+数字，未用形状区分；引线 2mm 间隙、不跨越文本。
交付前 10 项完整清单见 `coverage_report.json.predelivery_checklist`。

## 11. 工程实现要点（已验证，直接复用）

- **运行环境**：`~/.workbuddy/binaries/python/envs/default/Scripts/python.exe`（含 `pymupdf`/`Pillow`/`numpy`/`rapidocr_onnxruntime`/`openpyxl`）。
- **真实像素半径（关键修复）**：绘制 `R=8.5/11.3pt` 在 A4 页面（缩放比 sx≈0.18）真实像素半径约 **47/63px**；布局必须按 `Rpx(no)=R_pt/min(SX,SY)` 用像素半径，否则渲染图上气泡严重重叠。脚本已内置。
- **障碍掩膜**：OCR 文字框作硬障碍（自身框豁免引线穿越）；图像密度图（1pt 栅格化）作软惩罚 `cost = dist + 1200*geo_frac`。
- **自动布局**：72 角环形搜索（0/20/45/…/340px 距离档）+ 120 轮松弛推挤；硬约束=圆盘不碰文字、引线不穿文字（自身框豁免）、圆心距≥2R+1。
- **标注图矢量叠加**：直接在 `page` 上 `draw_circle`/`draw_line`/`draw_polyline`/`insert_text` 后 `doc.save()`，原图保持矢量。
- **一键流水线（效率核心）**：`scripts/auto_run.py` 串联 render→ocr→auto_extract→build_balloons→gen_combined→validate→finalize，**收到 PDF 一条命令出齐全部交付物**；`scripts/auto_extract_dims.py` 为通用自动尺寸抽取（初稿，待复核），替代过去逐图手搓 `gen_dims.py` 的低效环节。
- **编号数字正立居中（已修复）**：输出 PNG 与 render.png 同为页面原生坐标系（不应用 /Rotate），编号一律 `rotate=0` 水平/垂直居中于圆心，**绝不做旋转补偿**。旧版对旋转页(/Rotate=270/180)做反向旋转补偿，导致数字倒立且按角点锚定跑出圆圈——该缺陷已修复，现对任意页面旋转均正确。
- **Bash 工具本机不可用** → 一律用 Python 脚本或 PowerShell（PowerShell 的 stdout 有时不回显 → 结果写文件再 Read）。
- **标准查不到的项**（如 GB/T 14486 MT 系列）一律不填值，标"待查表"并在备注给备用口径。

## 12. 多页与批量处理

- **单图号多页**：同图号多页视为同一图集，**跨页连续编号**（第1页 1..n，第2页 n+1..）；页码单独记在检验表「图纸页码」列。每页独立渲染/OCR/建 `dims_table.py`，编号在 `build_balloons.py` 内按视图顺序自动连续。
- **多图号批量**：每个图号独立编号 + 独立标注图/检验表；用 `scripts/batch_run.py` 串起全链路（渲染→OCR→标注图→表A→表B→自检），并产出 `总汇总表.xlsx`（含图号、页数、气泡数、SC/NC、待确认、重叠、引线穿字、圆盘压字、覆盖性、各产出路径）。
- **旧气泡图**：图上已有编号 → 一律重新编号，并出「新旧编号对照表」（在表 A 汇总 Sheet 追加）。
- **放大图**：同一尺寸全图只有一个号，放大图沿用该号，不新增、不改号。
- **批量输入**：准备 `manifest.json`（每项 `{pdf, dims, meta?, name}`），运行：
  ```bash
  python scripts/batch_run.py --manifest manifest.json --out-base <输出根目录>
  ```
  `batch_run.py` 对每个图号在 `<out-base>/<name>/{work,outputs}/` 下产出全套文件，最后在 `<out-base>/` 汇总。

## 13. 参考文件（按需加载，勿整篇复述）

| 文件 | 何时读 | 内容 |
|------|--------|------|
| `references/tolerance-and-symbols.md` | 套公差、识别符号、判定特性分类 | 最终公差优先级、GB/T1804 线性+角度、GB/T1184、ISO2768、边界处理、GD&T 符号、主机厂符号对照、特性分类定义 |
| `references/io-and-flows.md` | 生成表格/标注图、多页、批量、复杂场景 | 分层步骤与 JSON schema、覆盖性自检、输出格式与首页模板、Excel 列规则与示例、批量与不规范图纸、完整校验清单 |
| `references/gbt_tolerances.md` | 套用未注公差、填表 B 基准值 | GB/T1804-2000 / GB/T1184-1996 数值表 |
| `references/workflow.md` | 用检验气泡图脚本、items.json 字段、常见坑 | 五命令流程、targets/items.json schema、OCR 多方向、坐标换算、交付约定 |
