# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [3.2.0] - 2026-04-06

### Added
- **Target Audience Profiles** (NEW!)
  - 6 profiles: early-readers (6-8), middle-grade (8-12), young-adult (12-16), new-adult (16-25), adult (25+), senior (60+)
  - Auto-configures all modules based on selected profile:
    - Chapter length (800-1,200 words for early-readers → 5,000-8,000 for adults)
    - Image count and categories (8+ characters for children → 3 for adults)
    - PDF layout (font size, line height, margins)
    - Wording style and vocabulary complexity
  - New module: `module-target-audience.md`
  - Profile selection in setup: `"Start NovelCraft Setup" → "Select target audience"`
  - Override support: Keep profile, change individual values
  - Documentation: `setup.md`, `SKILL.md`, `TARGET-AUDIENCE-FEATURE.md`

### Enhanced
- **Image Configuration v3.1 → v3.2**
  - Added `generate_chapter_images` setting (one image per chapter)
  - Added `settings_have_people` rule (Settings must be EMPTY)
  - New guide: `IMAGE-PROMPT-GUIDE.md` with English prompt templates
  - Prompt rules: "no text, no letters, no words, no typography" required
  - Settings images: "no people, no characters, no humans, no monsters"
- **Setup Process**
  - Reordered: Target Audience → Genre → Structure → Images → Chapters → Technical
  - Auto-configuration flow with profile selection
  - Chapter length table by audience in `setup.md`

### Changed
- **SKILL.md** v3.1 → v3.2
  - Added Target Audience Profiles section
  - Updated workflow diagram with Target Audience module
  - Added chapter images to image categories
  - New quick start commands: `/novelcraft setup target-audience`
- **setup.md** v3.1 → v3.2
  - Added Target Audience Profiles section with 6 profiles
  - Reorganized setup steps (audience first)
  - Added chapter length by audience table
  - New commands for profile management

## [3.0.0] - 2026-04-06

### Added
- **Standardized Config Schema v3.0**
  - Clear 3-level configuration hierarchy: Hardcoded → Module Configs → Project Manifest
  - Consistent structure across all module configs
  - `CONFIG-SCHEMA.md` documenting the system
  - `PROJECT-MANIFEST-TEMPLATE.md` for new projects
- **Setup Documentation**
  - `setup.md` — Chat-based setup guide (Quick-Start)
  - `project-setup.md` — Chat commands for project management
- **Validation Rules** with weights and critical flags
- **Execution Settings** (Parallel, Blocking, Retries, Duration)
- **Clear Input/Output definitions** per module

### Changed
- **Refactored all module configs** to follow standardized schema:
  - `module-concept.md`
  - `module-writer-extras.md`
  - `module-images.md`
  - `module-chapters.md`
  - `module-publication.md`
- **Migrated legacy configs** into module configs:
  - `novelcraft-defaults.md` → split into module configs
  - `visual_creation.md` → integrated into `module-images.md`
  - `layout-config.md` → integrated into `module-publication.md`
- **Translated all documentation to English**
  - `SKILL.md`
  - `setup.md`
  - `project-setup.md`
- **Updated References table** in `SKILL.md` to include `setup.md` and `project-setup.md`

### Removed
- `novelcraft-defaults.md` (legacy)
- `visual_creation.md` (legacy)
- `layout-config.md` (integrated)

### Added
- **Standardized Config Schema v3.0**
  - Clear 3-level configuration hierarchy: Hardcoded → Module Configs → Project Manifest
  - Consistent structure across all module configs
  - `CONFIG-SCHEMA.md` documenting the system
  - `PROJECT-MANIFEST-TEMPLATE.md` for new projects
- **Setup Documentation**
  - `setup.md` — Chat-based setup guide (Quick-Start)
  - `project-setup.md` — Chat commands for project management
- **Validation Rules** with weights and critical flags
- **Execution Settings** (Parallel, Blocking, Retries, Duration)
- **Clear Input/Output definitions** per module

### Changed
- **Refactored all module configs** to follow standardized schema:
  - `module-concept.md`
  - `module-writer-extras.md`
  - `module-images.md`
  - `module-chapters.md`
  - `module-publication.md`
- **Migrated legacy configs** into module configs:
  - `novelcraft-defaults.md` → split into module configs
  - `visual_creation.md` → integrated into `module-images.md`
  - `layout-config.md` → integrated into `module-publication.md`
- **Translated all documentation to English**
  - `SKILL.md`
  - `setup.md`
  - `project-setup.md`
- **Updated References table** in `SKILL.md` to include `setup.md` and `project-setup.md`

### Removed
- `novelcraft-defaults.md` (legacy)
- `visual_creation.md` (legacy)
- `layout-config.md` (integrated)

## [2.0.0] - 2026-04-05

### Added
- **Modular workflow system**
  - 5 distinct modules: Concept, Writer Extras, Images, Chapters, Publication
  - Module-specific config files (`module-*.md`)
  - Module templates for subagent calls
- **Review workflow with scoring**
  - Automatic scoring system (0-10)
  - Weighted criteria (Encoding ×3, Word Count ×2, etc.)
  - Automatic decision: APPROVED / MINOR_REVISION / MAJOR_REVISION / REJECTED
  - Max 3 revisions per chapter
- **Separate directories**
  - `01-drafts/` - Work-in-progress
  - `02-chapters/` - Approved chapters only
  - Publication reads ONLY from `02-chapters/`
- **Project Manifest**
  - Central status file for all subagents
  - Module status tracking
  - Revision tracking per chapter

### Changed
- Replaced single `project.md` with modular configs
- Chapters now require explicit review before approval
- Sequential chapter writing enforced (no parallel)

### Deprecated
- `novelcraft-defaults.md` (to be removed in v3.0)
- `visual_creation.md` (to be removed in v3.0)
- `layout-config.md` (to be integrated in v3.0)

## [1.0.0] - 2026-03-29

### Added
- Initial NovelCraft release
- Fully autonomous book authoring workflow
- Concept generation (genre, characters, plot, worldbuilding)
- Sequential chapter writing
- PDF/EPUB publication
- Optional prolog/epilog
- Optional image generation
- Legacy config: `novelcraft-defaults.md`

---

## Version Legend

| Version | Schema | Config System | Key Features |
|---------|--------|---------------|--------------|
| 3.2 | Standardized v3.2 | 3-level + Target Audience | Target profiles, chapter images, image prompts |
| 3.1 | Standardized v3.1 | 3-level hierarchy | Enhanced images, chapter images |
| 3.0 | Standardized v3.0 | 3-level hierarchy | Modular configs, setup docs |
| 2.x | Modular | Module configs | Review scoring, sequential chapters |
| 1.x | Legacy | Single defaults file | Initial release |

---

**Maintained by:** Felix (AI) with Ronny (User) 🧠💡
