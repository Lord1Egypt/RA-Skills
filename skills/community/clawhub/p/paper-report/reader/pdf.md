# PDF 模式处理流程

本文档描述从本地 PDF 文件或下载的 arXiv PDF 提取内容的完整流程。
完成 P1–P5 后，返回 [SKILL.md](../SKILL.md) 执行 **Step 2**（生成报告）和 **Step 3**（校验）。

## 依赖

```bash
{PYTHON} -m pip install PyMuPDF --quiet
```

## 进度清单

```
Task Progress (PDF Mode):
- [ ] Step P1: 获取 PDF 文件
- [ ] Step P2: PDF 转图片
- [ ] Step P3: 逐页阅读理解 & 规划截图
- [ ] Step P4: 裁剪关键图表
- [ ] Step P5: 校验截图质量
- [ ] 返回 SKILL.md Step 2: 生成报告
- [ ] 返回 SKILL.md Step 3: 校验文件
```

---

### Step P1: 获取 PDF 文件

**用户提供本地文件路径？** → 直接使用该路径，跳过下载。

**来自 arXiv（HTML 不可用，回退到 PDF 模式）？** → 用 curl 下载：

```bash
# arXiv ID 如 2605.12036
curl -L -o {workspace}/paper.pdf "https://arxiv.org/pdf/{ARXIV_ID}"
```

验证下载成功：

```bash
file {workspace}/paper.pdf
```

输出应包含 `PDF document`。如需确认页数，可用 PyMuPDF：

```python
import fitz
doc = fitz.open('{workspace}/paper.pdf')
print(f"Pages: {doc.page_count}")
doc.close()
```

---

### Step P2: PDF 转图片

使用 `scripts/pdf_to_images.py` 将每一页渲染为 PNG 图片：

```bash
{PYTHON} scripts/pdf_to_images.py {workspace}/paper.pdf {workspace}/pages
```

脚本以 2x 分辨率渲染，输出到 `{workspace}/pages/page_1.png`, `page_2.png`, ...

此步骤的目的是让模型以图片形式"看到"每一页的完整布局，包括公式、图表和排版。

---

### Step P3: 逐页阅读理解 & 规划截图

使用 Read 工具逐页查看 `{workspace}/pages/page_N.png` 图片。

每页阅读时，**同时完成两个任务**：

**任务 A — 内容理解**：
- 提取该页的核心论点、方法描述、实验结果等关键信息
- 用中文记录摘要，为最终报告准备素材

**任务 B — 图表定位**：
- 识别页面中的所有 Figure、Table
- 目测其在图片中的像素范围，换算为 PDF 裁剪坐标

**坐标换算方法**：

页面图片以 2x 渲染，因此：

```
PDF 坐标 = 图片像素坐标 ÷ 2
```

典型 A4 页面：图片约 1190 × 1684 px，对应 PDF 约 595 × 842 pt。

目测图表在图片中的上下左右像素边界，除以 2 后得到 `(x0, y0, x1, y1)`。

**双栏论文注意**：
- 跨双栏的满宽图表：x 范围约 `30 ~ 565`
- 仅占左栏的图表：x 范围约 `30 ~ 295`
- 仅占右栏的图表：x 范围约 `300 ~ 565`

不确定时宁可稍宽（后续 P5 校验可缩窄），留约 10pt 的上下 margin。

**图表选取原则**：见 [SKILL.md](../SKILL.md) Step 2「图表选取原则」。

**输出**：整理出截图计划列表，例如：

```
截图计划：
1. Figure 2 - 系统架构图（满宽） → page 3, Rect(30, 55, 565, 258)
2. Figure 3 - DiT 维度对比（左栏）→ page 6, Rect(30, 252, 295, 388)
3. Figure 5 - 主观评价（左栏）  → page 9, Rect(30, 55, 295, 180)
```

> **注意**：PDF 模式通过图片视觉推理理解内容，存在一定的误读风险，特别是在具体数字和表格数值方面。撰写报告时，对关键数据务必谨慎，有疑问时在报告中注明"根据图表目视"而非断言具体数值。

---

### Step P4: 裁剪关键图表

根据 Step P3 的截图计划，使用 `scripts/crop_figures.py` 批量裁剪：

```bash
{PYTHON} scripts/crop_figures.py \
  {workspace}/paper.pdf \
  {workspace}/figures \
  '{crop_spec_json}'
```

其中 `{crop_spec_json}` 是 JSON 格式的裁剪规格：

```json
[
  {"page": 3, "rect": [30, 38, 565, 290], "name": "fig1_architecture"},
  {"page": 3, "rect": [30, 295, 565, 485], "name": "fig2_results"},
  {"page": 5, "rect": [30, 50, 565, 200], "name": "table1_metrics"}
]
```

脚本以 3x 分辨率裁剪，输出到 `{workspace}/figures/` 目录。

---

### Step P5: 校验截图质量

使用 Read 工具逐一查看 `{workspace}/figures/` 中的每张截图：

- 图表内容是否完整，没有被截断？
- 是否包含了图表标题和标注？
- 是否有多余的文字区域混入？

**如果某张截图有问题**：调整对应的 Rect 坐标（扩大或缩小范围），然后重新裁剪该图。

**快速调整技巧**：
- 截断了底部 → 增大 y1（向下扩展）
- 截断了顶部 → 减小 y0（向上扩展）
- 混入了上方文字 → 增大 y0
- 混入了下方文字 → 减小 y1
- 一般留 5-10pt margin 即可

反复调整直到所有截图质量合格。

---

完成以上 P1–P5 后，返回 [SKILL.md](../SKILL.md) 执行 **Step 2** 生成报告。
