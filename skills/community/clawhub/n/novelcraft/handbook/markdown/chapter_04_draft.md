# Chapter 4: Modules in Detail

## Module 0: Concept

**Required:** Yes  
**Order:** First

Contains:
- Genre & theme
- Characters (3-5 main figures with backstory)
- Plot (3-act structure)
- Worldbuilding (setting, rules, history)
- Flashback planning

**Template:** `module-concept-template.md`

## Module 1: Writer Extras (Prolog/Epilog)

**Required:** No  
**Order:** Prolog before chapters, epilog after

Use for:
- World introduction
- Character backgrounds
- Outlook after main plot

**Template:** `module-writer-extras-template.md`

## Module 2: Images

**Required:** No  
**Order:** Parallel to chapters

Options:
- **Provider:** MCP servers, external APIs, local tools, manual
- **Cover:** Yes/No
- **Character images:** Set count
- **Text in images:** Yes/No
- **Overlay text:** Yes/No

**Important:** Start and forget. Don't block!

**Template:** `module-images-template.md`

## Module 3: Chapters

**Required:** Yes  
**Order:** After concept

Configuration via `module-chapters.md`:

```yaml
min_words: 7000
max_words: 8000
max_revisions: 3
scoring_enabled: true
```

### Review Criteria (with weights)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| UTF-8 Encoding | ×3 (CRITICAL) | No foreign characters |
| Word Count | ×2 (HIGH) | Target: 7,500 words |
| Continuity | ×2 (HIGH) | Consistent with previous |
| Plot Progression | ×2 (HIGH) | Story advances |
| Character Voice | ×1.5 (MEDIUM) | Believable figures |
| Style & Atmosphere | ×1.5 (MEDIUM) | Fits project style |
| Grammar | ×1 (LOW) | Correct language |

**Templates:**
- `module-chapters-template.md` (Writing)
- `module-review-template.md` (Review)
- `module-revision-template.md` (Revision)

## Module 4: Publication

**Required:** Yes  
**Order:** Last

Configuration via `module-publication.md`:

```yaml
formats:
  - pdf
  - epub
pdf_engine: weasyprint  # or other
layout: standard
typography:
  font: default
  size: 12pt
```

**Template:** `module-publication-template.md`

---

*Next chapter: Tips & common problems.*
