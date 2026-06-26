# KDP Author Engine 📖

**Write, Publish, and Market Books on Amazon with a 6-Agent AI Pipeline.**

From market research to bestseller ranking. 6 specialized agents. Human-in-the-loop at every gate. Built for indie authors who want a professional publishing operation.

---

## What This Skill Does

This is the methodology layer for the KDP Author Engine — a complete set of authoring, publishing, and marketing instructions that activates across a 6-agent OpenClaw pipeline.

Install this skill and your agents gain access to:
- Humanization rules (60+ forbidden AI phrases, structural tell detection)
- 6-dimension quality scoring system with weighted thresholds
- Genre playbooks for 7 book categories
- Amazon keyword research methodology
- Full KDP formatting and metadata guidance
- 12-week launch and marketing playbook

| Agent | Role |
|-------|------|
| **Bookfinder** 🔎 | Weekly Amazon scans, keyword intelligence, revenue estimates |
| **Author** 📖 | Blueprint creation, chapter briefs, pipeline orchestration |
| **Bookwriter** ✍️ | Chapter drafting with humanization rules and self-review |
| **Editor** ✏️ | 6-dimension quality scoring — minimum 7.5/10 to pass |
| **Publisher** 🚀 | KDP formatting, metadata, keywords, categories, cover brief |
| **Marketer** 📣 | ARC strategy, Amazon Ads, social media, email, performance reports |

---

## Requirements

- **OpenClaw** v4.5+ with Discord enabled
- **pandoc** — for .docx manuscript export (`brew install pandoc` on Mac)
- **Discord server** with 6 channels (one per agent)
- **BOOKS_DIR** — set in your agent config or as an env variable — the local path where manuscript .docx files are saved

---

## What's Inside This Skill

7 reference files — the complete indie publishing methodology:

| File | What It Covers |
|------|---------------|
| `humanization-rules.md` | 60+ forbidden AI phrases, structural tells, mandatory self-review checklist |
| `quality-checklist.md` | 6-dimension scoring rubric with weights and minimum thresholds |
| `genre-playbooks.md` | Playbooks for health, children's, AI/tech, faith, literary fiction, commercial fiction, self-help |
| `chapter-workflow.md` | Step-by-step chapter production from brief to approved draft |
| `kdp-publishing.md` | Formatting specs, metadata optimization, BISAC categories, pricing strategy |
| `keyword-research.md` | Amazon autocomplete mining, competitor extraction, BSR-to-sales conversion |
| `book-marketing.md` | 12-week launch timeline, ARC strategy, Amazon Ads, email sequences, performance reporting |

---

## The Pipeline

```
Bookfinder scans Amazon weekly
    ↓ 3 title recommendations + keyword intelligence
You approve a title
    ↓
Author creates blueprint + chapter briefs
    ↓
Bookwriter drafts each chapter
    ↓
Editor scores every draft (6 dimensions, min 7.5/10)
    ↓ failed chapters return with specific revision instructions
You approve each chapter → .docx saved locally via pandoc
    ↓
Author assembles full manuscript
    ↓
Publisher formats for KDP + builds metadata package
    ↓
Book goes live on Amazon
    ↓
Marketer executes launch: ARC, ads, social, email
    ↓ 30/60/90-day performance reports
```

---

## Get the Full Agent Package

This skill contains the methodology. To get the pre-configured agent workspaces, one-command setup script, pipeline workflow, and cron job for automated weekly scans — get the full KDP Author Engine package:

👉 **[Get KDP Author Engine — $149](https://oteng.link/kdp-author-engine)**

---

## Install

```bash
openclaw skills install kdp-author-engine
```

Or via clawhub CLI:
```bash
clawhub install kdp-author-engine
```

---

*Built by Dr. Leo Oteng, PharmD — pharmacist, AI builder, and indie author.*
