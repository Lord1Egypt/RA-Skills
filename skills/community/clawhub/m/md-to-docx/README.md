# md-to-docx

> Claude Code / OpenClaw Skill：将 Markdown 转为排版精美的 Word 文档，自动适配模板格式，支持 Mermaid 图表渲染。

## Quick Start

```bash
# 1. 安装前置依赖
pip install python-docx
npm install -g @mermaid-js/mermaid-cli

# 2. 安装 Skill（二选一）
npx openclaw add skill https://github.com/KrabWW/md-to-docx    # OpenClaw
git clone https://github.com/KrabWW/md-to-docx.git && claude skill add ./md-to-docx  # Claude Code

# 3. 使用（自然语言）
帮我把 chapter01.md 转成 Word 文档
```

## 效果预览

| 特性 | 说明 |
|------|------|
| 模板格式自动提取 | 给一个 `.doc`/`.docx` 模板，自动识别字体、字号、对齐、缩进、页边距 |
| Mermaid 图表渲染 | Markdown 中的 Mermaid 代码块自动转为 PNG 图片嵌入文档 |
| 中文排版标准 | 无模板时默认使用宋体/黑体、五号字、首行缩进两字符 |
| 行内格式保留 | **粗体**、*斜体*、`代码`、~~删除线~~ 全部保留 |
| 跨平台 | macOS / Windows / Linux 自动检测 Chrome |

---

## 快速安装

### 第 1 步：安装前置依赖

```bash
# Python 依赖（生成 Word 文档）
pip install python-docx

# Mermaid CLI（渲染流程图为 PNG）
npm install -g @mermaid-js/mermaid-cli

# Chrome 浏览器（Mermaid 渲染引擎）
# macOS / Windows 通常已预装，Linux 需手动安装：
#   sudo apt install google-chrome-stable
```

### 第 2 步：安装 Skill

**Claude Code：**

```bash
git clone https://github.com/KrabWW/md-to-docx.git
claude skill add /path/to/md-to-docx
```

**OpenClaw：**

```bash
npx openclaw add skill https://github.com/KrabWW/md-to-docx
```

### 第 3 步：开始使用

安装完成后，直接用自然语言告诉 AI 就行：

```
帮我把 chapter01.md 转成 Word 文档
```

```
用 docs/正文模板.doc 作为模板，把 report.md 导出为 Word
```

```
Convert README.md to docx
```

搞定。

---

## 命令行独立使用

不想通过 AI 助手？也可以直接当 Python 脚本用：

```bash
# 基本转换（使用中文默认排版）
python3 scripts/md_to_docx.py input.md -o output.docx

# 使用模板（自动提取格式）
python3 scripts/md_to_docx.py input.md -o output.docx -t template.doc

# 使用 .docx 模板
python3 scripts/md_to_docx.py input.md -o output.docx -t template.docx
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `input` | 输入的 Markdown 文件 | `chapter01.md` |
| `-o` | 输出路径（默认与输入同名 `.docx`） | `-o output.docx` |
| `-t` | 模板文件（`.doc` 或 `.docx`） | `-t template.doc` |

---

## 模板格式检测

提供一个 Word 模板文件，脚本会自动分析并提取：

| 提取项 | 识别方式 |
|--------|---------|
| 标题层级 | 按字号+对齐方式排序，最大居中 = 章标题 |
| 正文字体 | 有首行缩进的最大段落 |
| 页面设置 | 直接复制模板的页边距和纸张大小 |
| 中文字体配对 | 保留模板中的映射（如 Times New Roman ↔ 宋体） |

### 无模板时的默认格式

| 元素 | 字体 | 字号 | 对齐 |
|------|------|------|------|
| 章标题 (h1) | 黑体 | 18pt | 居中 |
| 节标题 (h2) | 黑体 | 16pt | 居中 |
| 小节标题 (h3) | 黑体 | 14pt | 左对齐 |
| 正文 | 宋体 | 10.5pt (五号) | 两端对齐，首行缩进 |
| 代码块 | Consolas | 9pt | 左对齐 |
| 引用 | 楷体 | 10.5pt | 斜体，左缩进 |

---

## 支持的 Markdown 语法

| 语法 | 示例 | 效果 |
|------|------|------|
| 标题 | `#` `##` `###` `####` | 自动匹配标题层级格式 |
| 粗体 | `**文本**` | 加粗 |
| 斜体 | `*文本*` | 斜体 |
| 行内代码 | `` `代码` `` | Consolas 等宽字体 |
| 删除线 | `~~文本~~` | 删除线 |
| 无序列表 | `- 项目` / `* 项目` | 圆点列表，悬挂缩进 |
| 有序列表 | `1. 项目` | 数字列表 |
| 表格 | `\| 表头 \| 表头 \|` | 带边框的 Word 表格 |
| 代码块 | ` ```python ` | 等宽字体 + 语言标签 |
| Mermaid | ` ```mermaid ` | 渲染为 PNG 嵌入 |
| 引用块 | `> 文本` | 斜体 + 左缩进 + 灰色 |
| 分隔线 | `---` | 居中横线 |

---

## 常见问题

### Q: Mermaid 图表渲染失败怎么办？

检查以下几点：
1. 是否安装了 `mmdc`：`mmdc --version`
2. 是否安装了 Chrome：macOS 检查 `/Applications/Google Chrome.app`
3. 渲染失败时会自动回退为代码块展示，不影响文档生成

### Q: `.doc` 模板无法识别？

macOS 会自动用 `textutil` 转换。Linux 需要安装 LibreOffice：
```bash
sudo apt install libreoffice
```

### Q: 如何自定义中文字体映射？

编辑 `scripts/md_to_docx.py` 中的 `get_cn_font()` 函数，修改字体映射表。

---

## License

MIT
