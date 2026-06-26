# Paper Analyzer（论文分析器）

Paper Analyzer 可以把论文链接、PDF 或粘贴的论文内容，转换成严谨的研究报告；在需要时，还能生成方法架构图。

默认情况下，它会完整阅读论文并写出英文 Markdown 报告。如果用户指定中文或其他语言，报告和图示标签会继承该语言。如果用户要求画图、架构图、HTML/SVG/PNG 输出，或指定暗色/亮色主题，它会额外生成出版级风格的方法图。

## 功能

- 读取 arXiv HTML、PDF、附件或粘贴的论文文本。
- 生成结构化 Markdown 报告，覆盖元信息、问题动机、技术方法、实验证据、批判性评估和综合结论。
- 对重要判断标注 `[paper]`、`[inferred]` 或 `[external]`，避免把推断说成事实。
- 生成 HTML、SVG、PNG 或全部格式的方法架构图。
- 支持暗色和亮色图示主题。
- 支持英文和中文报告/图示输出。

## 默认行为

没有画图指令时，仍然会写报告：

```text
Read this paper: https://arxiv.org/abs/2601.05242
```

预期输出：

- `outputs/{paper_shortname}_report.md`

## 画图行为

当用户表达视觉意图，或传入图示相关 flag 时，会触发制图：

```text
阅读这篇论文并画出方法架构图：https://arxiv.org/abs/2601.05242
```

默认图示输出：

- 图示语言继承报告语言
- 暗色主题
- HTML 格式

## 常用 Flags

| Flag | 示例 | 作用 |
|---|---|---|
| `--lang cn` | `--lang cn` | 生成中文报告，并默认生成中文图示标签。 |
| `--cn` | `--cn` | 中文输出的简写。 |
| `--draw-structure` | `--draw-structure` | 生成方法架构图。 |
| `--output` | `--output all` | 选择 `html`、`svg`、`png` 或 `all`；该 flag 会隐式触发制图。 |
| `--bg-theme` | `--bg-theme light` | 选择 `dark` 或 `light` 图示主题。 |
| `--showcase-language` | `--showcase-language en` | 单独覆盖图示语言，不影响报告语言。 |

## 示例

只生成英文报告：

```text
Analyze https://arxiv.org/abs/2601.05242
```

生成中文报告和中文暗色 HTML 图：

```text
用中文读这篇论文并画架构图：https://arxiv.org/abs/2601.05242
```

生成英文报告和亮色 SVG 图：

```text
Read this paper and create a diagram --bg-theme light --output svg https://arxiv.org/abs/2601.05242
```

中文报告，但图示使用英文：

```text
中文报告，图用英文 --showcase-language en --draw-structure https://arxiv.org/abs/2601.05242
```

## 输出文件

主报告：

- `/mnt/user-data/outputs/{paper_shortname}_report.md`
- 如果 `/mnt/user-data/outputs/` 不可用，则回退到当前 workspace 的 `outputs/` 目录。

图示文件：

- `{paper_shortname}_architecture.html`
- `{paper_shortname}_architecture.svg`
- `{paper_shortname}_architecture.png`
- 亮色主题在可能同时输出多主题时，可使用 `_light` 后缀。

## ClawHub 简介

**中文：** Paper Analyzer 是一个面向 Codex 的论文深度阅读 Skill。它可以读取 arXiv、PDF 或粘贴的论文内容，生成严谨的 Markdown 评审报告，并可绘制暗色或亮色主题的方法架构图。

**English:** Paper Analyzer is a research-paper deep reading skill for Codex. It reads papers from arXiv, PDFs, or pasted text, writes a rigorous Markdown review, and can generate polished method diagrams in dark or light themes.
