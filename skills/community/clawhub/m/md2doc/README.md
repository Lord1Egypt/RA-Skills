# MD2DOC - Markdown 文档转换器

专业的 Markdown 转 Word/PDF/HTML 工具，支持多种样式模板。

## 功能特性

- ✅ **多格式输出** - Word (.docx)、PDF、HTML
- ✅ **6 种样式模板** - 商务蓝、技术灰、简洁白、产品红、学术风、默认
- ✅ **智能封面** - 自动生成专业封面页
- ✅ **自动目录** - 基于标题层级生成目录
- ✅ **页眉页脚** - 自动添加页码和页眉
- ✅ **图片嵌入** - 支持本地图片和网络图片
- ✅ **表格美化** - 表头带背景色
- ✅ **代码高亮** - 代码块带样式

## 快速开始

### 安装依赖
```bash
pip install python-docx requests markdown beautifulsoup4 Pillow
```

### 基本使用
```bash
# Markdown 转 Word
python scripts/convert.py input.md

# 使用样式模板
python scripts/convert.py input.md --style business

# 同时输出 Word + PDF + HTML
python scripts/convert.py input.md --all

# 带封面的完整示例
python scripts/convert.py prd.md \
    --style product \
    --output prd.docx \
    --pdf prd.pdf \
    --html prd.html \
    --cover-author "产品团队" \
    --cover-date "2026年3月"
```

## 样式模板

| 样式 | 特点 | 封面 | 目录 | 页眉 | 页脚 |
|------|------|------|------|------|------|
| `default` | 标准样式 | ❌ | ✅ | ❌ | ✅ |
| `business` | 商务蓝主题 | ✅ | ✅ | ✅ | ✅ |
| `tech` | 技术灰风格 | ❌ | ✅ | ❌ | ✅ |
| `minimal` | 极简黑白 | ❌ | ❌ | ❌ | ❌ |
| `product` | 产品红强调 | ✅ | ✅ | ❌ | ✅ |
| `academic` | 学术宋体 | ✅ | ✅ | ✅ | ✅ |

## 命令行参数

```
python scripts/convert.py <input.md> [选项]

选项:
  --output, -o          输出 Word 文件路径
  --pdf, -p             输出 PDF 文件路径
  --html                输出 HTML 文件路径
  --all, -a             同时输出所有格式
  --style, -s           样式模板 (default/business/tech/minimal/product/academic)
  --list-styles         列出所有可用样式
  --cover-title         封面标题
  --cover-subtitle      封面副标题
  --cover-author        作者
  --cover-date          日期
```

## 在 OpenClaw 中使用

```python
import subprocess

# 基本转换
result = subprocess.run([
    "python", "skills/md2doc/scripts/convert.py",
    "文档.md", "--style", "business"
], capture_output=True, text=True)

# 完整转换（Word + PDF + HTML）
result = subprocess.run([
    "python", "skills/md2doc/scripts/convert.py",
    "prd.md", "--all", "--style", "product",
    "--cover-author", "产品团队"
], capture_output=True, text=True)
```

## 目录结构

```
md2doc/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── package.json          # 包信息
├── scripts/
│   ├── convert.py        # 主转换脚本
│   └── md2doc.py         # OpenClaw 入口
└── templates/
    └── styles.py         # 样式模板配置
```

## 依赖说明

- **Word 转 PDF**: 需要安装 Microsoft Word 或 LibreOffice
- **HTML 导出**: 纯 Python，无需额外软件
- **图片处理**: 自动下载网络图片并嵌入

## License

MIT
