# NovelCraft Configuration Setup

Step-by-step guide to create all 5 module configuration files.

---

## Prerequisites

```bash
# Create workspace directory
mkdir -p ~/.openclaw/workspace/novelcraft/config

# Copy this file to your workspace
cp ~/.openclaw/skills/novelcraft/references/config-setup.md \
   ~/.openclaw/workspace/novelcraft/config/README.md
```

---

## Module 0: Concept (`module-concept.md`)

**Create:** `~/.openclaw/workspace/novelcraft/config/module-concept.md`

```markdown
# Module: Concept

## Book Info
- title: Your Book Title
- subtitle: Optional Subtitle
- genre: Fantasy
- theme: redemption, sacrifice, power
- mood: dark, atmospheric, hopeful

## Characters
- protagonist: Name, age, backstory, motivation
- antagonist: Name, motivation, conflict with protagonist
- supporting: Character 1, Character 2, Character 3

## Plot Structure
- act_1: Setup and inciting incident
- act_2: Rising action, midpoint twist
- act_3: Climax and resolution

## Worldbuilding
- setting: Time period, location description
- magic_system: Rules, limitations, cost
- history: Key historical events

## Chapter Plan
- count: 15
- approximate_words_per_chapter: 7500
- total_target_words: 112500

## Flashbacks
- count: 3
- placement: Chapters 5, 9, 12
- purpose: Reveal protagonist's backstory
```

**✓ Checklist:**
- [ ] Title and subtitle defined
- [ ] Genre and mood set
- [ ] Protagonist and antagonist described
- [ ] 3-act structure outlined
- [ ] Magic system defined (if applicable)
- [ ] Chapter count set (10-15 recommended)
- [ ] Flashbacks planned (optional)

---

## Module 1: Writer Extras (`module-writer-extras.md`)

**Create:** `~/.openclaw/workspace/novelcraft/config/module-writer-extras.md`

```markdown
# Module: Writer Extras

## Prolog
- enabled: false
- word_count: 1500
- tone: mysterious
- hook: Sets up the world before Chapter 1
- content: Historical event or mythological backstory

## Epilog
- enabled: false
- word_count: 1500
- tone: reflective
- timeframe: One year later
- content: Shows aftermath and hints at future
```

**✓ Checklist:**
- [ ] Prolog enabled/disabled decided
- [ ] Epilog enabled/disabled decided
- [ ] Tone for each defined (if enabled)

---

## Module 2: Images (`module-images.md`)

**Create:** `~/.openclaw/workspace/novelcraft/config/module-images.md`

```markdown
# Module: Images

## Provider
- type: mcp_server
- server: mflux-webui
- endpoint: http://192.168.2.150:7861

## Generation Settings
- low_ram: true
- estimated_time_per_image: 45min

## Images to Generate
- cover: true
- characters: true
- character_count: 5
- settings: false
- chapter_images: false

## Character Prompts (if characters enabled)
- protagonist: "Portrait of [name], detailed description..."
- antagonist: "Portrait of [name], detailed description..."
- supporting_1: "Portrait of [name], detailed description..."
- supporting_2: "Portrait of [name], detailed description..."
- supporting_3: "Portrait of [name], detailed description..."

## Cover Prompt (if cover enabled)
- prompt: "Epic fantasy book cover, dark atmosphere, dragon..."
- size: 1024x1448
```

**✓ Checklist:**
- [ ] Provider configured (mcp_server, api, or manual)
- [ ] Cover generation enabled/disabled
- [ ] Character count set (3-5 recommended, or 0)
- [ ] Character prompts written (if enabled)
- [ ] Low RAM mode set (true for 16GB systems)

---

## Module 3: Chapters (`module-chapters.md`)

**Create:** `~/.openclaw/workspace/novelcraft/config/module-chapters.md`

```markdown
# Module: Chapters

## Word Count
- min_words: 7000
- target_words: 7500
- max_words: 8000

## Language
- code: de
- check_encoding: true

## Style
- tone: atmospheric
- perspective: third_person_limited
- tense: past
- atmosphere: dark, hopeful
- pacing: character-driven

## Review Settings
- scoring_enabled: true
- max_revisions: 3
- auto_decision: true

## Scoring Weights
- encoding: 3
- word_count: 2
- continuity: 2
- plot: 2
- character: 1.5
- style: 1.5
- grammar: 1

## Chapter Template
- structure: hook → development → climax → resolution → cliffhanger
- sensory_details: 3 per scene minimum
- dialogue_ratio: 30%
```

**✓ Checklist:**
- [ ] Word count range set (7000-8000)
- [ ] Language code set (de, en, etc.)
- [ ] Style defined (tone, perspective, atmosphere)
- [ ] Review enabled with scoring
- [ ] Max revisions set (3 recommended)

---

## Module 4: Publication (`module-publication.md`)

**Create:** `~/.openclaw/workspace/novelcraft/config/module-publication.md`

```markdown
# Module: Publication

## Output Formats
- epub: true
- pdf: true
- pdf_engine: xelatex

## Typography
- font: Latin Modern Roman
- font_size: 12pt
- line_height: 1.6
- margins: 2cm

## Layout
- paper_size: a4
- include_cover: true
- include_toc: true
- chapter_page_break: true

## Cover
- style: image_with_overlay
- title_position: center
- overlay_opacity: 0.4

## Output Paths
- final_dir: 03-final
- epub_filename: die-feuer-von-ashara.epub
- pdf_filename: die-feuer-von-ashara.pdf

## Visual Enhanced Version
- create_visual_version: true
- include_images: chapter_headers
- image_placement: before_chapter
```

**✓ Checklist:**
- [ ] EPUB and/or PDF selected
- [ ] Font and size defined
- [ ] Margins set
- [ ] Cover style chosen
- [ ] Output filenames defined
- [ ] Visual version enabled/disabled

---

## Project Manifest Template

**Create:** `~/.openclaw/workspace/novelcraft/Books/projects/novel-YOURBOOK/project-manifest.md`

```markdown
# Project Manifest

## Project Info
- **Name:** novel-yourbook
- **Title:** Your Book Title
- **Subtitle:** Optional Subtitle
- **Author:** NovelCraft
- **Created:** YYYY-MM-DD
- **Language:** de
- **Encoding:** UTF-8

## Paths
| Variable | Path | Description |
|----------|------|-------------|
| workspace | ~/.openclaw/workspace/novelcraft | Base workspace |
| project_dir | ~/.openclaw/workspace/novelcraft/Books/projects/novel-yourbook | Project root |
| concept_dir | 00-concept | Concept, characters, world |
| drafts_dir | 01-drafts | Work-in-progress chapters |
| chapters_dir | 02-chapters | Approved final chapters |
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
| concept | pending | ~/.openclaw/workspace/novelcraft/config/module-concept.md |
| writer-extras | pending | ~/.openclaw/workspace/novelcraft/config/module-writer-extras.md |
| images | pending | ~/.openclaw/workspace/novelcraft/config/module-images.md |
| chapters | pending | ~/.openclaw/workspace/novelcraft/config/module-chapters.md |
| publication | pending | ~/.openclaw/workspace/novelcraft/config/module-publication.md |

## Revision Tracking
| Chapter | Status | Score | Revisions | Location |
|---------|--------|-------|-----------|----------|
| 01 | pending | - | 0 | - |
| 02 | pending | - | 0 | - |
| 03-XX | pending | - | 0 | - |

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

**✓ Checklist:**
- [ ] Project name set (lowercase, hyphens)
- [ ] Title and subtitle defined
- [ ] Language set
- [ ] All 5 config paths correct
- [ ] Chapter count in revision tracking table

---

## Final Checklist

**Before Starting NovelCraft:**

- [ ] `module-concept.md` created with full book concept
- [ ] `module-writer-extras.md` created (can be minimal if no prolog/epilog)
- [ ] `module-images.md` created (can disable all images)
- [ ] `module-chapters.md` created with style settings
- [ ] `module-publication.md` created with output settings
- [ ] `project-manifest.md` created in project directory
- [ ] All file paths in project-manifest.md are correct
- [ ] All 6 files saved and readable

**Start Writing:**

Once all configurations are complete, NovelCraft will run autonomously:
1. Load project-manifest.md
2. Execute modules in order
3. Write chapters sequentially with review
4. Create final PDF/EPUB

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Config not found | Check path in project-manifest.md |
| Encoding errors | Ensure UTF-8, no special characters |
| Image generation fails | Set `enabled: false` in module-images.md |
| Chapter too short | Adjust min_words in module-chapters.md |
| Review always fails | Check scoring weights and thresholds |

---

## See Also

- `~/.openclaw/skills/novelcraft/references/CONFIG.md` — Full configuration documentation
- `~/.openclaw/skills/novelcraft/SKILL.md` — Skill documentation
- `~/.openclaw/skills/novelcraft/README.md` — Quick start guide
