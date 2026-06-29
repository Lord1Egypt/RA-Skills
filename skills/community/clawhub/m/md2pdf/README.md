# md2pdf

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
[![GitHub Release](https://img.shields.io/github/v/release/CoderMoray/md2pdf)](https://github.com/CoderMoray/md2pdf/releases)

一个 AI Agent Skill — 把 Markdown 转成排版精美的 PDF，自动生成封面、目录、书签、页码。你只需说一句话，剩下交给 AI。

## 目录

- [效果预览](#效果预览)
- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [封面配置](#封面配置)
- [AI 工作流](#ai-工作流)
- [安装与环境](#安装与环境)
- [CLI 参考](#cli-参考)
- [项目结构](#项目结构)
- [技术架构](#技术架构)
- [同类对比](#同类对比)
- [许可](#许可)

---

## 效果预览

- [📄 默认主题示例 PDF](output/README-default.pdf)
- [📄 学术主题示例 PDF](output/README-academic.pdf)

---

## 快速开始

### 安装

```bash
# 方式一：一键安装
npx skills add CoderMoray/md2pdf

# 方式二：手动 clone 到 skills 目录
cd skills
git clone https://github.com/CoderMoray/md2pdf.git
```

### 使用

安装后对 AI 说：

> "把这份 report.md 转成 PDF，用学术主题"

AI 会自动完成环境检测、转换、验证，你只需提供 Markdown 文件路径。

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 📄 封面页 | 从 YAML front-matter 自动生成标题、作者、日期、版本 |
| 📑 交互式目录 | 可点击目录页 + PDF 侧边栏书签（Outline） |
| 🔢 页码 | 每页底部居中 |
| 🎨 多主题 | `default` 苹果风格、`academic` 学术衬线 |
| 🌏 中文排版 | `--chinese-layout` 叠加到任意主题，行距/缩进/禁则 |
| 🈶 CJK 字体检测 | `--validate` 列出系统中文字体，Linux 自动提示安装 |
| 📊 表格/代码块 | 完整保留格式，highlight.js 语法高亮（190+ 语言） |
| ∑ KaTeX 公式 | pandoc `--katex` 原生渲染数学公式 |
| 📈 Mermaid 图表 | 注入 mermaid.js 渲染流程图、时序图、甘特图等 |
| 📐 智能分页 | 代码块/表格/图表保持完整不跨页，标题不孤行 |
| 🔧 环境自检 | 自动检测 pandoc + Playwright 是否就绪 |

---

## 封面配置

在 Markdown 文件头部添加 YAML 元数据，AI 自动读取并生成封面：

```yaml
---
title: "文档标题"
subtitle: "副标题"
author: "作者"
date: "2026-06-26"
version: "1.0"
---
```

所有字段可选。有 `title` 就有封面；没有 front-matter 时，自动用文件名作为封面标题。

---

## AI 工作流

加载 md2pdf Skill 后，AI 自动执行：

1. **环境检测** → 确保 pandoc + Playwright 就绪
2. **询问偏好** → 主题、字号、纸张、是否要封面/目录
3. **执行转换** → 调用底层脚本
4. **验证输出** → 页面诊断，检查空白页等异常
5. **交付结果** → 告知 PDF 位置

---

## 安装与环境

### 体积说明

md2pdf 本身很小（脚本 + 主题 < 100 KB），主要空间花在渲染引擎上：

| 层级 | 组件 | 大小 | 说明 |
|------|------|------|------|
| 📦 **本体** | `scripts/` + `themes/` | **< 0.1 MB** | Skill 核心代码，clone 即得 |
| 📎 **依赖①** | pandoc | **~35 MB** | Markdown → HTML 转换 |
| 🌐 **依赖②** | Playwright + Chromium | **~190 MB** | HTML → PDF 渲染引擎 |

> 💡 如果系统已安装 Chrome/Edge，md2pdf 可复用系统浏览器，无需额外下载 Chromium。`--validate` 会自动检测。

```bash
brew install pandoc
# 中文用户建议使用镜像：
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/playwright \
pip install playwright && playwright install chromium
```

---

## CLI 参考

如果不使用 AI Agent，也可以直接命令行调用：

```bash
python3 scripts/md2pdf.py --input doc.md --theme academic --katex --mermaid
```

> 💡 通过 AI Agent 使用时，直接告诉它要转什么文件即可，无需手动记参数。完整 CLI 参考见 [SKILL.md](SKILL.md)。

---

## 项目结构

```
md2pdf/
├── SKILL.md              # AI Agent Skill 描述
├── scripts/md2pdf.py     # 转换引擎
├── themes/
│   ├── default.css       # 默认主题（苹果风格）
│   ├── academic.css      # 学术主题
│   └── chinese.css       # 中文排版层（叠加用）
├── output/               # 生成的 PDF
├── docs/CHANGELOG.md
└── README.md
```

---

## 技术架构

```
Markdown → pandoc (--toc) → HTML → Playwright/Chromium → PDF
                                   ↑
                            封面 + CSS 主题
```

- **pandoc** 解析 Markdown，不依赖 AI
- **Playwright** 用真实浏览器渲染，输出与预览一致
- 全部逻辑内嵌脚本，结果可复现

### PDF 交互

| 特性 | 实现 |
|------|------|
| 侧边栏书签 | Playwright `outline: true` |
| 页内跳转 | pandoc `--toc` 超链接 |
| 页码 | Playwright 页脚模板 |

---

## 同类对比

目前 SkillHub 和 ClawHub 上有多个 Markdown → PDF 技能，各自选了不同的技术路线。**md2pdf 选择 Playwright（真实 Chromium 浏览器）**，在排版质量和安装体积之间走中间路线。

### 技术路线总览

| 技能 | 引擎 | 路线 |
|------|------|------|
| **md2pdf** | pandoc + Playwright/Chromium | 命令行解析 + 浏览器渲染 |
| [any2pdf](https://skillavatars.com/skills/lovstudio-any2pdf) | reportlab | 纯 Python 画 PDF |
| [md2pdf (Pandoc + Typst)](https://clawhub.ai/hansschinkenwurst78-dev/skills/openclaw-md2pdf) | Pandoc + Typst | 现代标记语言排版 |
| [md2pdf-weasyprint](https://skillhub.cn/skills/md2pdf-weasyprint) | WeasyPrint | Python CSS 排版 |
| [md2pdf-xelatex](https://skillhub.cn/skills/md2pdf-xelatex) | LaTeX xelatex | 学术排版引擎 |

### 能力对比

| 维度 | **md2pdf** | [any2pdf](https://skillavatars.com/skills/lovstudio-any2pdf) | [md2pdf (Typst)](https://clawhub.ai/hansschinkenwurst78-dev/skills/openclaw-md2pdf) | [md2pdf-weasyprint](https://skillhub.cn/skills/md2pdf-weasyprint) | [md2pdf-xelatex](https://skillhub.cn/skills/md2pdf-xelatex) |
|------|:---:|:---:|:---:|:---:|:---:|
| **引擎** | pandoc + Chromium | reportlab | Pandoc + Typst | WeasyPrint | LaTeX |
| **本体体积** | < 0.1 MB | < 0.1 MB | < 1 MB | < 1 MB | < 1 MB |
| **依赖体积** | ~225 MB | ~5 MB（纯 reportlab）<br>~300 MB（含 pandoc+TeX） | ~165 MB | ~80 MB | 150 MB ~ 4 GB |
| **代码高亮** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **CSS 灵活度** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ | ❌ |
| **中文/CJK** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **数学公式** | ⭐⭐⭐⭐ (KaTeX) | ❌ | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **图表/Mermaid** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **封面/目录/书签** | ✅ | ✅ | ✅ | ⭐ | ✅ |
| **多主题** | 2 套 | 12 套 | 模板定制 | ❌ | 模板定制 |
| **环境自检** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **页面诊断** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **学习成本** | 零（自然语言） | 低 | 低 | 低 | 高（需懂 LaTeX） |

### 为什么选 Chromium 路线？

- **WeasyPrint** 轻量但不支持 Flex/Grid 等现代 CSS，复杂表格和代码块易断裂
- **Typst** 新一代标记语言，速度快、数学公式强，但非 CSS 排版，样式定制受限于 Typst 语法
- **LaTeX** 排版最美但安装体积大、学习成本高，不适合"一句话生成 PDF"的 Skill 场景
- **reportlab** 最轻但需要手动处理每个渲染细节（代码换行、中文避头尾等）
- **Chromium** 在中间 —— 体积可控、CSS 完整支持、代码高亮与浏览器一致

---

## 许可

[MIT](LICENSE) © 2026 CoderMoray
