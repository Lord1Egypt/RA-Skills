# Paper Analyzer

Paper Analyzer turns a paper link, PDF, or pasted paper text into a rigorous research report and, when requested, a method diagram.

By default, it reads the full paper and writes an English Markdown report. If the user asks for another language, the report and diagram labels inherit that language. If the user asks for a diagram, architecture view, HTML/SVG/PNG output, or a dark/light theme, it also generates a publication-style architecture diagram.

## What It Does

- Reads arXiv HTML, PDFs, attachments, or pasted paper content.
- Produces a structured Markdown report with metadata, motivation, method, evidence, critique, and synthesis.
- Tags substantive claims as `[paper]`, `[inferred]`, or `[external]`.
- Creates method diagrams in HTML, SVG, PNG, or all formats.
- Supports dark and light diagram themes.
- Supports English and Chinese report/diagram output.

## Default Behavior

Without diagram instructions, the skill still writes a report:

```text
Read this paper: https://arxiv.org/abs/2601.05242
```

Expected output:

- `outputs/{paper_shortname}_report.md`

## Diagram Behavior

Diagram output is triggered by visual intent or by diagram flags:

```text
Read this paper and draw the method architecture: https://arxiv.org/abs/2601.05242
```

Default diagram output:

- English labels unless the report language is changed
- Dark theme
- HTML format

## Useful Flags

| Flag | Example | Effect |
|---|---|---|
| `--lang cn` | `--lang cn` | Generate Chinese report and Chinese diagram labels by default. |
| `--cn` | `--cn` | Shorthand for Chinese output. |
| `--draw-structure` | `--draw-structure` | Generate a method diagram. |
| `--output` | `--output all` | Choose `html`, `svg`, `png`, or `all`; implies diagram generation. |
| `--bg-theme` | `--bg-theme light` | Choose `dark` or `light` diagram theme. |
| `--showcase-language` | `--showcase-language en` | Override diagram label language separately from the report. |

## Examples

English report only:

```text
Analyze https://arxiv.org/abs/2601.05242
```

Chinese report and Chinese dark HTML diagram:

```text
用中文读这篇论文并画架构图：https://arxiv.org/abs/2601.05242
```

English report with light SVG diagram:

```text
Read this paper and create a diagram --bg-theme light --output svg https://arxiv.org/abs/2601.05242
```

Chinese report with English diagram:

```text
中文报告，图用英文 --showcase-language en --draw-structure https://arxiv.org/abs/2601.05242
```

## Output Files

Primary report:

- `/mnt/user-data/outputs/{paper_shortname}_report.md`
- Falls back to workspace `outputs/` if `/mnt/user-data/outputs/` is unavailable.

Diagram files:

- `{paper_shortname}_architecture.html`
- `{paper_shortname}_architecture.svg`
- `{paper_shortname}_architecture.png`
- Light theme outputs may use `_light` suffix when both themes could be produced.

## ClawHub Introduction

**English:** Paper Analyzer is a research-paper deep reading skill for Codex. It reads papers from arXiv, PDFs, or pasted text, writes a rigorous Markdown review, and can generate polished method diagrams in dark or light themes.

**中文：** Paper Analyzer 是一个面向 Codex 的论文深度阅读 Skill。它可以读取 arXiv、PDF 或粘贴的论文内容，生成严谨的 Markdown 评审报告，并可绘制暗色或亮色主题的方法架构图。
