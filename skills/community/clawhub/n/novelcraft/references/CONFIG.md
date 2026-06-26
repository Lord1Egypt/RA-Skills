# NovelCraft Configuration Reference

> Complete configuration documentation for NovelCraft v3.0

---

## Quick Reference

| Level | Name | Location | Purpose | Override |
|-------|------|----------|---------|----------|
| 1 | Hardcoded | Skill code | Fallback defaults | — |
| 2 | Module Configs | `workspace/config/module-*.md` | Technical settings | Level 1 |
| 3 | Project Manifest | `workspace/Books/projects/{PROJECT}/project-manifest.md` | Book-specific | Level 1+2 |

**Rule:** Higher level wins. Only defined fields override.

---

## Schema Documentation

For complete schema specification, see:
- **Workspace:** `~/.openclaw/workspace/novelcraft/config/CONFIG-SCHEMA.md`
- **Template:** `~/.openclaw/workspace/novelcraft/config/PROJECT-MANIFEST-TEMPLATE.md`

---

## Directory Structure

### Workspace (Project Data)
```
~/.openclaw/workspace/novelcraft/
├── config/                              # 5 Module Configs
│   ├── CONFIG-SCHEMA.md                # Schema v3.0 documentation
│   ├── PROJECT-MANIFEST-TEMPLATE.md      # Project template
│   ├── module-concept.md
│   ├── module-writer-extras.md
│   ├── module-images.md
│   ├── module-chapters.md
│   └── module-publication.md
│
└── Books/projects/[PROJECT]/
    ├── project-manifest.md              # Central Manifest (Level 3)
    ├── 00-concept/                      # Concept, characters, world
    ├── 01-drafts/                       # Drafts, reviews, revisions
    ├── 02-chapters/                     # ✅ APPROVED chapters only
    └── 03-final/                        # PDF, EPUB Output
```

---

## Configuration Levels

### Level 1: Hardcoded Defaults

**Location:** Skill code (unchangeable)

```yaml
chapter:
  min_words: 7000
  target_words: 7500
  max_words: 8000
  title_style: titled
  include_numbers: true

review:
  max_revisions: 3
  scoring_enabled: true
  weights:
    encoding: 3        # CRITICAL
    word_count: 2      # HIGH
    continuity: 2      # HIGH
    plot: 2            # HIGH
    character: 1.5     # MEDIUM
    style: 1.5         # MEDIUM
    grammar: 1         # LOW

thresholds:
  approved: 8.0
  minor_revision: 6.0
  major_revision: 4.0
  rejected: 0.0

paths:
  workspace_subdir: novelcraft
  books_folder: Books
  projects_subdir: projects
  concept_dir: 00-concept
  drafts_dir: 01-drafts
  chapters_dir: 02-chapters
  final_dir: 03-final
  images_dir: images
```

### Level 2: Module Configs

**Location:** `~/.openclaw/workspace/novelcraft/config/module-*.md`

Each module config follows standardized structure:

```markdown
# Module: {Name}

## Info
- **Name:** {module-name}
- **Type:** mandatory | optional
- **Order:** {number}

## Execution
| Setting | Value |
|---------|-------|
| Parallel | true | false |
| Blocking | true | false |
| Max retries | 2 |
| Estimated duration | 1-2h |

## Input
| File | Required | Description |
|------|----------|-------------|
| project-manifest.md | true | Project metadata |

## Output Files
| File | Required | Description |
|------|----------|-------------|
| {file} | true | Description |

## Validation Rules
| Rule | Value | Critical |
|------|-------|----------|
| {rule} | {value} | true | false |

## Settings
| Setting | Default | Override | Description |
|---------|---------|----------|-------------|
| {key} | {value} | Ebene 3 | Description |

## Prompt Guidelines
- **Genre:** {genre}
- **Style:** {style}
- **Tone:** {tone}
- **Language:** de
```

### Level 3: Project Manifest

**Location:** `~/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`

Central status file for all subagents:

```markdown
# Project Manifest

## Project Info
- **Name:** novel-drachen
- **Title:** Die Feuer von Ashara
- **Subtitle:** Das Erbe der Drachenkönige
- **Author:** NovelCraft
- **Created:** 2026-04-05
- **Language:** de
- **Encoding:** UTF-8

## Paths
| Variable | Path | Description |
|----------|------|-------------|
| workspace | ~/.openclaw/workspace/novelcraft | Base workspace |
| project_dir | ~/.openclaw/workspace/novelcraft/Books/projects/novel-drachen | Project root |
| concept_dir | 00-concept | Concept, characters, world |
| drafts_dir | 01-drafts | Work-in-progress |
| chapters_dir | 02-chapters | Approved chapters only |
| final_dir | 03-final | PDF, EPUB output |
| images_dir | images | Cover, characters, settings |

## Configs
| Module | Path |
|--------|------|
| concept | ~/.openclaw/workspace/novelcraft/config/module-concept.md |
| writer-extras | ~/.openclaw/workspace/novelcraft/config/module-writer-extras.md |
| images | ~/.openclaw/workspace/novelcraft/config/module-images.md |
| chapters | ~/.openclaw/workspace/novelcraft/config/module-chapters.md |
| publication | ~/.openclaw/workspace/novelcraft/config/module-publication.md |

## Modules Status
| Module | Status | Config |
|--------|--------|--------|
| concept | done | ~/.openclaw/workspace/novelcraft/config/module-concept.md |
| writer-extras | pending | ~/.openclaw/workspace/novelcraft/config/module-writer-extras.md |
| images | done | ~/.openclaw/workspace/novelcraft/config/module-images.md |
| chapters | rewriting | ~/.openclaw/workspace/novelcraft/config/module-chapters.md |
| publication | pending | ~/.openclaw/workspace/novelcraft/config/module-publication.md |

## Book Settings (Override Module Configs)
| Setting | Value | Override |
|---------|-------|----------|
| chapter_count | 15 | Ebene 2 |
| has_prolog | true | Ebene 2 |
| has_epilog | true | Ebene 2 |
| images_enabled | true | Ebene 2 |

## Revision Tracking
| Chapter | Status | Score | Revisions | Location |
|---------|--------|-------|-----------|----------|
| 01 | ✅ approved | 8.5 | 0 | 02-chapters/chapter_01.md |
| 02 | 🔧 rewriting | - | 1 | 01-drafts/chapter_02_draft.md |

## Execution Order
1. concept (mandatory)
2. writer-extras (optional) — prolog
3. images (parallel to chapters)
4. chapters (mandatory, sequential)
5. writer-extras (optional) — epilog
6. publication (mandatory)

## Validation
| Rule | Value |
|------|-------|
| Encoding | UTF-8 |
| Min chapters | 15 |
| Max chapters | 15 |
| Min words per chapter | 7000 |
| Max words per chapter | 8000 |
| No foreign characters | true |
```

---

## Module Reference

### Module 0: Concept

**Config:** `module-concept.md`

**Key Settings:**
- genre, mood, theme
- protagonist, antagonist
- setting, magic_system
- chapter_count (10-15 recommended)
- character_count (3-5)

**Creates:**
- `00-concept/concept.md`
- `00-concept/characters.md`
- `00-concept/world.md`
- `00-concept/plan.md`

### Module 1: Writer Extras

**Config:** `module-writer-extras.md`

**Key Settings:**
- has_prolog: true | false
- has_epilog: true | false
- prolog_tone: mysterious | ...
- epilog_tone: reflective | ...

**Creates:**
- `00-concept/prolog.md`
- `00-concept/epilog.md`

### Module 2: Images

**Config:** `module-images.md`

**Key Settings:**
- provider: mflux-webui | mcp-server | external_api | local | manual
- api_endpoint: http://...
- low_ram: true | false
- generate_cover: true | false
- generate_characters: true | false
- character_count: 3-5
- text_in_image: false (FLUX limitation)
- overlay_text: true

**Creates:**
- `images/cover.png`
- `images/{character}.png`
- `images/{setting}.png`

**Important:** Never block on images — proceed to module 3 immediately!

### Module 3: Chapters

**Config:** `module-chapters.md`

**Key Settings:**
- min_words: 7000
- max_words: 8000
- target_words: 7500
- max_revisions: 3
- scoring_enabled: true
- chapter_title_style: titled | numbered | both
- auto_generate_titles: true | false
- include_chapter_numbers: true | false

**Creates:**
1. `01-drafts/chapter_XX_draft.md`
2. `01-drafts/chapter_XX_review.md`
3. (Optional) Revisions
4. On APPROVED: `02-chapters/chapter_XX.md`

**Rules:**
- Only ONE chapter at a time
- Always review with scoring
- Max 3 revisions, then rewrite

### Module 4: Publication

**Config:** `module-publication.md`

**Key Settings:**
- formats: [pdf, epub]
- pdf_engine: xelatex | pandoc
- epub_tool: pandoc
- font: Latin Modern Roman
- font_size: 11pt | 12pt
- line_height: 1.5 | 1.6
- margins: 2cm | 2.5cm
- include_cover: true | false
- include_toc: true | false

**Creates:**
- `03-final/{title}.pdf`
- `03-final/{title}.epub`

**Important:** Reads ONLY from `02-chapters/` (approved chapters)!

---

## Review System

### Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| UTF-8 Encoding | ×3 (CRITICAL) | No foreign characters |
| Word Count 7000-8000 | ×2 (HIGH) | Target: 7500 words |
| Continuity | ×2 (HIGH) | Consistent with previous chapter |
| Plot Progression | ×2 (HIGH) | Story develops |
| Character Voice | ×1.5 (MEDIUM) | Believable characters |
| Style & Atmosphere | ×1.5 (MEDIUM) | Fits project style |
| Grammar | ×1 (LOW) | Correct language |

**Calculation:** Weighted Score = Σ(score × weight) / Σ(weights)

### Decision Matrix

| Score | Decision | Action |
|-------|----------|--------|
| 8.0-10.0 | ✅ **APPROVED** | Copy to 02-chapters/, next chapter |
| 6.0-7.9 | ⚠️ **MINOR_REVISION** | Specific fixes, max 3 revisions |
| 4.0-5.9 | 🔧 **MAJOR_REVISION** | Major rewrite, max 3 revisions |
| 0.0-3.9 | ❌ **REJECTED** | Complete rewrite, max 3 revisions |

---

## Important Rules

1. **Configs in workspace, not in skill** — `~/.openclaw/workspace/novelcraft/config/`
2. **Templates in skill** — `~/.openclaw/skills/novelcraft/templates/`
3. **Only approved chapters in 02-chapters/** — Publication reads only from there
4. **Images never block** — Proceed to chapters immediately
5. **Chapters never parallel** — Strictly sequential
6. **Autonomous = no questions** — Only ask in step-by-step mode
7. **3-Level hierarchy** — Higher level wins on conflicts

---

## Migration History

| Version | Schema | Changes |
|---------|--------|---------|
| 3.0 | Standardized | Clear 3-level hierarchy, standardized module structure |
| 2.0 | Modular | Module configs, review system, scoring |
| 1.0 | Legacy | Single defaults file |

---

**Version:** 3.0.0 — Standardized Config Schema  
**Maintained by:** Felix (AI) with Ronny (User) 🧠💡
