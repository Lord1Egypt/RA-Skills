---
name: md-to-html
version: 1.0.2
description: "将Markdown格式的笔记转换为带左侧固定目录大纲的可阅读HTML文件。适用于：(1) 将学习笔记、技术文档转换为可浏览的HTML；(2) 为Markdown文件生成带目录导航的阅读界面；(3) 整理长文档生成静态网站。触发条件：用户说转换HTML、markdown转html、生成HTML笔记、把笔记转成网页等"
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["python"] } } }
---

# Markdown转HTML工具

将Markdown笔记转换为带有左侧固定目录大纲的可阅读HTML页面。

## 使用方法

### 基本命令

```bash
python scripts/md2html.py -i <markdown文件路径>
```

> **提示**：Agent 会自动使用正确的 Python 路径执行脚本。

### 参数说明

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入的Markdown文件路径（必需） |
| `-o, --output` | 输出的HTML文件路径（可选，默认与输入同目录） |
| `-t, --title` | HTML页面标题（可选，默认使用文件名） |
| `-l, --level` | 目录中显示的最大标题层级（1-6，默认4） |

### 示例

```bash
# 基本转换
python scripts/md2html.py -i "AI学习笔记.md"

# 指定输出路径
python scripts/md2html.py -i notes.md -o output.html

# 指定标题和目录层级
python scripts/md2html.py -i notes.md -t "我的学习笔记" -l 3
```

## 输出特点

生成的HTML包含：
- **左侧固定目录**：自动从标题生成，支持折叠/展开
- **目录交互**：点击跳转、滚动高亮、可拖拽调整宽度
- **代码高亮**：Prism.js 支持 Python、Bash、JavaScript、JSON
- **数学公式**：KaTeX 支持 LaTeX 语法（完全离线，字体内嵌）
- **Mermaid图表**：支持 flowchart、sequenceDiagram、graph 等图表
- **响应式设计**：适配移动端，自动隐藏侧边栏
- **返回顶部**：滚动后显示返回顶部按钮
- **完全离线**：所有 JS/CSS/字体已内嵌，无需网络连接

## 支持的Markdown特性

- 标题（H1-H6）
- 段落、粗体、斜体
- 有序/无序列表
- 代码块（带语法高亮）
- 表格
- 引用块
- 图片
- 超链接
- 数学公式（LaTeX）
- Mermaid 图表

## 目录结构

```
md-to-html/
├── SKILL.md              # 技能说明文档
├── scripts/
│   └── md2html.py        # 转换脚本
└── lib/                  # 内嵌的 JS/CSS 库
    ├── prism-tomorrow.min.css   # Prism 主题
    ├── prism.min.js             # Prism 核心
    ├── prism-python.min.js      # Python 语法
    ├── prism-bash.min.js        # Bash 语法
    ├── prism-javascript.min.js  # JavaScript 语法
    ├── prism-json.min.js        # JSON 语法
    ├── mermaid.min.js           # Mermaid 图表
    ├── katex.min.js             # KaTeX 核心
    ├── katex.embedded.css       # KaTeX 样式（含内嵌字体）
    └── auto-render.min.js       # KaTeX 自动渲染
```

## 依赖

- Python 3.x
- markdown (Python库)

所有前端库已打包到 `lib/` 目录，无需网络即可使用。