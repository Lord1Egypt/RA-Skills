# NovelCraft --help

> Command reference for NovelCraft CLI-style interface

## Usage

```
NovelCraft [command] [options]
/novelcraft [command]
```

## Commands

### Project Management

| Command | Description | Example |
|---------|-------------|---------|
| `project` | Create new project | `/novelcraft project` |
| `project list` | List all projects with status | `/novelcraft project list` |
| `project <number>` | Switch to project by number | `/novelcraft project 1` |
| `project <name>` | Switch to project by name | `/novelcraft project my-novel` |
| `setup` | Setup/Reconfigure project | `/novelcraft setup` |
| `setup [module]` | Configure specific module | `/novelcraft setup images` |
| `reconfigure` | Reconfigure all modules | `/novelcraft reconfigure` |
| `reconfigure [module]` | Reconfigure one module | `/novelcraft reconfigure chapters` |

### Project List Output

```
/novelcraft project list

Your NovelCraft Projects:
═══════════════════════════════════════════════════

[1] 📖 The Last Dragons
    Status: 5/12 chapters written
    Phase: Writing
    Last active: 2026-04-05

[2] 📖 Space Opera (paused)
    Status: Concept phase
    Phase: Planning
    Last active: 2026-03-28

[3] 📖 Mystery in Paris
    Status: 0/10 chapters
    Phase: Images generating...
    Last active: 2026-04-06

═══════════════════════════════════════════════════
Use "/novelcraft project <number>" to switch
```

### Available Modules

- `concept` — Genre, characters, plot, worldbuilding
- `writer` — Prolog, epilog, tone/style
- `images` — Image generation, sizes, provider, style
- `chapters` — Word count, revisions, scoring
- `publication` — PDF/EPUB formats, fonts, layout

### Info Commands

| Command | Description |
|---------|-------------|
| `help` | Show this help |
| `help [module]` | Help for specific module |
| `status` | Show current project status |
| `version` | Show version |

### Alternative Syntax (Long Form)

| Command | Description |
|---------|-------------|
| `--project` | Create new project |
| `--project-list` | List all projects |
| `--setup` | Same as `setup` |
| `--setup --module=images` | Configure images |
| `--reconfigure` | Same as `reconfigure` |
| `--help` | Show help |
| `--status` | Show project status |
| `--version` | Show version |

---

## Module: Images

`/novelcraft setup images` or `/novelcraft reconfigure images`

### Interactive Questions

1. **Enable images?** (yes/no)
2. **Provider?** (mflux-webui / mcp / manual / api / none)
3. **Image types?**
   - Cover? (yes/no)
   - Portraits? (yes/no)
   - World visuals? (yes/no)
   - Chapter visuals? (yes/no)
4. **Resolutions** (for each enabled type):
   - Width? (512/768/1024/1280/1536)
   - Height? (512/768/1024/1280/1448)
5. **Style?** (genre-match / Realistisch / Anime / Fantasy-Art / ...)
6. **Text in image?** (yes/no)
7. **Text as overlay?** (yes/no)

### Default Resolutions

| Type | Width | Height | Aspect |
|------|-------|--------|--------|
| cover | 768 | 1024 | 3:4 |
| portraits | 512 | 768 | 2:3 |
| world_visuals | 1024 | 512 | 2:1 |
| chapter_visuals | 512 | 512 | 1:1 |

---

## Module: Chapters

`/novelcraft setup chapters` or `/novelcraft reconfigure chapters`

### Interactive Questions

1. **Target word count?** (5000-10000, default: 7500)
2. **Min words?** (target - 500)
3. **Max words?** (target + 500)
4. **Max revisions?** (1-5, default: 3)
5. **Scoring enabled?** (yes/no)
6. **Strict mode?** (yes/no)
7. **Revision mode?** (auto / manual / score_based)

---

## Module: Concept

`/novelcraft setup concept` or `/novelcraft reconfigure concept`

### Interactive Questions

1. **Character count?** (2-8, default: 4)
2. **Plot structure?** (3-Akt / 5-Akt / Hero's Journey / Freestyle)
3. **Flashbacks allowed?** (yes/no)
4. **Worldbuilding depth?** (Basic / Mittel / Detailliert)

---

## Module: Writer Extras

`/novelcraft setup writer` or `/novelcraft reconfigure writer`

### Interactive Questions

1. **Prolog?** (yes/no)
2. **Prolog length?** (1500-4000, default: 2500)
3. **Epilog?** (yes/no)
4. **Epilog length?** (1000-3000, default: 2000)
5. **Tone?** (narrativ / dramatisch / locker / mysteriös / action / romantisch / düster)

---

## Module: Publication

`/novelcraft setup publication` or `/novelcraft reconfigure publication`

### Interactive Questions

1. **Formats?** (pdf / epub / both)
2. **PDF engine?** (auto / pdflatex / xelatex / lualatex)
3. **Page size?** (a4 / a5 / letter / pocket)
4. **Font?** (serif / sans-serif / monospace / custom)
5. **Font size?** (10pt / 11pt / 12pt)
6. **Line spacing?** (1.15 / 1.5 / 1.75 / 2.0)
7. **Output directory?** (default: ~/Ronny/Bücher/)

---

## Examples

```bash
# Create new project
/novelcraft project

# List all projects
/novelcraft project list

# Switch to project #2
/novelcraft project 2

# Switch by name
/novelcraft project "Space Opera"

# Configure current project
/novelcraft setup

# Configure only images
/novelcraft setup images

# Full reconfiguration
/novelcraft reconfigure

# Check help
/novelcraft help

# Show status
NovelCraft --status

# Legacy natural language (still works)
"Create NovelCraft project"
"Reconfigure module chapters"
"Show all my books"
```

---

## See Also

- [setup.md](setup.md) — Chat-based setup guide
- [project-setup.md](project-setup.md) — Complete command reference
- [references/CONFIG.md](references/CONFIG.md) — Config schema details
- [SKILL.md](SKILL.md) — Main skill documentation

---

**Version:** 3.0.0
