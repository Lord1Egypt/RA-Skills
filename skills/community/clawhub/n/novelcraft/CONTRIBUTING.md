# Contributing to NovelCraft

Thank you for your interest in contributing! This document provides guidelines for the NovelCraft 3.0 standardized system.

---

## 📁 Project Structure

### Skill (Read-Only Templates)
```
~/.openclaw/skills/novelcraft/
├── SKILL.md                          # Main documentation
├── README.md                         # Quick start guide
├── CHANGELOG.md                      # Version history
├── CONTRIBUTING.md                     # This file
├── templates/                        # 7 module templates
│   ├── module-concept-template.md
│   ├── module-writer-extras-template.md
│   ├── module-images-template.md
│   ├── module-chapters-template.md
│   ├── module-review-template.md
│   ├── module-revision-template.md
│   └── module-publication-template.md
└── references/
    └── CONFIG.md                     # Config documentation
```

### Workspace (User Data)
```
~/.openclaw/workspace/novelcraft/
├── config/                           # 5 module configs (user-created)
│   ├── CONFIG-SCHEMA.md             # Schema v3.0 documentation
│   ├── PROJECT-MANIFEST-TEMPLATE.md # Project template
│   ├── module-concept.md
│   ├── module-writer-extras.md
│   ├── module-images.md
│   ├── module-chapters.md
│   └── module-publication.md
│
└── Books/projects/novel-[TITLE]/
    ├── project-manifest.md          # Central status file
    ├── 00-concept/                  # Concept, characters, world
    ├── 01-drafts/                   # WIP: drafts, reviews
    ├── 02-chapters/                 # ✅ APPROVED chapters only
    └── 03-final/                    # PDF, EPUB
```

---

## 🏗️ Architecture

### 3-Level Configuration

| Level | Name | Purpose | Override |
|-------|------|---------|----------|
| 1 | Hardcoded | Fallback defaults | — |
| 2 | Module Configs | Technical settings | Level 1 |
| 3 | Project Manifest | Book-specific data | Level 1+2 |

**Rule:** Higher level wins. Only defined fields override.

---

## 📝 Development Guidelines

### Module Config Schema

All `module-*.md` files must follow this structure:

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

## Input
| File | Required |
|------|----------|
| project-manifest.md | true |

## Output
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
| {key} | {value} | Ebene 1|2|3 | Description |

## Prompt Guidelines
- **Genre:** {genre}
- **Style:** {style}
- **Tone:** {tone}
```

### Templates

Templates define subagent tasks. Each template must:
- Specify exact file paths to load
- Define clear output format
- Include validation steps
- Reference project-manifest.md

Example structure:
```markdown
# Module Template: [Name]

## Task for Subagent

**STEP 1: Load Configuration**
Read:
1. `/path/to/project-manifest.md`
2. `/path/to/module-[name].md`

**STEP 2: [Action]**
...

**STEP 3: Save Output**
Save to: `/path/to/output.md`
```

### Review System

All chapter templates must:
1. Write to `01-drafts/chapter_XX_draft.md`
2. Trigger review subagent
3. Use scoring criteria with weights
4. Support max 3 revisions

---

## 🔍 Code Style

### Markdown Formatting
- Use ATX-style headers (`## Header`)
- Use tables for structured data
- Use code blocks for examples
- Keep line length reasonable (~100 chars)

### Naming Conventions
- **Files:** lowercase-with-dashes.md
- **Settings:** snake_case
- **Tables:** Clear headers, aligned columns
- **Booleans:** true | false (not yes/no)

### Language
- All documentation in English
- UTF-8 encoding only
- Full paths in templates

---

## 🚀 Submitting Changes

### Before Submitting

- [ ] Test with a test project
- [ ] Update CHANGELOG.md
- [ ] Update relevant documentation
- [ ] Check for breaking changes
- [ ] Verify markdown formatting

### Change Types

**Config Changes:**
- Follow standardized schema
- Tables properly formatted
- Settings include Override level
- Validation rules documented

**Template Changes:**
- Clear step-by-step structure
- Exact file paths specified
- Validation steps included
- Test with actual subagent run

**Documentation Changes:**
- Clear and concise
- Examples provided
- Links work correctly
- No typos

### Process

1. Fork the repository
2. Create a feature branch
3. Update relevant templates/configs
4. Update CHANGELOG.md
5. Submit pull request

---

## 📋 Configuration Levels Reference

### What Belongs Where

**Level 1 (Hardcoded):**
- Fallback word count: 7500
- Max revisions: 3
- Path structure
- Review weights

**Level 2 (Module Config):**
- Prompt guidelines
- API endpoints
- Validation rules
- Timeout values
- Retry logic
- Output specifications

**Level 3 (Project Manifest):**
- Book title, subtitle, author
- Chapter count
- Enable/disable features (prolog, epilog, images)
- Module status tracking
- Revision tracking

---

## ❓ Questions?

Open an issue on GitHub: https://github.com/Kesuek/novelcraft

---

**Maintained by:** Felix (AI) with Ronny (User) 🧠💡

*NovelCraft 3.0 — Standardized, Modular, Quality-first*
