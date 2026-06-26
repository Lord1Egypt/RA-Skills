# 🧬 Nature Paper Hub

<p align="center">
  <img src="https://img.shields.io/badge/Nature_Journals-9_supported-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/OpenClaw-compatible-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Claude_Code-plugin-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Codex-compatible-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

<p align="center">
  <a href="#chinese">中文版</a> · <a href="#english">English</a>
</p>

---

<h2 id="chinese">🇨🇳 中文版</h2>

### 简介

`nature-paper-hub` 是一套面向 Nature 系列期刊投稿的全流程 AI 写作 agent，覆盖从**选刊、文献调研、论文起草、图表生成、引用核验、投稿前检查，到审稿意见回复**的完整链路。

支持 **OpenClaw、Claude Code、Codex** 三种平台，输出格式支持 **LaTeX（Overleaf）和 Word（.docx）**，并内置 CSV/Excel 自动生图、CrossRef 实时引用核验、个人文献库 RAG 写作风格锚定。

---

### 功能一览

| Skill | 功能说明 |
|-------|----------|
| 🏠 `nature-paper-hub` | 主入口，8 阶段全流程对话路由 |
| 📊 `nature-figure` | CSV/Excel → Nature 风格 matplotlib/R 图，自动识别图表类型 |
| 📖 `nature-reader` | PDF/DOI/arXiv → 双语精读 Markdown，含图表解读与引用建议 |
| 📚 `nature-citation` | CrossRef 实时核验 + RetractionWatch 撤稿检查 + BibTeX/RIS/ENW/Zotero 导出 |
| 🎞️ `nature-paper2ppt` | 论文 → 中文/双语 PPTX，含演讲者备注 |

---

### 支持的 Nature 子刊

| 期刊 | 影响因子 | 接收率 | 正文字数 | 图数 | 引用 |
|------|---------|--------|---------|------|------|
| Nature | 63.7 | ~8% | 3,000 | 6 | 30 |
| Nature Materials | 37.2 | ~9% | 3,000 | 6 | 50 |
| Nature Chemistry | 19.2 | ~9% | 3,000 | 6 | 50 |
| Nature Energy | 60.9 | ~8% | 3,000 | 6 | 50 |
| Nature Catalysis | 37.8 | ~8% | 3,000 | 6 | 50 |
| Nature Sustainability | 25.1 | ~10% | 4,000 | 8 | 60 |
| Nature Communications | 15.7 | ~20% | 5,000† | 10 | 60 |
| Nature Methods | 32.1 | ~8-10% | 3,000 | 6 | 50 |
| Nature Computational Science | 12.0 | ~12% | 5,000 | 8 | 60 |
| **Nature Chemical Engineering** | **13.0** | **~8%** | **3,500** | **6+10ED** | **50** |
| **Nature Machine Intelligence** | **23.9** | **~8%** | **3,500** | **6** | **50** |
| **Nature Synthesis** | **20.0** | **~8%** | **3,000** | **6‡** | **50** |

† Nature Communications 字数含 Methods 章节  
‡ Nature Synthesis 不接受 Scheme，只接受 Figure；Methods 中不可含图表

---

### 安装

#### 方式一：OpenClaw

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
cp -R nature-paper-hub ~/.openclaw/workspace/skills/
# 重启 OpenClaw，对话中说"选刊"即可激活
```

#### 方式二：Claude Code

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# 安装为用户级 subagents（全局可用）
mkdir -p ~/.claude/agents
cp nature-paper-hub/skills/nature-figure/SKILL.md ~/.claude/agents/nature-figure.md
cp nature-paper-hub/skills/nature-reader/SKILL.md ~/.claude/agents/nature-reader.md
cp nature-paper-hub/skills/nature-citation/SKILL.md ~/.claude/agents/nature-citation.md
cp nature-paper-hub/skills/nature-paper2ppt/SKILL.md ~/.claude/agents/nature-paper2ppt.md
cp nature-paper-hub/SKILL.md ~/.claude/agents/nature-paper-hub.md
```

或安装为项目级 subagents（仅当前项目可用）：
```bash
mkdir -p .claude/agents
cp nature-paper-hub/skills/*/SKILL.md .claude/agents/
```

安装完成后，在 Claude Code 中直接对话触发即可（无需额外命令）：
```
Use nature-figure to generate a matplotlib figure from my data.csv
```

#### 方式三：Codex

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# 创建 skills 目录（默认不存在）并安装
mkdir -p ~/.codex/skills
for d in nature-paper-hub/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done

# 验证安装
ls ~/.codex/skills/
# 重启 Codex 后生效
```

#### 安装 Python 依赖

```bash
pip install -r nature-paper-hub/scripts/requirements.txt
```

---

### 快速上手

#### OpenClaw / Telegram
在对话中输入以下关键词直接跳转对应阶段：

```
选刊         → 选择目标 Nature 子刊，显示字数/图数/引用限制
文献综述     → 调用个人文献库 + 网络搜索
写大纲       → 按子刊生成定制化论文结构
写摘要       → 起草符合 Nature 风格的 Abstract（150词）
图表规划     → 规划每张图的叙事逻辑
检查引用     → CrossRef 实时核验 + 撤稿检查
导出         → 选择 LaTeX（Overleaf）或 Word
写回复信     → 逐条审稿意见生成回复框架
```

#### Claude Code
```
Use nature-figure to generate a matplotlib figure from my data.csv
Use nature-reader to create a bilingual reader for this paper: ~/Downloads/paper.pdf
Use nature-citation to verify my reference list and export as BibTeX
Use nature-paper2ppt to convert this paper into a Chinese presentation
```

#### Codex
```
Use the nature-figure skill to plot my experimental results from data.xlsx
Use nature-reader to translate this Nature paper and ground each figure
Use nature-citation to find supporting references for oxygen evolution catalysis
```

---

### 全流程说明

```
阶段 0: 选刊           → 选目标子刊，加载对应字数/图数/引用限制
阶段 1: 文献调研       → LitReview 个人库 + CrossRef + 网络搜索
阶段 2: 结构规划       → 按期刊类型定制论文大纲
阶段 3: 逐节起草       → Abstract / Introduction / Results / Discussion / Methods
阶段 4: 图表生成       → CSV/Excel 自动出图 + matplotlib/R 代码 + 图例文字
阶段 5: 引用核验       → CrossRef API + RetractionWatch + 多格式导出
阶段 6: 投稿前检查     → 字数/图数/格式/内容完整 checklist
阶段 7: 导出           → LaTeX (Overleaf) / Word (.docx) / PPTX
阶段 8: 审稿回复       → 逐条回复框架 + 修改说明 + 封面信
```

---

### 文件结构

```
nature-paper-hub/
├── README.md                    # 本文件（中英双语）
├── SKILL.md                     # 主 skill（OpenClaw 入口）
├── skills/
│   ├── nature-figure/SKILL.md   # 科研绘图（自动识别 + matplotlib/R）
│   ├── nature-reader/SKILL.md   # 双语论文精读器
│   ├── nature-citation/SKILL.md # CrossRef 引用核验 + 多格式导出
│   └── nature-paper2ppt/SKILL.md# 论文转 PPT
├── templates/
│   ├── journal-specs.json       # 9个子刊规格数据
│   └── nature-latex.tex         # Overleaf LaTeX 模板
└── scripts/
    ├── auto_figure.py           # CSV/Excel → Nature 图（540行）
    ├── export_docx.py           # Word 导出
    ├── export_pptx.py           # PPT 导出
    └── requirements.txt         # Python 依赖
```

---

### 与同类项目对比

| 功能 | **nature-paper-hub** | Yuan1z0825/nature-skills | Boom5426/Nature-Paper-Skills |
|------|:---:|:---:|:---:|
| 9个子刊精确规格（字数/图/引用） | ✅ | ❌ | ✅ |
| 全流程单入口路由 | ✅ | ❌ | ✅ |
| LaTeX / Overleaf 模板 | ✅ | ❌ | ❌ |
| Word 导出（.docx） | ✅ | ❌ | ❌ |
| matplotlib/R 科研绘图代码 | ✅ | ✅ | ❌ |
| CSV/Excel → 自动生图 | ✅ | ❌ | ❌ |
| 双语论文精读器 | ✅ | ✅ | ❌ |
| 论文转 PPT（PPTX） | ✅ | ✅ | ❌ |
| 引用多格式导出（BibTeX/RIS/ENW/Zotero） | ✅ | ✅ | ❌ |
| CrossRef API 实时引用核验 | ✅ | ❌ | ❌ |
| RetractionWatch 撤稿检查 | ✅ | ❌ | ❌ |
| LitReview RAG 写作风格锚定 | ✅ | ❌ | ❌ |
| 个人文献库集成 | ✅ | ❌ | ❌ |
| Claude Code 插件 | ✅ | ✅ | ✅ |
| Codex 兼容 | ✅ | ✅ | ✅ |
| OpenClaw 兼容 | ✅ | ❌ | ❌ |

---

### 致谢

设计灵感部分来源于：
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)（上海交通大学袁一哲团队）
- [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

---

### 许可证

MIT License — 自由使用、修改和分发，保留原始署名即可。

---

### 贡献指南

欢迎提 Issue 和 PR！请说明：
1. 目标期刊
2. 功能缺口或 bug 描述
3. 建议实现方式

---
---

<h2 id="english">🇬🇧 English</h2>

### Introduction

`nature-paper-hub` is a full-pipeline AI writing agent for Nature-series journal submissions. It covers every stage from **journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission audit, to reviewer response**.

Compatible with **OpenClaw, Claude Code, and Codex**. Outputs **LaTeX (Overleaf-ready) and Word (.docx)**. Features include automatic figure generation from CSV/Excel, CrossRef real-time citation verification, and RAG-enhanced writing style grounded in your personal literature library.

---

### Features

| Skill | Description |
|-------|-------------|
| 🏠 `nature-paper-hub` | Main hub with 8-stage conversational pipeline routing |
| 📊 `nature-figure` | CSV/Excel → Nature-style matplotlib/R figures with auto chart-type detection |
| 📖 `nature-reader` | PDF/DOI/arXiv → bilingual annotated Markdown with figure grounding and citation suggestions |
| 📚 `nature-citation` | CrossRef real-time verification + RetractionWatch check + BibTeX/RIS/ENW/Zotero export |
| 🎞️ `nature-paper2ppt` | Paper → Chinese/bilingual PPTX with presenter notes |

---

### Supported Journals

| Journal | IF | Accept | Words | Figs | Refs |
|---------|:---:|:---:|:---:|:---:|:---:|
| Nature | 63.7 | ~8% | 3,000 | 6 | 30 |
| Nature Materials | 37.2 | ~9% | 3,000 | 6 | 50 |
| Nature Chemistry | 19.2 | ~9% | 3,000 | 6 | 50 |
| Nature Energy | 60.9 | ~8% | 3,000 | 6 | 50 |
| Nature Catalysis | 37.8 | ~8% | 3,000 | 6 | 50 |
| Nature Sustainability | 25.1 | ~10% | 4,000 | 8 | 60 |
| Nature Communications | 15.7 | ~20% | 5,000† | 10 | 60 |
| Nature Methods | 32.1 | ~8-10% | 3,000 | 6 | 50 |
| Nature Computational Science | 12.0 | ~12% | 5,000 | 8 | 60 |
| **Nature Chemical Engineering** | **13.0** | **~8%** | **3,500** | **6+10ED** | **50** |
| **Nature Machine Intelligence** | **23.9** | **~8%** | **3,500** | **6** | **50** |
| **Nature Synthesis** | **20.0** | **~8%** | **3,000** | **6‡** | **50** |

† Nature Communications word count includes Methods section  
‡ Nature Synthesis does not accept Schemes — figures only; Methods section cannot contain figures or tables

---

### Installation

#### Option 1: OpenClaw

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git
cp -R nature-paper-hub ~/.openclaw/workspace/skills/
# Restart OpenClaw. Say "选刊" or "choose journal" to activate.
```

#### Option 2: Claude Code

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# Install as user-level subagents (available in all projects)
mkdir -p ~/.claude/agents
cp nature-paper-hub/skills/nature-figure/SKILL.md ~/.claude/agents/nature-figure.md
cp nature-paper-hub/skills/nature-reader/SKILL.md ~/.claude/agents/nature-reader.md
cp nature-paper-hub/skills/nature-citation/SKILL.md ~/.claude/agents/nature-citation.md
cp nature-paper-hub/skills/nature-paper2ppt/SKILL.md ~/.claude/agents/nature-paper2ppt.md
cp nature-paper-hub/SKILL.md ~/.claude/agents/nature-paper-hub.md
```

Or install as project-level subagents (current project only):
```bash
mkdir -p .claude/agents
cp nature-paper-hub/skills/*/SKILL.md .claude/agents/
```

Once installed, trigger naturally in conversation — no extra commands needed:
```
Use nature-figure to generate a matplotlib figure from my data.csv
```

#### Option 3: Codex

```bash
git clone https://github.com/Yang1Bai/nature-paper-hub.git

# Create skills directory (does not exist by default) and install
mkdir -p ~/.codex/skills
for d in nature-paper-hub/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done

# Verify installation
ls ~/.codex/skills/
# Restart Codex to pick up new skills.
```

#### Install Python dependencies

```bash
pip install -r nature-paper-hub/scripts/requirements.txt
```

---

### Quick Start

#### OpenClaw / Telegram
Say any of these in conversation to jump to that stage:

```
选刊 / choose journal    → Select target journal; see word/figure/ref limits
文献综述 / literature    → Search personal library + CrossRef + web
写大纲 / outline         → Generate journal-specific manuscript structure
写摘要 / abstract        → Draft Nature-style Abstract (150 words)
图表规划 / figure plan   → Plan figure narrative logic
检查引用 / citations     → CrossRef verify + retraction check
导出 / export            → LaTeX (Overleaf) or Word
写回复信 / rebuttal      → Point-by-point reviewer response framework
```

#### Claude Code
```
Use nature-figure to generate a matplotlib figure from my data.csv
Use nature-reader to create a bilingual reader for this paper: ~/Downloads/paper.pdf
Use nature-citation to verify my reference list and export as BibTeX
Use nature-paper2ppt to convert this paper into a Chinese presentation
```

#### Codex
```
Use the nature-figure skill to plot my experimental results from data.xlsx
Use nature-reader to translate this Nature paper and ground each figure
Use nature-citation to find supporting references for oxygen evolution catalysis
```

---

### Full Pipeline

```
Stage 0: Journal Selection    → Choose sub-journal; load word/figure/ref limits
Stage 1: Literature Review    → Personal library + CrossRef + web search
Stage 2: Outline Planning     → Journal-tailored manuscript structure
Stage 3: Section Drafting     → Abstract / Intro / Results / Discussion / Methods
Stage 4: Figure Generation    → Auto-plot from CSV/Excel + matplotlib/R code + legend text
Stage 5: Citation Check       → CrossRef API + RetractionWatch + multi-format export
Stage 6: Pre-submission Audit → Word count / figure count / format / content checklist
Stage 7: Export               → LaTeX (Overleaf) / Word (.docx) / PPTX
Stage 8: Reviewer Response    → Point-by-point reply + change summary + cover letter
```

---

### Repository Structure

```
nature-paper-hub/
├── README.md                    # This file (bilingual CN/EN)
├── SKILL.md                     # Main skill (OpenClaw entry point)
├── skills/
│   ├── nature-figure/SKILL.md   # Figure generation (auto-detect + matplotlib/R)
│   ├── nature-reader/SKILL.md   # Bilingual paper reader
│   ├── nature-citation/SKILL.md # CrossRef citation verification + multi-format export
│   └── nature-paper2ppt/SKILL.md# Paper to presentation
├── templates/
│   ├── journal-specs.json       # Per-journal specs (9 journals)
│   └── nature-latex.tex         # Overleaf-ready LaTeX template
└── scripts/
    ├── auto_figure.py           # CSV/Excel → Nature figure (540 lines)
    ├── export_docx.py           # Word export
    ├── export_pptx.py           # PPTX export
    └── requirements.txt         # Python dependencies
```

---

### Comparison with Similar Projects

| Feature | **nature-paper-hub** | Yuan1z0825/nature-skills | Boom5426/Nature-Paper-Skills |
|---------|:---:|:---:|:---:|
| Per-journal word/figure/ref limits (9 journals) | ✅ | ❌ | ✅ |
| Single-entry full-pipeline routing | ✅ | ❌ | ✅ |
| LaTeX / Overleaf template | ✅ | ❌ | ❌ |
| Word export (.docx) | ✅ | ❌ | ❌ |
| matplotlib/R figure code generation | ✅ | ✅ | ❌ |
| CSV/Excel → auto figure | ✅ | ❌ | ❌ |
| Bilingual paper reader | ✅ | ✅ | ❌ |
| Paper to PPTX presentation | ✅ | ✅ | ❌ |
| Multi-format citation export (BibTeX/RIS/ENW/Zotero) | ✅ | ✅ | ❌ |
| CrossRef API real-time citation verification | ✅ | ❌ | ❌ |
| RetractionWatch retraction check | ✅ | ❌ | ❌ |
| RAG writing style grounded in personal library | ✅ | ❌ | ❌ |
| Personal literature library integration | ✅ | ❌ | ❌ |
| Claude Code plugin | ✅ | ✅ | ✅ |
| Codex compatible | ✅ | ✅ | ✅ |
| OpenClaw compatible | ✅ | ❌ | ❌ |

---

### Acknowledgements

Inspired in part by:
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) — Yuan Yizhe, Shanghai Jiao Tong University
- [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)
- [Nature Portfolio Author Guidelines](https://www.nature.com/authors)

---

### License

MIT License — free to use, modify, and distribute with attribution.

---

### Contributing

Issues and PRs are welcome. Please include:
1. Target journal
2. Feature gap or bug description
3. Suggested implementation approach
