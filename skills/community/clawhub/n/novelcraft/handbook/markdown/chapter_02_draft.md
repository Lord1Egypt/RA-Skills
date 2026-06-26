# Chapter 2: Configuration & Setup

## The 3-Level Configuration Hierarchy

Novelcraft works with a 3-level hierarchy system. Higher levels override lower ones.

### Level 1: Hardcoded (Skill Code)
Fallback values — only relevant if nothing else is defined.

### Level 2: Module Configs
Path: `~/.openclaw/workspace/novelcraft/config/`

Here you set technical configurations:

| Config File | Contains |
|-------------|----------|
| `module-concept.md` | Genre, theme, characters, plot, worldbuilding |
| `module-writer-extras.md` | Prolog/epilog enabled? |
| `module-images.md` | Image provider, cover, character count |
| `module-chapters.md` | Word count, revisions, scoring |
| `module-publication.md` | Formats, layout, typography |

### Level 3: Project Manifest
Path: `~/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`

Book-specific data: title, chapter count, progress tracking.

## Important Default Values

- **Words per chapter:** 7,000-8,000 (target: 7,500)
- **Max revisions:** 3 per chapter
- **Formats:** PDF, EPUB
- **Scoring:** Enabled (decides approval)

## Directory Structure

```
~/.openclaw/workspace/novelcraft/
├── config/                    # Your module configs
├── Books/
│   └── projects/{PROJECT}/
│       ├── project-manifest.md  # Status tracking
│       ├── 00-concept/          # Concept data
│       ├── 01-drafts/           # Raw chapters + reviews
│       ├── 02-chapters/         # ✅ Finalized chapters
│       └── 03-final/            # PDF, EPUB
```

## Quick Start

1. Load Novelcraft skill: `clawhub install novelcraft`
2. Create project folder
3. Create `project-manifest.md`
4. Adjust module configs as needed
5. Start

---

*Next chapter: The complete workflow from beginning to end.*
