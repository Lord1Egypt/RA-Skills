# 🚀 markdown2pdf 安装指南

## ✅ 项目已准备就绪

**markdown2pdf** 是一个 OpenClaw skill，能将 markdown 输出转化为 PDF 文件和 PNG 图片。

---

## 📁 项目结构

```
markdown2pdf/
├── src/converter.py       # 主转换器
├── test_document.md       # 测试文件
├── test_quick.py          # 快速测试
├── install.sh             # 安装脚本
├── INSTALL.md             # 安装指南
├── README.md              # 完整文档
└── SKILL.md               # OpenClaw 定义
```

---

## 🎨 功能特性

- 📄 **Markdown 转 PDF** - 专业 PDF 文件生成
- 🖼️ **Markdown 转 PNG** - 高质量 PNG 图片
- 🎨 **5 种内置主题** - default, dark, github, minimal, professional
- ✨ **自定义 CSS** - 完全控制样式
- 🚀 **CLI 和 API** - 多种使用方式
- 🧩 **OpenClaw 集成** - 无缝集成

---

## 🔧 安装步骤

### 1️⃣ 安装 Python 依赖

```bash
cd /root/.openclaw/workspace/skills/markdown2pdf
pip3 install markdown pdfkit imgkit
```

### 2️⃣ 安装 wkhtmltopdf

```bash
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# Windows
# 下载 https://wkhtmltopdf.org/downloads.html
```

### 3️⃣ 运行安装脚本

```bash
chmod +x install.sh
./install.sh
```

---

## 📖 使用方法

### CLI 使用

```bash
# 基本用法（生成 PDF 和 PNG）
python3 src/converter.py input.md

# 只生成 PDF
python3 src/converter.py input.md -f pdf

# 使用 github 主题
python3 src/converter.py README.md -t github -f pdf

# 列出所有主题
python3 src/converter.py --list-themes
```

### 可用主题

| 主题 | 描述 | 适用场景 |
|------|------|----------|
| default | 现代简洁设计 | 通用文档 |
| dark | 深色主题 | 演示、夜间阅读 |
| github | GitHub 风格 | 技术文档、README |
| minimal | 极简设计 | 优雅文档、出版物 |
| professional | 商务风格 | 报告、商业文档 |

---

## 💻 Python API

```python
from src.converter import (
    MarkdownConverter,
    convert_markdown,
    convert_markdown_to_pdf
)

# 简单转换
pdf_path = convert_markdown_to_pdf(
    markdown_text="# Hello World",
    output_filename="hello.pdf",
    theme="github"
)

# 高级用法
converter = MarkdownConverter(
    output_dir=Path("./output"),
    theme="dark"
)

results = converter.convert(
    markdown_text="# Document",
    formats=["pdf", "png"]
)
```

---

## ✅ 测试结果

**所有核心功能测试通过！**

- ✅ 主题系统正常工作
- ✅ Markdown 转换器初始化正常
- ✅ HTML 生成正常
- ✅ CSS 生成正常

---

## 📞 需要帮助？

- 查看 `README.md` 获取完整文档
- 查看 `INSTALL.md` 获取详细安装指南
- 运行 `python3 src/converter.py --help` 查看 CLI 帮助

---

## 🎉 开始使用

**准备好试用了吗？**

1. 运行安装脚本：`./install.sh`
2. 测试功能：`python3 src/converter.py test_document.md`
3. 转换你的 markdown 文件！

---

**祝你使用愉快！📄🖼️**

— PocketAI 🧤
