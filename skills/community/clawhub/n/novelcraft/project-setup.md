# NovelCraft Project Setup Script

> Chat commands for creating NovelCraft projects and configs

---

## 🚀 Create New Project

### Quick Setup (Slash Commands)

```
/novelcraft setup
```

### Module-Specific Setup

```
/novelcraft setup concept       # Genre, characters, plot
/novelcraft setup images        # Image generation settings
/novelcraft setup chapters      # Chapter writing settings
/novelcraft setup publication   # PDF/EPUB settings
```

### Alternative Syntax

```
NovelCraft --setup
NovelCraft --setup --module=images
```

### Legacy (Natural Language)

```
"Create NovelCraft project 'my-novel' with title 'The Fires of Ashara', 
Genre 'Epic Fantasy', 15 chapters, with prolog, without epilog, with images"
```

---

## ⚙️ Interactive Configuration (Reconfigure)

### Full Reconfiguration

```
/novelcraft reconfigure
```

### Single Module Reconfiguration

```
/novelcraft reconfigure images
/novelcraft reconfigure chapters
/novelcraft reconfigure concept
/novelcraft reconfigure writer
/novelcraft reconfigure publication
```

### Alternative Syntax

```
NovelCraft --reconfigure
NovelCraft --reconfigure --module=images
```

### Legacy (Natural Language)

```
"Reconfigure NovelCraft"         — All modules
"Reconfigure module images"        — Images only
"Reconfigure image resolutions"    — Just sizes
```

---

## 📝 Config Management

### Show Configs

```
"Show all NovelCraft configs"
"Show module-concept.md"
"Show project-manifest"
```

### Edit Config

```
"Change Genre to 'Sci-Fi' in module-concept.md"
"Set chapter_count to 12 in project-manifest"
"Enable prolog in project-manifest"
"Disable images in project-manifest"
```

### Validate Config

```
"Check NovelCraft configs"
"Validate project-manifest"
```

---

## 🔄 Project Status

### Show Status

```
"Show NovelCraft status"
"How far is my book?"
"Which modules are done?"
```

### Manual Step

```
"Start Module Concept"
"Start image generation"
"Write Chapter 1"
"Create PDF"
```

---

## 📋 Recurring Tasks

### Project List

```
"Show all NovelCraft projects"
"List my books"
```

### Backup

```
"Backup NovelCraft configs"
"Export project-manifest"
```

### Reset

```
"Reset NovelCraft configs to defaults"
"Delete project 'my-novel'"
```

---

## 🛠️ Development

### Show Template

```
"Show module-concept-template"
"Show module-chapters-template"
```

### Schema Docs

```
"Show CONFIG-SCHEMA"
"Show PROJECT-MANIFEST-TEMPLATE"
```

---

## 💡 Example Workflows

### Workflow 1: Quick Start

```
1. "Create NovelCraft project 'dragon-novel' with title 
    'The Last Dragons', Genre 'Fantasy', 12 chapters"
2. "Start NovelCraft" ← runs autonomously
```

### Workflow 2: Step-by-Step

```
1. "Create NovelCraft project 'my-novel'"
2. [Answer questions]
3. "Show module-concept.md" ← check
4. "Start Module Concept"
5. "Show 00-concept/concept.md" ← check
6. "Start Module Chapters"
7. ...
```

### Workflow 3: Existing Project

```
1. "Show NovelCraft status"
2. "Chapter 3 is done, next please"
3. ...
```

---

## 📊 Parameter Reference

### Project Manifest (Level 3 Overrides)

| Parameter | Type | Default | Description |
|-----------|-----|---------|--------------|
| chapter_count | int | 15 | Number of chapters |
| has_prolog | bool | true | Generate prolog |
| has_epilog | bool | true | Generate epilog |
| images_enabled | bool | true | Generate images |
| character_count | int | 5 | Number of character images |
| language | str | de | Language (de/en) |

### Module Configs (Level 2)

| Config | Key-Settings |
|--------|--------------|
| module-concept.md | genre, style, tone, chapter_count |
| module-writer-extras.md | has_prolog, has_epilog, prolog_tone |
| module-images.md | provider, api_endpoint, low_ram, character_count |
| module-chapters.md | min_words, max_words, max_revisions, scoring_enabled |
| module-publication.md | formats, pdf_engine, font, font_size, margins |

---

## ❓ Help

```
"How does NovelCraft work?"
"Explain the review system"
"What does '3-Level Hierarchy' mean?"
"Show NovelCraft documentation"
```

---

## 🎯 Power User

### Multiple Projects

```
"Switch to project 'novel-a'"
"Copy config from 'novel-a' to 'novel-b'"
```

### Custom Templates

```
"Create custom module-concept-template"
"Use template from ~/templates/"
```

---

**Version:** 3.0.0  
**See also:** `setup.md` for Setup Guide
