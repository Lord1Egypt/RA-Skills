# Data Pipeline, Format Choices, and Maintenance Notes

## Overview
This skill's intelligence comes from 33 high-quality structured descriptions of the Liberating Structures, plus the selection guidance in `ls-selection-guide.md`. All raw acquisition and structuring is done via local development scripts; the published package contains only the final clean reference data.

## Build Pipeline
1. `scripts/ls_crawler.py` — Polite scraper that walks the official LS menu and downloads the 33 individual structure pages into `raw/`.
2. `scripts/ls_structurizer.py` — LLM-assisted (via Grok Build delegation) parser that extracts every field (`what_is_made_possible`, `steps`, `tips_and_traps`, `examples`, `riffs_and_variations`, etc.) into machine-readable files.
3. Manual review + format conversion step (this session).

The `scripts/` directory and `raw/` are intentionally excluded from the ClawHub package via `.clawhubignore`.

## Format Evolution: JSON → YAML with Literal Blocks
**Initial choice (v0.1–0.2):** JSON was selected for maximum machine-parsing reliability and to avoid indentation/escaping issues while the LLM was generating the structured output.

**User-driven change (this session):** After the user explicitly asked "為什麼要用JSON，而不是用YAML或Markdown?", the team re-evaluated.

**Decision and rationale:**
- Switched all 33 structures to `.yaml`.
- Any field containing newlines (long prose such as `what_is_made_possible`, `steps`, `tips_and_traps`, `purposes`, etc.) is now emitted as a YAML literal block scalar using the `|` style.
- This produces clean, paragraph-wrapped, highly readable text for both humans and LLMs reviewing or editing the data.
- PyYAML with a custom representer still guarantees reliable round-tripping and parsing.
- Result: far better maintainability and reviewability with no loss of structure.

**Trade-off summary (documented for future skill authors):**
- JSON: Excellent machine stability, but long strings become ugly one-line blobs or escaped.
- Markdown: Human-friendly but poor for precise field extraction and LLM grounding.
- YAML + literal blocks: Best of both worlds for knowledge-heavy skills that contain substantial natural-language content.

## Maintenance Commands (Local Development Only)
```bash
# Re-structure after manual fixes to raw data
python scripts/ls_structurizer.py

# Full re-crawl (use sparingly — the site is stable)
python scripts/ls_crawler.py
```

Never commit `raw/` or regenerated files to the published package.

## Lesson for Other Knowledge Skills
When building reference data that includes long-form facilitation, design, or domain prose:
- Prefer YAML literal block scalars (`|`) over JSON strings.
- Keep the published surface minimal (only the final structured assets).
- Encode the "why this format" decision in a `references/` file so future maintainers understand the history and do not regress.

This approach was validated during the development of this skill itself.

## Related
- `references/ls-selection-guide.md`
- `.clawhubignore` (excludes development artifacts)
- Main `SKILL.md` (see "Core Design Principle" and "Current Data Assets")