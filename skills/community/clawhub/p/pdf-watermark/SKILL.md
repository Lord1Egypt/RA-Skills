---
name: pdf-watermark
description: "PDF文字水印工具 / PDF text watermark tool. 智能检测页面方向，自动调整角度和大小，支持中文，居中显示。Auto-detects page orientation, adjusts angle & size, supports Chinese, centered."
---

# PDF 水印添加工具

为 PDF 文档添加文字水印，支持智能适配和中文内容。

## 使用流程

### 1. 获取必要信息

**必须确认的信息：**
- 📄 PDF 文件路径（本地路径或 URL）
- 📝 **水印文字内容** - **如果用户未提供，必须主动询问：** "请告诉我水印文字内容（如'内部资料'、'机密'、姓名日期等）："

**可选参数（用户未指定时使用默认值）：**
- 透明度：默认 0.25（25%，不影响阅读）
- 角度：默认自动计算（竖版约30°，横版约25°）
- 字体大小：默认自动根据页面尺寸计算

### 2. 执行水印添加

使用脚本 `scripts/add_pdf_watermark.py`：

```bash
# 全自动模式（推荐）
python3 scripts/add_pdf_watermark.py <输入PDF路径> "<水印文字>" [输出PDF路径]

# 自定义参数
python3 scripts/add_pdf_watermark.py <输入PDF> "<水印文字>" <输出PDF> <角度> <透明度> <字体大小>
```

**参数说明：**
- `<输入PDF路径>`: 源文件路径或 URL
- `"<水印文字>"`: 要显示的水印文字（必须提供）
- `<输出PDF路径>`: 可选，默认为 `原文件名_watermarked.pdf`
- `<角度>`: 可选，默认 "auto" 自动计算
- `<透明度>`: 可选，0.0-1.0，默认 0.25
- `<字体大小>`: 可选，默认 "auto" 自动计算

### 3. 智能特性

脚本会自动：
- 🔍 **检测页面方向**：竖版/横版/方版
- 📐 **智能计算角度**：竖版约30°，横版约25°，方版约35°
- 📏 **自动调整字体**：根据页面尺寸计算最佳字体大小（28-60px范围）
- 🎯 **页面居中**：水印始终位于页面几何中心
- 📝 **中文支持**：自动加载系统可用的中文字体（黑体/宋体/苹方等）

### 4. 处理远程文件

如果用户提供的是 URL，先下载文件：

```bash
curl -L "<PDF_URL>" -o /tmp/temp_input.pdf
python3 scripts/add_pdf_watermark.py /tmp/temp_input.pdf "<水印文字>" /tmp/output_watermarked.pdf
```

### 5. 发送结果

处理完成后，将带水印的 PDF 文件发送给用户。

## 示例

**场景1：用户提供了所有信息**
```
用户：给这个文件加水印 "内部资料-张三 2024/01/15"，文件是 report.pdf
执行：python3 scripts/add_pdf_watermark.py report.pdf "内部资料-张三 2024/01/15" report_watermarked.pdf
```

**场景2：用户未提供水印内容**
```
用户：帮我给这个PDF加水印
回复：请告诉我水印文字内容（如"内部资料"、"机密"、姓名日期等）：
用户回复后：再执行加水印操作
```

**场景3：从URL下载**
```
用户：给 http://example.com/doc.pdf 加水印 "机密文件"
执行：
  curl -L "http://example.com/doc.pdf" -o /tmp/doc.pdf
  python3 scripts/add_pdf_watermark.py /tmp/doc.pdf "机密文件" /tmp/doc_watermarked.pdf
```

## 注意事项

- 水印使用灰色半透明，确保不影响原文阅读
- 中文自动检测系统字体，优先使用黑体(STHeiti)
- 每页独立计算，混合方向页面也能正确处理
- 输出文件默认保存在工作目录
