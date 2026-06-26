# 🚀 markdown2pdf 快速开始指南

## 1️⃣ 安装依赖

### 方法 A: 使用安装脚本（推荐）

```bash
cd /root/.openclaw/workspace/skills/markdown2pdf
chmod +x install.sh
./install.sh
```

### 方法 B: 手动安装

```bash
# 安装 Python 依赖
pip3 install markdown pdfkit imgkit

# 安装 wkhtmltopdf
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# CentOS/RHEL
sudo yum install wkhtmltopdf
```

---

## 2️⃣ 测试安装

```bash
cd /root/.openclaw/workspace/skills/markdown2pdf

# 运行快速测试
python3 test_quick.py

# 测试转换（需要 wkhtmltopdf）
python3 src/converter.py test_document.md -t github -f pdf
```

---

## 3️⃣ 使用方法

### CLI 使用

```bash
# 基本用法（生成 PDF 和 PNG）
python3 src/converter.py input.md

# 只生成 PDF
python3 src/converter.py input.md -f pdf

# 只生成 PNG
python3 src/converter.py input.md -f png

# 使用主题
python3 src/converter.py input.md -t github

# 指定输出文件名
python3 src/converter.py input.md -o my-document

# 指定输出目录
python3 src/converter.py input.md -d ./output

# 组合使用
python3 src/converter.py README.md -t github -f pdf -o readme -d ./docs
```

### 可用主题

```bash
# 列出所有主题
python3 src/converter.py --list-themes

# 输出：
# Available themes:
#   - default
#   - dark
#   - github
#   - minimal
#   - professional
```

### 主题说明

| 主题 | 描述 | 适用场景 |
|------|------|----------|
| `default` | 现代简洁设计 | 通用文档 |
| `dark` | 深色主题 | 演示、夜间阅读 |
| `github` | GitHub 风格 | 技术文档、README |
| `minimal` | 极简设计 | 优雅文档、出版物 |
| `professional` | 商务风格 | 报告、商业文档 |

---

## 4️⃣ Python API 使用

```python
from src.converter import (
    MarkdownConverter,
    convert_markdown,
    convert_markdown_to_pdf,
    convert_markdown_to_png
)

# 方法 1: 简单转换
pdf_path = convert_markdown_to_pdf(
    markdown_text="# Hello World",
    output_filename="hello.pdf",
    theme="github"
)

# 方法 2: 多格式转换
results = convert_markdown(
    markdown_text="# Document",
    output_filename="doc",
    formats=["pdf", "png"],
    theme="professional"
)

# 方法 3: 高级用法
converter = MarkdownConverter(
    output_dir=Path("./output"),
    theme="dark",
    custom_css=".custom { color: red; }"
)

# 转换为 PDF
pdf_path = converter.convert_to_pdf(
    markdown_text="# My Document",
    output_filename="document.pdf",
    page_size="A4",
    margin="15mm"
)

# 转换为 PNG
png_path = converter.convert_to_png(
    markdown_text="# My Document",
    output_filename="document.png",
    width=1920,
    quality=100
)

# 转换为多种格式
results = converter.convert(
    markdown_text="# My Document",
    output_filename="document",
    formats=["pdf", "png"]
)

print(f"PDF: {results['pdf']}")
print(f"PNG: {results['png']}")
```

---

## 5️⃣ OpenClaw 集成

在 OpenClaw 中使用时，markdown2pdf 会自动处理你的 markdown 输出并转换为 PDF/PNG。

### 配置示例

```json
{
  "skills": {
    "markdown2pdf": {
      "enabled": true,
      "config": {
        "default_theme": "github",
        "default_formats": ["pdf"],
        "output_dir": "./documents"
      }
    }
  }
}
```

### 使用示例

当你在 OpenClaw 中生成 markdown 内容时，可以自动转换为 PDF：

```
/convert README.md -t github -f pdf
```

---

## 6️⃣ 常见问题

### Q: 提示 `ModuleNotFoundError: No module named 'markdown'`

**A:** 安装 Python 依赖：
```bash
pip3 install markdown pdfkit imgkit
```

### Q: 提示 `wkhtmltopdf not found`

**A:** 安装 wkhtmltopdf：
- macOS: `brew install wkhtmltopdf`
- Ubuntu: `sudo apt-get install wkhtmltopdf`
- Windows: 从 https://wkhtmltopdf.org 下载

### Q: 生成的 PDF 是空白的

**A:** 检查：
1. markdown 文件是否有内容
2. wkhtmltopdf 是否正确安装
3. 查看错误信息

### Q: 如何自定义样式？

**A:** 使用自定义 CSS：
```python
converter = MarkdownConverter(
    theme='minimal',
    custom_css="""
        h1 { color: #2c3e50; }
        .codehilite { background: #f8f8f8; }
    """
)
```

---

## 7️⃣ 示例文件

项目包含一个测试文件：

```bash
# 查看测试文件
cat test_document.md

# 转换测试文件
python3 src/converter.py test_document.md -t github -f pdf,png
```

---

## 📞 需要帮助？

- 查看 README.md 获取完整文档
- 运行 `python3 src/converter.py --help` 查看 CLI 帮助
- 查看 GitHub Issues: https://github.com/leohuang8688/markdown2pdf/issues

---

**祝你使用愉快！📄🖼️**

— PocketAI 🧤
