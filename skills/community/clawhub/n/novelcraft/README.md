# NovelCraft

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Fully autonomous book author for OpenClaw — creates complete novels from idea to finished PDF/EPUB using AI subagents.**

NovelCraft uses a **modular configuration system** with automatic **review workflow** and **scoring** for quality assurance.

---

## ✨ Features

- 🚀 **Fully Autonomous** — Complete novels with minimal input
- 📝 **Sequential Chapter Writing** — One chapter at a time for quality
- 🎯 **Automatic Review System** — Score-based quality control
- 📊 **Scoring Matrix** — Weighted criteria, automatic decisions
- 🎨 **Optional Images** — Character portraits, settings, covers, **chapter images**
- 📚 **Multiple Formats** — PDF (LaTeX), EPUB, Markdown
- 📁 **Draft/Approved Folders** — Quality separation
- ⚙️ **Standardized Config Schema v3.2** — Clear 3-level hierarchy
- 👥 **Target Audience Profiles** — **NEW:** Auto-configure for age groups (6-8, 8-12, 12-16, 16-25, 25+, 60+)
- 🔁 **Max 3 Revisions** — Forced rewrite if needed
- 🤖 **Subagent Architecture** — Each module runs isolated

---

## 🚀 Quick Start

### 1. Create Configs in Workspace

```bash
mkdir -p ~/.openclaw/workspace/novelcraft/config
# Copy module configs from SKILL.md examples
```

### 2. Create Project

```bash
mkdir -p ~/.openclaw/workspace/novelcraft/Books/projects/my-novel
# Create project-manifest.md from template
```

### 3. Start NovelCraft

Tell OpenClaw: *"Starte NovelCraft für mein Buch 'Mein Roman'"*

---

## 📁 Directory Structure

### Workspace (Project Data)
```
~/.openclaw/workspace/novelcraft/
├── config/                              # 5 Module Configs
│   ├── CONFIG-SCHEMA.md                 # Schema documentation v3.0
│   ├── PROJECT-MANIFEST-TEMPLATE.md     # Project template
│   ├── module-concept.md
│   ├── module-writer-extras.md
│   ├── module-images.md
│   ├── module-chapters.md
│   └── module-publication.md
│
└── Books/projects/novel-[TITLE]/
    ├── project-manifest.md              # Central status file
    ├── 00-concept/                      # Concept, characters, world
    ├── 01-drafts/                       # WIP: Drafts, Reviews, Revisions
    │   ├── chapter_01_draft.md
    │   ├── chapter_01_review.md
    │   └── chapter_01_review_v2.md
    ├── 02-chapters/                     # ✅ APPROVED chapters only
    │   ├── chapter_01.md
    │   └── chapter_02.md
    └── 03-final/                        # PDF, EPUB
```

### Skill (Templates & Docs)
```
~/.openclaw/skills/novelcraft/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── templates/                           # 7 Module Templates
│   ├── module-concept-template.md
│   ├── module-writer-extras-template.md
│   ├── module-images-template.md
│   ├── module-chapters-template.md
│   ├── module-review-template.md
│   ├── module-revision-template.md
│   └── module-publication-template.md
└── references/
    └── CONFIG.md                        # Config documentation
```

---

## 🔄 Workflow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Concept   │───→│ Writer       │───→│   Images    │───→│  Chapters   │───→│ Writer       │───→│ Publication │
│             │    │ Extras       │    │  (parallel) │    │  (sequential│    │ Extras       │    │             │
│             │    │ (Prolog)     │    │             │    │  with Review│    │ (Epilog)     │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
```

---

## ⚙️ Configuration Schema v3.0

### 3-Level Hierarchy

| Level | Name | Location | Purpose | Override |
|-------|------|----------|---------|----------|
| 1 | Hardcoded | Skill code | Fallback defaults | — |
| 2 | Module Configs | `workspace/config/module-*.md` | Technical settings | Level 1 |
| 3 | Project Manifest | `workspace/Books/projects/{PROJECT}/project-manifest.md` | Book-specific | Level 1+2 |
| **4** | **Target Audience** | `workspace/config/module-target-audience.md` | **NEW:** Auto-configure all | **All levels** |

**Rule:** Higher level wins. Target Audience profile auto-configures all modules.

### Modules

| # | Module | Type | Description |
|---|--------|------|-------------|
| 0 | **Target Audience** | Optional | **NEW:** Auto-configure for age profile |
| 1 | **Concept** | Required | Genre, plot, characters, world |
| 2 | **Writer Extras** | Optional | Prolog & Epilog |
| 3 | **Images** | Optional | Cover, characters, settings, chapter images |
| 4 | **Chapters** | Required | Sequential writing with review |
| 5 | **Publication** | Required | PDF/EPUB creation |

---

## ✅ Review System

### Automatic Scoring

| Criterion | Weight | Description |
|-----------|--------|-------------|
| UTF-8 Encoding | ×3 (CRITICAL) | No foreign characters |
| Word Count 7000-8000 | ×2 (HIGH) | Target: 7500 words |
| Continuity | ×2 (HIGH) | Consistent with previous chapter |
| Plot Progression | ×2 (HIGH) | Story develops |
| Character Voice | ×1.5 (MEDIUM) | Believable characters |
| Style & Atmosphere | ×1.5 (MEDIUM) | Fits project style |
| Grammar | ×1 (LOW) | Correct language |

### Decisions

| Score | Decision | Action |
|-------|----------|--------|
| 8.0-10.0 | ✅ **APPROVED** | Copy to `02-chapters/`, next chapter |
| 6.0-7.9 | ⚠️ **MINOR_REVISION** | Specific fixes, max 3 attempts |
| 4.0-5.9 | 🔧 **MAJOR_REVISION** | Major rewrite, max 3 attempts |
| 0.0-3.9 | ❌ **REJECTED** | Complete rewrite, max 3 attempts |

**After 3 revisions:** Forced rewrite

---

## 📋 Important Rules

- ✅ **Only one chapter at a time** — Strictly sequential
- ✅ **Never block on images** — Proceed to chapters immediately
- ✅ **Autonomous = no questions** — Runs through
- ✅ **Publication reads only 02-chapters/** — No drafts
- ✅ **Max 3 revisions** — Then forced rewrite

---

## 📚 Documentation

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill documentation |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | Contribution guidelines |
| `references/CONFIG.md` | Complete config docs |
| `templates/*.md` | Module templates |
| `workspace/config/CONFIG-SCHEMA.md` | Schema v3.0 |
| `workspace/config/PROJECT-MANIFEST-TEMPLATE.md` | Project template |

---

## 🔧 Requirements

- OpenClaw with ACP support
- pandoc (EPUB/PDF)
- xelatex (optional, enhanced PDF)
- Image provider (optional)

---

## 📜 License

MIT License — see LICENSE file

---

**Maintained by:** Felix (AI) with Ronny (User) 🧠💡

*NovelCraft 3.2 — Target Audience Profiles, Enhanced Images, Quality-first*
