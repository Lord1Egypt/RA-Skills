# Artifact Options Reference

Options for each artifact type, with discussion priority levels:

- **ASK** — Must ask: large impact on output character. Fallback defaults exist for "use defaults" scenarios, but normally always ask because the choice significantly shapes the output.
- **OFFER** — Mention default, let user decide whether to change
- **SILENT** — Use default silently, unless user specifies
- **SILENT (infer or ask)** — Infer from context; ask only if ambiguous

**Global options:**
- `language` — ASK once, apply to all artifacts (default: `zh_Hant`)
- `-s/--source` — SILENT. Uses all sources by default. Only discuss if user has multiple sources and mentions targeting specific ones.

---

## Summary Table

| Artifact | ASK | OFFER | SILENT |
|----------|-----|-------|--------|
| Audio | `format` (4) | `length` (3) | description |
| Video | `format` (3), `style` (9, when non-cinematic) | — | description |
| Report | `format` (4) | — | `append` |
| Quiz | — | `difficulty` (3), `quantity` (2) | — |
| Flashcards | — | `difficulty` (3), `quantity` (2) | — |
| Slide Deck | `format` (2) | — | `length` |
| Infographic | `style` (11, suggest 2-3 popular) | `orientation` (3) | `detail` |
| Data Table | — | — | description (REQUIRED, infer or ask) |
| Mind Map | no options | — | — |

---

## Per-Artifact Details

### Audio (Podcast)

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--format` | **ASK** | `deep-dive`, `brief`, `critique`, `debate` | `deep-dive` |
| `--length` | **OFFER** | `short`, `default`, `long` | `default` |
| description | **SILENT** | free text | omit |

### Video

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--format` | **ASK** | `explainer`, `brief`, `cinematic` | `explainer` |
| `--style` | **ASK** (when non-cinematic) | `auto`, `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro-print`, `heritage`, `paper-craft` | `auto` |
| description | **SILENT** | free text | omit |

> **Warning:** `cinematic` uses Veo 3 and ignores `--style`. Generation takes 30-40 minutes. Alert the user about the time cost when they choose cinematic.

### Report

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--format` | **ASK** | `briefing-doc`, `study-guide`, `blog-post`, `custom` | `briefing-doc` |
| `--append` | **SILENT** | free text (extra instructions) | omit |

### Quiz

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--difficulty` | **OFFER** | `easy`, `medium`, `hard` | `medium` |
| `--quantity` | **OFFER** | `fewer`, `standard` | `standard` |

> Note: CLI also accepts `more`, but it behaves the same as `standard` — don't present it as an option.

### Flashcards

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--difficulty` | **OFFER** | `easy`, `medium`, `hard` | `medium` |
| `--quantity` | **OFFER** | `fewer`, `standard` | `standard` |

> Quiz and Flashcards share identical options — present them together in a single question.

### Slide Deck

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--format` | **ASK** | `detailed`, `presenter` | `detailed` |
| `--length` | **SILENT** | `default`, `short` | `default` |

### Infographic

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| `--style` | **ASK** | `auto`, `sketch-note`, `professional`, `bento-grid`, `editorial`, `instructional`, `bricks`, `clay`, `anime`, `kawaii`, `scientific` | `auto` |
| `--orientation` | **OFFER** | `landscape`, `portrait`, `square` | `landscape` |
| `--detail` | **SILENT** | `concise`, `standard`, `detailed` | `standard` |

> Suggest 2-3 popular styles (e.g., `sketch-note`, `professional`, `bento-grid`) rather than listing all 11.

### Data Table

| Option | Priority | Values | Default |
|--------|----------|--------|---------|
| description | **SILENT (infer or ask)** | free text (REQUIRED) | infer from source context |

> Description is required by the CLI. Infer from context (e.g., "summarize key metrics"); ask only if context is truly ambiguous.

### Mind Map

No options. Generate directly with `notebooklm generate mind-map`.

---

## Discussion Rules

1. **Already specified** — If the user specified an option in their message, skip it.
2. **Batch presentation** — Present all ASK/OFFER options in a single message, not one at a time.
3. **Merge identical** — Quiz + Flashcards share the same options; ask once for both.
4. **Skip empty** — Mind Map has no options; don't mention it.
5. **Data Table** — Infer description from context; only ask if truly ambiguous.
6. **"Use defaults"** — If the user says "use defaults" or similar, apply all default values and proceed immediately.
7. **Language** — Ask once as a global setting, apply to all artifacts.
