# pdf-vision-reader

PDF 视觉阅读器 — 用 AI 视觉能力理解任意 PDF

## 功能

- 将 PDF 每页转换为高清 PNG 图片
- 用 AI 视觉模型分析图片内容（中英文）
- 识别：水印、表格、图表、数据、布局结构
- 适合：幻灯片 PDF、图片型 PDF、扫描件

## 安装依赖

```bash
pip install pymupdf numpy opencv-python-headless
```

## 使用方式

本技能通过 OpenClaw 自动调用，无需手动执行脚本。

主要流程：
1. 接收用户 PDF 文件或路径
2. 调用 `scripts/extract.py` 提取图片
3. 用视觉 AI 模型分批分析
4. 整合结果并输出

## 手动测试

```bash
cd C:\Users\Administrator\.openclaw\workspace
python skills/pdf-vision-reader/scripts/extract.py "你的PDF路径.pdf" "输出目录"
```

## 依赖

- Python 3.8+
- PyMuPDF (pip install pymupdf)
- numpy
- opencv-python-headless
