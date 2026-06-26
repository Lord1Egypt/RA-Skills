# PDF智能处理套件 (PDF Intelligence Suite)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一站式PDF文档智能处理解决方案，支持文本提取、表格识别、OCR文字识别、格式转换等功能。

## 📋 功能特性

| 功能模块 | 描述 | 状态 |
|---------|------|------|
| 文本提取 | 从PDF提取纯文本或结构化文本 | ✅ |
| 表格识别 | 自动识别表格并导出为Excel/CSV | ✅ |
| OCR识别 | 扫描件文字识别，支持中英文 | ✅ |
| PDF转Word | 转换为可编辑的DOCX格式 | ✅ |
| PDF转Excel | 提取表格数据到Excel | ✅ |
| 页面操作 | 合并、拆分、旋转、删除页面 | ✅ |
| 安全处理 | 加密、解密、添加水印 | ✅ |

## 🚀 快速开始

### 安装

```bash
# 克隆或下载本技能到 skills 目录
cd /root/.openclaw/workspace/skills/pdf-intelligence-suite

# 安装依赖
pip install -r requirements.txt

# 安装Tesseract OCR（用于OCR功能）
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# macOS:
brew install tesseract tesseract-lang

# Windows:
# 下载安装: https://github.com/UB-Mannheim/tesseract/wiki
```

### 基础使用

```python
from src.pdf_intelligence_suite import (
    PDFExtractor, 
    TableExtractor, 
    OCRProcessor,
    PDFConverter
)

# 1. 提取文本
extractor = PDFExtractor()
text = extractor.extract_text("document.pdf")
print(text)

# 2. 提取表格
tables = TableExtractor.extract_tables("report.pdf")
for i, table in enumerate(tables):
    table.to_excel(f"table_{i}.xlsx")

# 3. OCR识别扫描件
ocr = OCRProcessor(languages=['chi_sim', 'eng'])
text = ocr.process_pdf("scanned.pdf")
print(text)

# 4. PDF转Word
converter = PDFConverter()
converter.to_word("input.pdf", "output.docx")
```

## 📖 详细文档

### 1. 文本提取 (PDFExtractor)

```python
from src.pdf_intelligence_suite import PDFExtractor

extractor = PDFExtractor()

# 提取全部文本
text = extractor.extract_text("document.pdf")

# 提取指定页面
text = extractor.extract_text("document.pdf", pages=[0, 1, 2])

# 提取带位置信息的文本
elements = extractor.extract_with_layout("document.pdf")
for elem in elements:
    print(f"Text: {elem.text}, Page: {elem.page}, Position: {elem.bbox}")

# 按坐标区域提取
text = extractor.extract_by_bbox("document.pdf", page=0, bbox=(100, 100, 300, 200))
```

### 2. 表格识别 (TableExtractor)

```python
from src.pdf_intelligence_suite import TableExtractor

# 提取所有表格
tables = TableExtractor.extract_tables("report.pdf")

# 提取指定页面的表格
tables = TableExtractor.extract_tables("report.pdf", pages=[1, 2])

# 指定提取方法
# 'lattice': 用于有清晰边框的表格
# 'stream': 用于无边框或空格分隔的表格
tables = TableExtractor.extract_tables("report.pdf", method='lattice')

# 导出格式
for i, table in enumerate(tables):
    # 转为DataFrame
    df = table.df
    
    # 保存为Excel
    table.to_excel(f"table_{i}.xlsx")
    
    # 保存为CSV
    table.to_csv(f"table_{i}.csv")
```

### 3. OCR文字识别 (OCRProcessor)

```python
from src.pdf_intelligence_suite import OCRProcessor

# 初始化（指定语言）
ocr = OCRProcessor(languages=['chi_sim', 'eng'])  # 中文简体+英文

# 识别整个PDF
text = ocr.process_pdf("scanned.pdf")

# 识别指定页面
text = ocr.process_pdf("scanned.pdf", pages=[0, 1])

# 识别单张图片
from PIL import Image
img = Image.open("page.png")
text = ocr.process_image(img)

# 获取详细结果（包含位置信息）
results = ocr.process_pdf_with_data("scanned.pdf")
for item in results:
    print(f"Text: {item['text']}, Confidence: {item['confidence']}")
```

### 4. 格式转换 (PDFConverter)

```python
from src.pdf_intelligence_suite import PDFConverter

converter = PDFConverter()

# PDF转Word
converter.to_word("input.pdf", "output.docx")

# PDF转Excel
converter.to_excel("input.pdf", "output.xlsx")

# PDF转图片（每页一张）
converter.to_images("input.pdf", output_dir="./images", fmt="png")

# PDF转文本
converter.to_text("input.pdf", "output.txt")

# PDF转HTML
converter.to_html("input.pdf", "output.html")
```

### 5. 页面操作 (PDFManipulator)

```python
from src.pdf_intelligence_suite import PDFManipulator

manip = PDFManipulator()

# 合并多个PDF
manip.merge(["file1.pdf", "file2.pdf", "file3.pdf"], "merged.pdf")

# 拆分PDF
manip.split("document.pdf", [3, 5], "part_{}.pdf")  # 在第3页和第5页后拆分

# 旋转页面
manip.rotate("document.pdf", [0, 1], 90, "rotated.pdf")  # 第1、2页顺时针旋转90度

# 删除页面
manip.remove_pages("document.pdf", [2, 3], "removed.pdf")

# 提取页面
manip.extract_pages("document.pdf", [0, 2, 4], "extracted.pdf")

# 插入页面
manip.insert_pages("base.pdf", "insert.pdf", position=2, output="result.pdf")
```

### 6. 安全处理 (PDFSecurity)

```python
from src.pdf_intelligence_suite import PDFSecurity

security = PDFSecurity()

# 加密PDF
security.encrypt("input.pdf", "encrypted.pdf", password="secret123")

# 解密PDF
security.decrypt("encrypted.pdf", "decrypted.pdf", password="secret123")

# 添加水印
security.add_watermark(
    "input.pdf", 
    "watermarked.pdf",
    text="CONFIDENTIAL",
    opacity=0.3,
    angle=45
)

# 添加图片水印
security.add_image_watermark(
    "input.pdf",
    "watermarked.pdf", 
    image_path="logo.png",
    position="center"
)
```

## 🧪 运行测试

```bash
cd /root/.openclaw/workspace/skills/pdf-intelligence-suite

# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_pdf_suite.py::TestPDFExtractor -v

# 生成覆盖率报告
python -m pytest tests/ --cov=src/pdf_intelligence_suite --cov-report=html
```

## 📁 项目结构

```
pdf-intelligence-suite/
├── SKILL.md                          # 技能描述文件
├── README.md                         # 本文档
├── requirements.txt                  # Python依赖
├── setup.py                          # 安装脚本
├── examples/
│   └── basic_usage.py               # 使用示例
├── src/pdf_intelligence_suite/
│   ├── __init__.py
│   ├── extractor.py                 # 文本提取
│   ├── tables.py                    # 表格识别
│   ├── ocr.py                       # OCR识别
│   ├── converter.py                 # 格式转换
│   ├── manipulator.py               # 页面操作
│   ├── security.py                  # 安全处理
│   └── utils.py                     # 工具函数
└── tests/
    └── test_pdf_suite.py            # 单元测试
```

## ⚙️ 配置说明

### Tesseract 路径配置

如果Tesseract未安装在默认路径，请设置环境变量：

```bash
# Linux/macOS
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Windows
set TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
```

或在代码中指定：

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
```

## 🔧 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| PyPDF2 | >=3.0.0 | PDF基础操作 |
| pdfplumber | >=0.10.0 | 高级文本/表格提取 |
| camelot-py | >=0.11.0 | 表格识别引擎 |
| pytesseract | >=0.3.10 | OCR接口 |
| pdf2image | >=1.16.3 | PDF转图片 |
| python-docx | >=0.8.11 | Word文档处理 |
| openpyxl | >=3.0.0 | Excel处理 |
| Pillow | >=9.0.0 | 图像处理 |
| reportlab | >=3.6.0 | PDF生成 |

## 🐛 常见问题

### Q: OCR识别中文时出现乱码？

A: 确保已安装中文语言包：
```bash
# Ubuntu
sudo apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# macOS
brew install tesseract-lang
```

### Q: 表格识别不准确？

A: 尝试切换识别方法：
```python
# 对于有边框的表格
tables = TableExtractor.extract_tables("report.pdf", method='lattice')

# 对于无边框表格
tables = TableExtractor.extract_tables("report.pdf", method='stream')
```

### Q: 转换后的Word格式错乱？

A: 复杂PDF布局转换为Word可能存在限制，建议：
1. 先提取文本，再手动排版
2. 使用PDF转图片+OCR识别的方式

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进本技能！

## 📧 联系

如有问题，请在ClawHub Skills仓库提交Issue。
