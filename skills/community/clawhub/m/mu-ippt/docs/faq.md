# FAQ — mu-ippt

[English](#english) | [中文](#中文)

---

## English

### What is mu-ippt?

mu-ippt is an AI-powered Skill for creating professional, natively editable PowerPoint presentations. It covers the full PPT workflow: generating from scratch, creating technical diagrams, using consulting report templates, and editing existing PPTs.

### What AI tools does it work with?

mu-ippt works with any AI coding assistant that supports Skills/prompts, including Claude Code, Cursor, Windsurf, VS Code Copilot, CatPaw Desk, and more.

### What formats does it support as input?

You can use PDF, DOCX, URL, Markdown, plain text, or any document as input. mu-ippt will convert your content into a polished presentation.

### Are the generated PPTs truly editable?

Yes. Unlike tools that export images into slides, mu-ippt generates real PowerPoint shapes, text boxes, and charts using DrawingML. Every element can be clicked and edited directly in PowerPoint, Keynote, or Google Slides.

### How many templates are available?

mu-ippt includes 20 layout templates, 40 consulting report templates, 119 chart types, and 6,732 vector icons. It also supports 14 design philosophies and 8 canvas formats.

### What are the 5 workflows?

- **Workflow 0**: Multi-page requirement routing and diagnosis
- **Workflow A**: Generate multi-page PPT from scratch (SVG → DrawingML pipeline)
- **Workflow B**: Generate single technical diagrams and charts
- **Workflow C**: Consulting report templates (python-pptx native shapes)
- **Workflow D**: Edit existing PPT files (OOXML unpack → edit → validate → repack)

### Do I need to install Python?

Python is required for some workflows (SVG to PPTX conversion, consulting templates, etc.). Install dependencies with `pip install -r requirements.txt`.

### Is it free?

Yes, mu-ippt is open source under the MIT license. You can use it freely for personal and commercial projects.

### How do I report bugs or request features?

- Bug reports & feature requests: [GitHub Issues](https://github.com/muippt/mu-ippt/issues)
- Questions & discussions: [GitHub Discussions](https://github.com/muippt/mu-ippt/discussions)
- Business inquiries: muippt@agent.qq.com

---

## 中文

### mu-ippt 是什么？

mu-ippt 是一个 AI 驱动的 PPT 智能创作 Skill，覆盖 PPT 全场景工作流：从零生成、技术图表、咨询汇报模板、编辑已有 PPT。

### 支持哪些 AI 工具？

mu-ippt 支持所有兼容 Skills/prompts 的 AI 编程助手，包括 Claude Code、Cursor、Windsurf、VS Code Copilot、CatPaw Desk 等。

### 支持哪些输入格式？

支持 PDF、DOCX、URL、Markdown、纯文本等任意文档作为输入，mu-ippt 会将内容转化为专业演示文稿。

### 生成的 PPT 是真正可编辑的吗？

是的。与导出图片到幻灯片的工具不同，mu-ippt 使用 DrawingML 生成真正的 PowerPoint 形状、文本框和图表。每个元素都可以在 PowerPoint、Keynote 或 Google Slides 中直接点击编辑。

### 有多少模板？

mu-ippt 包含 20 套布局模板、40 个咨询汇报模板、119 种图表类型和 6,732 个矢量图标。还支持 14 种设计哲学流派和 8 种画布格式。

### 5 个工作流是什么？

- **工作流 0**：多页需求路由与诊断
- **工作流 A**：从零生成多页 PPT（SVG → DrawingML 流水线）
- **工作流 B**：生成单张技术图表
- **工作流 C**：咨询汇报模板（python-pptx 原生形状）
- **工作流 D**：编辑已有 PPT 文件（OOXML 解包 → 编辑 → 验证 → 打包）

### 需要安装 Python 吗？

部分工作流需要 Python（SVG 转 PPTX、咨询模板等）。通过 `pip install -r requirements.txt` 安装依赖。

### 免费吗？

是的，mu-ippt 基于 MIT 许可证开源，可自由用于个人和商业项目。

### 如何反馈问题或提建议？

- Bug 反馈与功能建议：[GitHub Issues](https://github.com/muippt/mu-ippt/issues)
- 提问与交流：[GitHub Discussions](https://github.com/muippt/mu-ippt/discussions)
- 商务合作：muippt@agent.qq.com
