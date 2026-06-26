---
name: pdf-studio
description: Professional PDF document generator. Use when user needs to create reports, invoices, certificates, portfolios, or any publication-ready PDF. Supports images, tables, charts, TOC, headers/footers, and cross-platform fonts. Generates print-quality PDFs. PDF文档生成、专业报告、发票制作。
version: 1.1.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📑", "requires": {"bins": ["python3"]}}}
---

# PDF Studio

Professional PDF document generator that creates publication-ready PDFs with perfect typography and layout.

## Features

- 📑 **Print Quality**: 300 DPI, CMYK support, bleed marks
- 🎨 **Professional Layout**: Multi-column, headers/footers, page numbers
- 🖼️ **Image Support**: Embedded images, captions, watermarks
- 📊 **Tables & Charts**: Formatted tables, bar charts, pie charts
- 📐 **Typography**: Professional fonts, kerning, ligatures
- 🌍 **Multi-Language**: Chinese, English, Japanese, etc.
- ✅ **Cross-Platform**: Windows, macOS, Linux
- 📱 **PDF/A Compliant**: Archival quality

## Trigger Conditions

- "生成PDF" / "Generate PDF"
- "帮我做一份报告" / "Create a report"
- "制作发票" / "Create an invoice"
- "生成证书" / "Generate certificate"
- "制作作品集" / "Create portfolio"
- "pdf-studio"

## Document Types

### Business (商务)
- 年度报告
- 商业计划书
- 发票/账单
- 合同/协议
- 产品手册

### Academic (学术)
- 论文排版
- 学位证书
- 研究报告
- 会议论文

### Government (政府)
- 公文
- 公告
- 证书
- 表格

### Personal (个人)
- 简历
- 作品集
- 证书
- 邀请函

---

## Step 1: Understand Requirements

```
请提供以下信息：

文档类型：（报告/发票/证书/简历/其他）
纸张大小：（A4/Letter/A3/自定义）
方向：（纵向/横向）
页边距：（默认/自定义）
字体要求：（默认/指定字体）
语言：（中文/英文）
特殊要求：（水印/页眉页脚/目录等）
```

---

## Step 2: Generate PDF

### Recommended Libraries

PDF generation requires Python libraries. Users should install manually before use:

- **FPDF2**: Simple PDF generation
- **WeasyPrint**: HTML/CSS to PDF
- **ReportLab**: Advanced PDF features

### Basic PDF Generation

1. Install a PDF library (e.g., FPDF2)
2. Create document with pages
3. Add content (text, images, tables)
4. Output PDF file

### HTML/CSS to PDF

1. Prepare HTML content
2. Apply CSS styles
3. Convert to PDF using library

---

## Typography Settings (字体设置)

### Cross-Platform Fonts

| Language | Serif | Sans | Mono |
|----------|-------|------|------|
| Chinese | Noto Serif SC | Noto Sans SC | Noto Sans Mono CJK SC |
| English | Liberation Serif | Liberation Sans | Fira Code |
| Japanese | Noto Serif JP | Noto Sans JP | Noto Sans Mono CJK JP |

### Font Paths (for reference)

- **macOS**: `/System/Library/Fonts/`
- **Linux**: `/usr/share/fonts/`
- **Windows**: `C:/Windows/Fonts/`

---

## Page Layout (页面布局)

### Standard Sizes

| Size | Dimensions (mm) | Use Case |
|------|-----------------|----------|
| A4 | 210 × 297 | Standard documents |
| Letter | 216 × 279 | US documents |
| A3 | 297 × 420 | Large reports |

### Margin Presets

| Preset | Top/Bottom | Left/Right |
|--------|------------|------------|
| Normal | 2.54cm | 2.54cm |
| Narrow | 1.27cm | 1.27cm |
| Wide | 2.54cm | 5.08cm |

---

## Error Handling

```
字体缺失       → 使用开源字体回退
图片格式不支持 → 转换为PNG/JPEG
内存不足       → 分页处理大文档
生成失败       → 输出HTML备选
```

---

## Security Notes (安全说明)

- ✅ No network calls or external endpoints
- ✅ No credentials or API keys required
- ✅ Local file processing only
- ✅ No data uploaded to external servers
- ⚠️ Requires python3 and manually installed libraries
- ⚠️ Review code before execution

## Notes

- 使用FPDF2确保跨平台一致性
- 所有字体可嵌入PDF中
- 支持PDF/A归档标准
- 图片自动压缩优化
- 支持水印和页眉页脚
- **依赖**：用户需自行安装 Python 库（fpdf2/weasyprint/reportlab）