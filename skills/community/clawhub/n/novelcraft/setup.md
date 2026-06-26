# NovelCraft Setup Guide

> Chat-based setup for NovelCraft v3.2 — with Target Audience Profiles

---

## Quick Start (Chat)

Copy this block into chat and customize:

```markdown
## NovelCraft Setup

### 1. Project Name
**Project ID:** [your-project-name]  
**Book Title:** [Your Book Title]  
**Subtitle:** [optional]

### 2. Target Audience (NEW v3.2)
**Profile:** [early-readers / middle-grade / young-adult / new-adult / adult / senior / custom]  
*Auto-configures: Chapter length, images, wording, PDF layout*

### 3. Genre & Style (Optional if profile selected)
**Genre:** [Epic Fantasy / Sci-Fi / Thriller / Children Book / ...]  
**Style:** [Atmospheric-dense / Action-oriented / Humorous / ...]  
**Tone:** [Dark-hopeful / Light / Humorous / ...]

*Note: If target profile selected, these may be pre-filled with recommendations*

### 4. Book Structure
**Chapters:** [10-15]  
**Prolog:** [yes / no]  
**Epilog:** [yes / no]  
**Images:** [yes / no]

### 5. Image Configuration (if images=yes)
*Auto-configured by profile, editable:*
**Provider:** [mflux-webui / mcp / api / local / manual / none]  
**Generate Cover:** [yes / no]  
**Generate Characters:** [yes / no]  
**Character Count:** [3-8]  
**Generate Settings:** [yes / no]  
**Settings contain people:** [yes / no] - **Default: NO**  
**Generate Chapter Images:** [yes / no]

### 6. Chapter Configuration
*Auto-configured by profile, editable:*
**Min Words:** [auto or 800-7000]  
**Max Words:** [auto or 1200-8000]  
**Target:** [auto or 1000-7500]  
**Max Revisions:** [auto or 2-3]

### 6. Technical
**Language:** [de / en / ...]  
**PDF Engine:** [xelatex / pandoc]  
**Font:** [Latin Modern Roman / ...]

---
**Start Setup:** "Create NovelCraft config for this project"
```

---

## Target Audience Profiles (v3.2)

**NEW:** Select a profile for automatic configuration of all modules!

### Available Profiles

| # | Profile | Age | Chapter Words | Images | Use Case |
|---|---------|-----|---------------|--------|----------|
| 1 | **early-readers** | 6-8 | 800-1,200 | 8+ chars, chapter images | First readers, picture books |
| 2 | **middle-grade** | 8-12 | 1,500-2,500 | 6 chars, chapter images | Adventure, fantasy, self-reading |
| 3 | **young-adult** | 12-16 | 3,000-5,000 | 4 chars, minimal | Teen themes, emotional |
| 4 | **new-adult** | 16-25 | 4,000-6,000 | 3 chars, minimal | Coming-of-age, complex |
| 5 | **adult** | 25+ | 5,000-8,000 | 3 chars | Full freedom, all genres |
| 6 | **senior** | 60+ | 3,000-5,000 | 4 chars | Large text, relaxed pace |
| 7 | **custom** | any | manual | manual | Full manual control |

### What Auto-Configures?

Selecting a profile automatically sets:

| Module | Settings |
|--------|----------|
| **Chapters** | Min/max words, sentences per paragraph, max revisions |
| **Images** | Character count, chapter images yes/no, settings yes/no |
| **Concept** | Wording style, vocabulary complexity |
| **Publication** | Font size, line height, margins, font family |

### Override After Profile Selection

You can always override individual settings:

```
You: "Start NovelCraft Setup"
Assistant: "Select target audience: [1] early-readers, [2] middle-grade..."
You: "1" (early-readers)
Assistant: "Profile selected! Auto-configured: 800-1200 words/chapter, 8+ character images..."
You: "Change chapter target to 1500 words"
Assistant: "Override applied. Chapter target: 1500 (profile default was 1000)"
```

### Profile Examples

**Early Readers (6-8):**
- "Monster in der 1c" — children's book
- Auto: Short chapters, lots of images, simple words
- Font: 14pt Verdana, large margins

**Middle Grade (8-12):**
- Adventure/fantasy series
- Auto: Medium chapters, colorful images, active voice
- Font: 12pt Georgia, medium margins

**Young Adult (12-16):**
- Dystopian romance
- Auto: Longer chapters, realistic style, emotional themes
- Font: 11pt Garamond, standard margins

### Quick Commands

| Command | Action |
|---------|--------|
| `/novelcraft setup` | Full setup with profile selection |
| `/novelcraft setup target-audience` | Change profile only |
| `/novelcraft reconfigure` | Reconfigure all (keeps profile) |

---

## Step-by-Step

### Step 1: Create Project

Say in chat:
> "I want to create a new NovelCraft project"
> "Start NovelCraft Setup"

The assistant will ask:
1. **Target Audience Profile** (NEW v3.2) — Select profile for auto-configuration
2. Project ID (short, no spaces)
3. Book title
4. Genre
5. Chapter count
6. Image preferences

*If you select a profile, chapter lengths and image settings auto-configure!*

### Step 2: Image Configuration (Interactive)

If images=yes, you'll be asked:
1. **Provider:** mflux-webui / mcp / api / local / manual
2. **Cover:** yes/no
3. **Characters:** yes/no + count
4. **Settings:** yes/no
5. **Settings have people:** yes/no (**recommended: NO**)
6. **Chapter Images:** yes/no (one per chapter)

### Step 3: Create Config

The assistant creates:
1. `workspace/config/module-*.md` (5 files)
2. `workspace/Books/projects/{ID}/project-manifest.md`
3. Project folder structure

### Step 4: Review

Check the created configs:
> "Show me the NovelCraft configs"
> "Show module-images.md"

### Step 5: Adjust (Interactive Reconfiguration)

Reconfigure anything interactively:
> "Reconfigure NovelCraft" — Walk through all 5 modules with questions
> "Reconfigure module images" — Just image settings (detailed)
> "Reconfigure module chapters" — Just chapter settings
> "Reconfigure image resolutions" — Just change sizes

---

## Config Options

### Module Configs (all projects)

| Config | Purpose |
|--------|---------|
| `module-concept.md` | Genre, characters, world |
| `module-writer-extras.md` | Prolog/Epilog |
| `module-images.md` | Image generation (cover, characters, settings, chapter images) |
| `module-chapters.md` | Chapter writing |
| `module-publication.md` | PDF/EPUB |

### Image Configuration Options

| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| `provider` | mflux-webui, mcp, api, local, manual, none | none | Image generation provider |
| `generate_cover` | yes / no | yes | Book cover image |
| `generate_characters` | yes / no | yes | Character portraits |
| `character_count` | 3-10 | 5 | Number of characters |
| `generate_settings` | yes / no | yes | Location/environment images |
| `settings_have_people` | yes / no | **NO** | **Settings should be empty!** |
| `generate_chapter_images` | yes / no | no | One image per chapter |
| `chapter_image_count` | matches chapters | - | Auto-set to chapter count |

**IMPORTANT RULES:**
- **Settings NEVER contain people/monsters** — only empty locations
- **Chapter images** = illustration for each chapter header
- **All prompts in ENGLISH** for FLUX compatibility
- **"no text, no letters, no words"** required in every prompt

### Chapter Length by Audience

| Audience | Min Words | Max Words | Target |
|----------|-----------|-----------|--------|
| Children 6-8 | 800 | 1,200 | 1,000 |
| Children 8-10 | 1,500 | 2,500 | 2,000 |
| YA / Teen | 3,000 | 5,000 | 4,000 |
| Adult | 7,000 | 8,000 | 7,500 |

---

## Slash Commands

| Command | Function |
|---------|----------|
| `/novelcraft setup` | Interactive project creation (includes target audience + image config) |
| `/novelcraft setup target-audience` | **NEW:** Configure or change target audience |
| `/novelcraft setup concept` | Configure concept module |
| `/novelcraft setup writer` | Configure writer-extras module |
| `/novelcraft setup images` | Configure images module (detailed) |
| `/novelcraft setup chapters` | Configure chapters module |
| `/novelcraft setup publication` | Configure publication module |
| `/novelcraft reconfigure` | Full reconfiguration (all modules) |
| `/novelcraft reconfigure target-audience` | **NEW:** Change profile and auto-reconfigure |
| `/novelcraft reconfigure images` | Reconfigure images only |

### Alternative Syntax

| Command | Function |
|---------|----------|
| `NovelCraft --setup` | Quick setup with defaults |
| `NovelCraft --setup --module=images` | Setup specific module |
| `NovelCraft --reconfigure` | Reconfigure all |

### Legacy (still works)

| Command | Function |
|---------|----------|
| "Create NovelCraft project" | Start new setup |
| "Reconfigure NovelCraft" | Full reconfiguration |
| "Reconfigure module images" | Reconfigure images only |

---

## Chat Commands (Natural Language)

Use these if you prefer natural language:

### Setup & Configuration

| Command | Function |
|---------|----------|
| "Start NovelCraft Setup" | Interactive project creation |
| "Reconfigure NovelCraft" | Full reconfiguration (all 5 modules) |
| "Reconfigure module images" | Reconfigure images (detailed) |
| "Reconfigure module chapters" | Reconfigure chapters only |
| "Reconfigure image resolutions" | Just change image sizes |
| "Enable chapter images" | Add chapter images to config |
| "Disable settings with people" | Ensure settings are empty |

### View & Edit

| Command | Function |
|---------|----------|
| "Show NovelCraft configs" | Display all current configs |
| "Show module-images.md" | Show specific module |
| "Change [X] to [Y]" | Quick config edit |

### Control

| Command | Function |
|---------|----------|
| "Start NovelCraft" | Begin book creation |
| "NovelCraft status" | Show project status |

---

## Example Session

```
You: I want to create a children's book

Assistant: Great! I'll set up NovelCraft.

Questions:
1. Project ID (e.g. "monster-1c"): monster-1c
2. Book title: Monster in der 1c
3. Subtitle (optional): Damit hat keiner gerechnet
4. Genre: Children's book
5. Target audience: Children 6-8
6. How many chapters (10-15)? 12
7. Prolog wanted? yes
8. Epilog wanted? yes
9. Generate images? yes
10. Image provider? mflux-webui
11. Generate cover? yes
12. Generate characters? yes (how many? 8)
13. Generate settings? yes
14. Settings contain people? NO (recommended)
15. Generate chapter images? yes

[Assistant creates configs with appropriate settings]

Assistant: Configs created! Chapter length auto-set to 800-1200 words 
for your target audience.

Verify with: "Show me module-images.md"

You: Enable chapter images

Assistant: Chapter images enabled - one per chapter will be generated.
```

---

## Image Generation Guidelines

### English Prompts Only
All prompts must be in English for FLUX compatibility.

### No Text in Images
Every prompt MUST include:
```
no text, no letters, no words, no typography, no writing, no watermark, no signature
```

### Settings = Empty Places
Settings images show **only locations**, never people or monsters:
- ✅ Classroom with empty desks
- ✅ Playground with no children
- ✅ Corridor with no students
- ❌ Classroom with children
- ❌ Playground with monsters

### Chapter Images
Optional: One illustration per chapter header:
- Style: Consistent with book art
- Content: Scene from the chapter
- Size: 512x768 or 768x512
- Text: NEVER

---

## Troubleshooting

### Config not found
> "Show NovelCraft directory"

### Module missing
> "Create missing module-*.md"

### Check project status
> "Show project-manifest"

### Image prompts have text
Regenerate with stronger negative prompt:
> "no text, no letters, no words, no typography" 

---

## More Help

- **Image Prompt Guide:** `workspace/config/IMAGE-PROMPT-GUIDE.md`
- **Schema:** `workspace/config/CONFIG-SCHEMA.md`
- **Template:** `workspace/config/PROJECT-MANIFEST-TEMPLATE.md`
- **Docs:** `skill/references/CONFIG.md`
- **Project Commands:** `skill/project-setup.md`

---

**Version:** 3.1.0 — with Chapter Images & Image Configuration
