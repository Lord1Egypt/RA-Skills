# 🔍 novel-bug-checker

> **Publication-Grade Novel Quality Inspector · AI-Powered Narrative Bug Detection Tool**
>
> A professional OpenClaw skill for auditing Chinese novel narrative quality — detecting logic flaws, character inconsistencies, pacing issues, and narrative bugs with graded reports and actionable repair suggestions.

<p align="center">
  <picture>
    <media name="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="novel-bug-checker banner" width="800">
  </picture>
</p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_EN.md">English</a>
</p>

<p align="center">
  <a href="https://clawhub.ai/USER/skills/novel-bug-checker"><img src="https://img.shields.io/badge/ClawHub-v1.0.0-7b2ff7?style=flat-square" alt="ClawHub"></a>
  <a href="https://github.com/USER/novel-bug-checker"><img src="https://img.shields.io/badge/GitHub-open-2ea44f?style=flat-square" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT"></a>
</p>

---

## 🌟 Why novel-bug-checker?

| Dimension | Manual Review | **novel-bug-checker** |
|-----------|--------------|----------------------|
| 🎯 Coverage | Relies on personal experience, easy to miss | **Systematic scan**: Logic / Characters / Pacing / Foreshadowing |
| 📊 Reporting | Oral feedback, unquantifiable | **Graded reports**: 🔴Critical / 🟠Major / 🟡Medium / 🟢Minor |
| 🔧 Fix Suggestions | Must think for yourself | **Strategy-driven**: ≥3 repair plans per bug |
| 🧠 Theory | Intuition-based | **Narratology-backed**: timelines, causality, character arcs, info density |
| 📝 Scripts | None | **3 Python scripts**: logic / pacing / consistency analysis |
| 🔄 Verification | Can't re-check | **Repair validation**: auto-recheck after modifications |

---

## ✨ Key Features

### 🕵️ Logic Flaw Detection
- **Timeline contradictions**: event ordering, time calculations, causal sequences
- **Broken causality**: missing prerequisites for major plot turns
- **Ability mutation**: unexplained power jumps, inconsistent power systems
- **Unreasonable knowledge**: characters knowing things they shouldn't

### 👤 Character Consistency Check
- **Personality shifts**: behavior changes without motivation
- **Motivation conflicts**: goals vs actions misalignment
- **Dialogue drift**: speech patterns inconsistent with background
- **Broken character arcs**: development lacking necessary experiences

### 📈 Pacing & Structure Analysis
- **Information density**: detect overloaded or sparse passages
- **Climax buildup**: tension accumulation before high points
- **Scene transitions**: evaluate smoothness and natural flow
- **Foreshadowing management**: track setup vs payoff

### 🔄 Repair Validation
Submit revised text for automatic rechecking. Compare before/after reports, highlighting fixed issues and new problems.

---

## 📖 Quick Start

### Install

```bash
# Via OpenClaw
openclaw skills install novel-bug-checker

# Via ClawHub CLI
clawhub install novel-bug-checker
```

### Install Dependencies

```bash
pip install jieba
```

> Only requires `jieba` (Chinese word segmentation) — lightweight, no heavy NLP libraries.

### Start an Audit

Tell your AI: **"Check this novel chapter for logic flaws"** or paste your text directly.

The AI will automatically:
1. Read text → 2. Logic analysis → 3. Character consistency → 4. Pacing analysis → 5. Graded report

### CLI Mode (Optional)

```bash
# Logic analysis
python scripts/logic-analyzer.py novel.txt -o report.txt

# Pacing analysis
python scripts/rhythm-analyzer.py novel.txt -g 玄幻

# Character consistency
python scripts/consistency-checker.py novel.txt -o report.txt
```

---

## 🏗️ Project Structure

```
novel-bug-checker/
├── SKILL.md                          # Core skill definition
├── README.md                         # This file (Chinese)
├── assets/                           # Assets
│   ├── banner-light.svg
│   └── banner-dark.svg
├── references/                       # Knowledge base
│   ├── bug-patterns.md               # Bug pattern classification
│   ├── character-consistency.md      # Character consistency guide
│   ├── narrative-theory.md           # Narratology foundations
│   └── repair-strategies.md          # Repair strategy library
├── scripts/                          # Analysis tools
│   ├── logic-analyzer.py             # Logic flaw analyzer
│   ├── rhythm-analyzer.py            # Pacing analyzer
│   └── consistency-checker.py        # Character consistency checker
├── templates/                        # Output templates
│   ├── bug-report.txt                # Bug report template
│   ├── repair-suggestions.txt        # Repair suggestions template
│   └── summary-report.txt            # Summary report template
└── example.md                        # Usage examples
```

---

## 🎯 Use Cases

- ✅ **Web/Serial Novels**: Xianxia, Urban, Mystery — comprehensive large-architecture audits
- ✅ **Literary Fiction**: Ensure publication-grade narrative quality
- ✅ **Serialized Works**: Quality control before chapter release
- ✅ **Final Revisions**: Exhaustive bug sweep before publication
- ✅ **Writing Education**: Case-driven narrative analysis training

---

## 📦 Tech Stack

- **Runtime**: OpenClaw AI Agent + Python 3
- **Core Dependency**: jieba (Chinese word segmentation)
- **Formats**: Markdown + Python + TXT
- **License**: MIT

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/USER">USER</a><br>
  <sub>Quality assurance for every novel written with care</sub>
</p>
