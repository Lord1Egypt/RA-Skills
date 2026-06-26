[English](README.md) | **中文**

# Paper to Slides

一个 AI Skill，深度研读学术论文并生成精美的 HTML 演示文稿——给它一篇 PDF 或 arXiv 链接，返回结构化研读报告和可直接汇报的 slide deck。

**理念：** 读论文应该产出可复用的成果物，而不仅仅是"读过了"。一条命令，同时获得深度分析和演示文稿。

## 你会得到什么

给 skill 一篇论文（本地 PDF、arXiv 链接或任意 PDF URL），它会产出：

- **研读报告** — 双模式深度解析：Part A 是完整学术分析（结构化摘要→方法论→实验→讨论），Part B 将核心逻辑链提炼为一句话总结
- **HTML 演示文稿** — 零依赖、带动画的演示文稿，10 种风格预设，支持浏览器内编辑，响应式设计适配任何屏幕

两种输出可以单独使用，也可以一起生成。

## 快速开始

1. 在你的 agent 中安装此 skill（OpenClaw 或 Claude Code）
2. 说"读这篇论文然后做成 slides"，附上 PDF 路径或 arXiv 链接
3. Agent 自动处理一切——提取、分析、选风格、生成

```
解析 https://arxiv.org/abs/2603.02096，组会汇报，亮色，15页左右
```

```
深度研读 /path/to/paper.pdf，生成报告和slides，暗色主题
```

未指定 slides 参数时 agent 会询问用途、页数、主题风格和是否需要编辑功能。也可以一次性指定跳过提问。

## 风格预览

内置 10 种风格预设。[打开在线预览 →](style-preview.html)

### 亮色主题

| Swiss Modern ⭐ | Notebook Tabs | Pastel Geometry |
|:---:|:---:|:---:|
| ![Swiss Modern](style-examples/swiss-modern.png) | ![Notebook Tabs](style-examples/notebook-tabs.png) | ![Pastel Geometry](style-examples/pastel-geometry.png) |
| 干净精确，学术默认 | 笔记本质感，编辑风 | 友好亲和，柔和 |

| Split Pastel | Vintage Editorial | Paper & Ink |
|:---:|:---:|:---:|
| ![Split Pastel](style-examples/split-pastel.png) | ![Vintage Editorial](style-examples/vintage-editorial.png) | ![Paper & Ink](style-examples/paper-ink.png) |
| 活泼创意，双色分割 | 复古杂志，有态度 | 文学编辑，深思熟虑 |

### 暗色主题

| Bold Signal | Neon Cyber | Dark Botanical | Terminal Green |
|:---:|:---:|:---:|:---:|
| ![Bold Signal](style-examples/bold-signal.png) | ![Neon Cyber](style-examples/neon-cyber.png) | ![Dark Botanical](style-examples/dark-botanical.png) | ![Terminal Green](style-examples/terminal-green.png) |
| 高冲击力，自信 | 赛博科技，未来感 | 优雅高级，艺术感 | 黑客极客，终端风 |

## 安装

### OpenClaw

```bash
# 从 ClawHub 安装（即将上线）
clawhub install paper-to-slides

# 或手动安装
git clone https://github.com/zhangguanghao523/paper-to-slides.git ~/.openclaw/skills/paper-to-slides
```

### Claude Code

```bash
git clone https://github.com/zhangguanghao523/paper-to-slides.git ~/.claude/skills/paper-to-slides
```

### 系统依赖

Skill 需要 `pdftotext` 来提取 PDF 文本：

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt install poppler-utils
```

完成。不需要 Python 包、npm 或构建工具。生成的 slides 是纯 HTML + 内联 CSS/JS。

## 架构

此 skill 采用**渐进式加载** —— 主文件 `SKILL.md` 是精简的工作流地图，支撑文件按需加载：

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `SKILL.md` | 核心两阶段工作流 | 始终（skill 调用时） |
| `prompts/part-a-template.md` | Part A 深度学术报告模板 | 阶段一（撰写报告） |
| `prompts/part-b-template.md` | Part B 核心逻辑提炼模板 | 阶段一（撰写报告） |
| `prompts/slide-styles.md` | 10 种视觉风格预设 | 阶段二（选择风格） |
| `prompts/slide-template.md` | HTML 架构、视口 CSS、JS 控制器 | 阶段二（生成 slides） |

## 技术依赖

| 组件 | 作用 |
|------|------|
| [paper-parse](https://clawhub.com) | 双模式报告模板（Part A + Part B） |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 零依赖 HTML 演示框架 |
| [poppler](https://poppler.freedesktop.org/) | PDF 文本与图表提取（pdftotext / pdftoppm） |

## 环境要求

- AI agent（OpenClaw、Claude Code 或类似工具）
- `pdftotext`（来自 poppler）—— 用于 PDF 文本提取
- 网络连接（下载 arXiv 论文和加载 Google Fonts）

## 致谢

基于 [OpenClaw](https://github.com/openclaw/openclaw) 构建。演示引擎改编自 [@zarazhangrui](https://github.com/zarazhangrui) 的 [frontend-slides](https://github.com/zarazhangrui/frontend-slides)。报告模板改编自 [paper-parse](https://clawhub.com)。

## 许可证

MIT — 使用、修改、分享，随你。
