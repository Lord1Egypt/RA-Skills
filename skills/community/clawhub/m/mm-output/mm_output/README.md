# MMOutput - Multi-modal Output Module

多模态输出模块，用于将 PosterGen 生成的 HTML 转换为 PDF、PNG 和 DOCX 格式。

## 功能特性

- **PDF 输出**: 使用无头浏览器 Chrome (Playwright) 将 HTML 打印为 PDF
- **PNG 输出**: 使用无头浏览器 Chrome 截取 HTML 页面为 PNG 图片
- **DOCX 输出**: 使用 python-docx 将 HTML 内容转换为 Word 文档

## 安装依赖

```bash
pip install playwright python-docx beautifulsoup4
playwright install chromium
```

## 命令行使用

```bash
python -m mm_output.cli input.html --format all --output-dir ./outputs/
```

python -m mm_output.cli ./output/poster_llm__report_web_reduced.html --format pptx --output ./mm_outputs/poster_llm.pptx