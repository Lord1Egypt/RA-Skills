# 🔍 LiaoGong-OCR · 廖工双引擎OCR

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey)]()

**廖工AI设计实战出品** — easyocr + tesseract 双引擎OCR系统，15条预处理链含实测基准数据。从截图、海报、手机拍照、文档中优雅提取文字。

---

## 🎯 为什么双引擎？

| 引擎 | 擅长 | 短板 |
|------|------|------|
| **easyocr** | 中文截图、海报、复杂排版 | 速度慢，首次下载100MB模型 |
| **tesseract** | 英文文档、白底黑字、极快 | 中文复杂排版效果差 |

一个工具，两个引擎，自动选择最优方案。

---

## ⚡ 三种安装方式

### 方式一：pip 安装

```bash
pip install liaogong-ocr
# 或开发模式
git clone https://github.com/jnbno1163/liaogong-ocr.git
cd liaogong-ocr
pip install -e .
```

安装后直接使用命令：

```bash
liaogong-ocr your_image.jpg
```

### 方式二：GitHub 克隆

```bash
git clone https://github.com/jnbno1163/liaogong-ocr.git
cd liaogong-ocr
pip install -r requirements.txt
python -m liaogong_ocr.engine your_image.jpg
```

### 方式三：AI Agent 触发

```bash
npx clawhub@latest install liaogong-ocr
```

触发词：`OCR this image` / `图片转文字` / `OCR识别` / `提取图片文字`

---

## 📖 三种用法

### CLI 工具

```bash
# 自动选择引擎
liaogong-ocr poster.jpg

# 中文复杂场景用 easyocr
liaogong-ocr -e easyocr screenshot.png

# 英文文档快速 OCR
liaogong-ocr -e tesseract document.png

# 手机拍照优化模式（87%数字准确率）
liaogong-ocr -p phone photo.jpg

# 保存到文件
liaogong-ocr image.jpg -o result.txt

# 显示详细信息
liaogong-ocr image.jpg --verbose
```

### Python 库

```python
from liaogong_ocr import OCREngine

engine = OCREngine()
result = engine.process("poster.jpg", engine="easyocr")
print(result["text"])
print(result["confidence"])
print(result["engine_used"])
```

```python
from liaogong_ocr import CHAINS, chain_cross_validate

# 应用最优手机拍照预处理链
img = CHAINS['optimal_phone'](image)

# 多链交叉验证（可靠性更高）
results = chain_cross_validate(image)
```

### AI Agent 触发

安装 ClawHub 技能后，AI 助手自动识别以下触发词并调用 OCR：
- `OCR this image` / `extract text from image`
- `图片转文字` / `OCR识别` / `提取图片文字` / `截图转文字`

---

## 🔬 预处理链实测对比

手机拍屏幕数字提取，15条预处理链实测结果：

| 预处理链 | 处理方式 | 数字准确率 | 速度 |
|----------|----------|-----------|------|
| **optimal_phone** | 反色+灰度+对比度2.5x | **87%** | 快 |
| grayscale_binary | 灰度+二值化阈值128 | 72% | 快 |
| contrast_enhance | 灰度+对比度增强2.0x | 65% | 快 |
| sharpen | 灰度+锐化滤镜 | 55% | 快 |
| clahe | CLAHE直方图均衡化 | 31% | 中 |
| adaptive_binary | 自适应二值化阈值 | 18% | 慢 |

---

## 📁 项目结构

```
liaogong-ocr/
├── liaogong_ocr/              # Python 包
│   ├── __init__.py            # 导出 OCREngine, CHAINS, CHAIN_BENCHMARKS
│   ├── engine.py              # 核心双引擎OCR
│   └── preprocess.py          # 15条可组合预处理链
├── scripts/
│   ├── benchmark_chains.py    # 重现基准测试
│   └── batch_ocr.py           # 批量文件夹OCR
├── tests/
│   └── test_ocr_engine.py     # 冒烟测试
├── examples/                  # 示例图片
├── references/                # 预处理指南+基准报告
├── setup.py                   # pip 安装配置
└── requirements.txt
```

---

## 🔧 系统要求

- **Python** 3.8+
- **Tesseract** 系统安装：
  - Windows: `winget install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Linux: `sudo apt install tesseract-ocr`
- **easyocr** 1.7+（首次运行下载 ~100MB 模型，之后缓存本地）

---

**廖工AI设计实战出品 · [github.com/jnbno1163](https://github.com/jnbno1163)**
