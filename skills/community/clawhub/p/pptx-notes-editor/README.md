# PPTX Notes Editor - Agent Skill

An agent skill for editing PowerPoint speaker notes directly in PPTX XML. Works with **Claude Code**, **OpenClaw**, and any AI agent that supports the SKILL.md standard.

> [中文文档](#中文说明)

## Why This Skill?

Most PPTX tools focus on **creating slides**. This skill focuses exclusively on **editing speaker notes** — the text presenters read while presenting.

**Unique capabilities you won't find elsewhere:**
- Slide-to-notes mapping detection (`notesSlide3.xml` may NOT be slide 3!)
- Multiple rewriting styles: narrative, concise, verbatim, or custom
- Reads the entire PPT first for contextual, coherent notes
- Page-by-page interactive confirmation — nothing is modified without your approval

## Features

- **Unpack/Pack PPTX** - Decompress PPTX to XML, edit, and repack
- **Slide-Notes Mapping** - Automatically detect slide-to-notesSlide correspondence
- **Style Selection** - Choose narrative, concise bullet points, verbatim script, or custom style
- **Global Context** - Reads entire PPT before writing notes for coherent flow
- **Interactive Confirmation** - Shows draft, waits for your approval before any modification
- **Export to Markdown** - Batch export all notes with slide titles
- **XML-Safe Editing** - Handles XML escaping (`& < > "`) correctly

## Install

### Claude Code

```bash
# One-line install (Recommended)
mkdir -p ~/.claude/skills/pptx-notes-editor && curl -fsSL https://raw.githubusercontent.com/cm8421/pptx-notes-editor/main/SKILL.md -o ~/.claude/skills/pptx-notes-editor/SKILL.md

# Or via skills CLI
npx skills add cm8421/pptx-notes-editor
```

### OpenClaw

```bash
/skill install @cm8421/pptx-notes-editor
```

### Any Agent (Manual)

```bash
git clone https://github.com/cm8421/pptx-notes-editor.git
# Copy SKILL.md to your agent's skill directory
```

## Usage

Simply describe what you want to do with your PPTX notes:

```
> Help me edit the speaker notes in my-presentation.pptx
> Rewrite the notes in my-presentation.pptx to be more conversational
> Export the notes from my-presentation.pptx to markdown
```

## Workflow

```
Select Style → Read Entire PPT → Page-by-Page Draft → Confirm → Modify XML → Pack → Verify
```

The skill will:
1. Ask you to select page range, notes style, and language
2. Read through all slides to understand the narrative arc
3. For each page: show slide content + current notes → generate draft → **wait for your confirmation**
4. Pack modified PPTX and verify

### Key Insight: Slide numbers ≠ Notes numbers

`notesSlide3.xml` may NOT correspond to slide 3! The mapping is stored in `_rels/slide3.xml.rels`.

## Requirements

- `unzip` / `zip` (standard on macOS/Linux)
- An AI agent that supports SKILL.md (Claude Code, OpenClaw, etc.)

## License

MIT

---

<a id="中文说明"></a>

## 中文说明

### 为什么需要这个 Skill？

市面上的 PPTX 工具都专注于**创建幻灯片**。这个 Skill 专注于**编辑演讲备注** — 演讲者在演示时阅读的文字。

**独特的功能：**
- 自动检测幻灯片与备注的映射关系（编号可能不对应！）
- 支持多种风格：叙事风格、精简要点、逐字稿、自定义
- 先通读整个PPT再逐页设计备注，保证上下文连贯
- 逐页交互确认 — 未经你确认不做任何修改

### 安装

**Claude Code：**
```bash
mkdir -p ~/.claude/skills/pptx-notes-editor && curl -fsSL https://raw.githubusercontent.com/cm8421/pptx-notes-editor/main/SKILL.md -o ~/.claude/skills/pptx-notes-editor/SKILL.md
```

**OpenClaw：**
```bash
/skill install @cm8421/pptx-notes-editor
```

### 使用

```
> 帮我编辑 my-presentation.pptx 的演讲备注
> 用叙事风格重写备注
> 把备注导出为 Markdown
```

### 工作流程

```
选择风格 → 通读全文 → 逐页生成草稿 → 确认 → 修改XML → 打包 → 验证
```
