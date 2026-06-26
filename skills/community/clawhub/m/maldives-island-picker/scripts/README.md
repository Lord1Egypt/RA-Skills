# Scripts 目录

本目录包含马尔代夫选岛助手的辅助脚本。

## export-pdf.py

**用途**：将 Markdown 格式的选岛报告转换为 PDF

**使用时机**：步骤 5 导出报告时，如果用户要求 PDF 格式

**用法**：
```bash
# 首次使用需安装依赖
pip install markdown weasyprint

# 转换 Markdown 为 PDF
python scripts/export-pdf.py 马尔代夫选岛报告-2026-04-01.md

# 或指定输出文件名
python scripts/export-pdf.py 输入.md 输出.pdf
```

**特性**：
- 自动检测并提示安装缺失依赖
- 中文排版优化（PingFang SC / Microsoft YaHei 字体）
- 表格、引用、图片样式美化
- 支持 Markdown 表格、代码块等格式
