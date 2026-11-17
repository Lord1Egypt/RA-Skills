# mu-pdf-converter 使用详细指南

## 各格式详细说明

### 📊 PDF → PPT（核心功能）

```bash
python pdf_to_pptx.py input.pdf \
  [--outfile output.pptx] \
  [--slide-size 16:9|4:3|A4]
```

**幻灯片尺寸预设：**
- `16:9` 宽屏（默认，25.4×14.3cm）
- `4:3` 标准（25.4×19.1cm）  
- `A4` A4横向（27.5×21.6cm）

**分层转换策略（四层由底到顶叠加）：**

```
Layer 4（顶）: 文本框  ── 可编辑，保留字体/颜色/加粗/斜体
Layer 3:       表格    ── 原生 Table 对象，可编辑
Layer 2:       SVG     ── 整页矢量图，Office 2019+ 可编辑路径
Layer 1（底）: 位图    ── 原始 PNG/JPEG，无损质量
```

### 📝 PDF → Word

```bash
python pdf_to_docx.py input.pdf [--outfile output.docx]
```

- 文本块按阅读顺序重建为段落
- 字号比正文大 2pt 以上 → 自动识别为 Heading 1
- 保留加粗、斜体、字体颜色
- 表格用原生 Table 对象插入，首行加粗
- 多页 PDF → 每页之间插入分页符

### 📋 PDF → Excel（仅表格）

```bash
python pdf_to_xlsx.py input.pdf \
  [--pages all|1-3] \
  [--outfile output.xlsx]
```

- 扫描所有（或指定）页面的表格
- 每个表格 → 独立 Sheet（命名：`Page1_Table1` 等）
- 首行加粗 + 淡蓝色背景
- 列宽根据内容自适应（中文字符按 2 倍宽度计算）
- 未发现表格时给出友好提示和建议

### 🖼 PDF → 图片

```bash
python pdf_to_images.py input.pdf \
  [--dpi 150] \
  [--format png|jpg] \
  [--pages 1-3] \
  [--outdir ./output]
```

- 使用 PyMuPDF 矩阵缩放渲染（`scale = dpi / 72`）
- 默认 150 DPI（适合屏幕）；打印建议 300 DPI
- 输出文件名：`{stem}_page_001.png`
- JPEG 输出质量：90（可在代码中调整）

---

## PPT 转换技术细节

### 坐标系转换

```
PDF 坐标 (pt, 原点左上角)
  ↓ × PT_TO_EMU (12700)
EMU 绝对坐标
  ↓ × (slide_width / pdf_width_emu)
Slide EMU 坐标
```

### 文本块字体属性提取

通过 `fitz` span flags 位掩码解析：
- bit 0: 斜体（italic）
- bit 4: 加粗（bold）
- `span.color`：整数颜色值 → RGBColor(r, g, b)

### 表格识别逻辑

1. `pdfplumber.find_tables()` → 获取表格 bbox 列表
2. 文本块与表格 bbox 重叠率 > 30% → 判定为表格内文本，跳过文本框插入
3. `extract_tables()` → 获取单元格数据 → 插入 `slide.shapes.add_table()`

### SVG 矢量图插入

python-pptx 原生不支持 SVG，通过直接操作 OOXML 实现：
- `fitz_page.get_drawings()` 检测矢量路径存在
- `page.get_svg_image()` 导出整页 SVG
- 构造 `<p:pic>` + SVG 关系写入 slide XML
- Office 2019+ / Microsoft 365 / LibreOffice 7+ 支持编辑 SVG 路径

---

## 降级策略

| 场景 | 处理方式 |
|------|---------|
| 扫描件（无文本层） | 仅插入位图（Layer 1），跳过文本/表格/SVG |
| 表格无边框 | pdfplumber 可能漏检，相关文本仍作为文本框插入 |
| SVG 插入失败 | 跳过 Layer 2，不影响其他层 |
| 中文字体缺失 | `map_font_name()` 映射到 SimSun/SimHei/Microsoft YaHei |
| 图片 xref 损坏 | 跳过该图片，记录警告 |

---

## 已知限制

1. **多栏布局**：pptx 不支持分栏，多栏 PDF 可能导致文字重叠
2. **扫描件**：无文本层，只能保留图片外观，不可编辑
3. **渐变/透明度**：SVG 层可保留，但位图层无法还原复杂效果
4. **数字签名**：加密 PDF 需先解密（`qpdf --decrypt`）
5. **SVG 兼容性**：SVG 编辑需 Office 2019+；老版 Office 显示为图片但不可编辑
6. **表格合并单元格**：pdfplumber 不完全支持跨行/跨列合并识别
7. **文字方向**：竖排文字（CJK 竖向排版）可能错位
8. **图片水印（扫描件）**：扫描件中的图片水印需先通过 OCR 处理添加文本层，再用 pdf_remove_watermark.py 识别涂抹
9. **加密 PDF**：加密 PDF 需先解密（`qpdf --decrypt input.pdf decrypted.pdf`）再进行水印移除

---


### 📋 PDF 表单填写（pdf_fill_form.py）

依赖：`pypdf`, `pymupdf`（`pip install pypdf pymupdf`）

**路径A — 可填字段 PDF（fillable form）**

```bash
# 步骤1：检测字段，输出 JSON 结构
python3 pdf_fill_form.py form.pdf --detect

# 步骤2：准备 values.json，格式：
# {"姓名": "张三", "日期": "2024-03-15", "同意": true}

# 步骤3：填写并输出
python3 pdf_fill_form.py form.pdf --fill-json values.json --outfile filled.pdf
```

支持字段类型：`text`（文本）/ `checkbox`（复选框）/ `radio_group`（单选组）/ `select`（下拉）

**路径B — 非可填字段 PDF（non-fillable）**

```bash
# 步骤1：转图分析，每页输出 PNG，打印坐标参考
python3 pdf_fill_form.py form.pdf --analyze --outdir ./form_images --dpi 150

# 步骤2：根据图片坐标准备 annotations.json：
# [{"page": 1, "x": 150, "y": 200, "text": "张三", "font_size": 11}]

# 步骤3：注释填写
python3 pdf_fill_form.py form.pdf --annotate-json annotations.json --outfile filled.pdf
```

### 📊 Excel 批量模式（pdf_to_xlsx.py --batch）

```bash
# 扫描目录内所有 .pdf，提取全部表格写入同一 Excel
python3 pdf_to_xlsx.py --batch ./invoices/ --outfile batch_result.xlsx
```

- Sheet 命名：`{文件名}_P{页}_T{表}`（截断到 Excel 31 字符上限）
- 自动生成 `Summary` 汇总 Sheet，含：文件名、页码、表序号、行数、列数
- `--batch` 与单文件 `input` 互斥，不可同时指定

---

