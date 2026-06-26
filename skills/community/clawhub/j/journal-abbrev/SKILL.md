---
name: journal-abbrev
description: Use when looking up journal or magazine name abbreviations, converting between full names and ISO 4/MEDLINE abbreviations, processing BibTeX files for journal name standardization, or answering questions about 期刊缩写/杂志缩写. Triggers on "journal abbreviation", "abbreviate journal", "journal name", "期刊缩写", "杂志缩写", "ISO 4", "LTWA", "BibTeX journal". PROACTIVELY USE when user mentions citation formatting, reference list preparation, or manuscript submission to specific journals.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
# --- Claude Code fields above, OpenClaw/SkillsMP fields below ---
author: Agents365-ai
category: Academic Research
version: 1.0.2
created: 2026-03-29
updated: 2026-04-12
github: https://github.com/Agents365-ai/journal-abbrev
homepage: https://github.com/Agents365-ai/journal-abbrev
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📖"
    homepage: https://github.com/Agents365-ai/journal-abbrev
    os: ["macos", "linux", "windows"]
---

# Journal Abbreviation Lookup

Look up journal/magazine name abbreviations using a multi-source cascade: JabRef database (~25K journals) → AbbrevISO API (ISO 4) → NLM Catalog (MEDLINE).

**Critical rule:** Always use `jabbrv.py` for lookups. Never guess abbreviations — even common journals have non-obvious abbreviations.

## Quick Reference

| User wants... | Command |
|---------------|---------|
| Abbreviate a journal name | `python3 jabbrv.py abbrev "Nature Medicine"` |
| Expand an abbreviation | `python3 jabbrv.py expand "Nat. Med."` |
| Auto-detect direction | `python3 jabbrv.py lookup "J. Am. Chem. Soc."` |
| Fuzzy search (paginated) | `python3 jabbrv.py search "biolog chem" --limit 10 --offset 0` |
| Process a .bib file | `python3 jabbrv.py bib refs.bib` |
| Preview .bib changes (no write) | `python3 jabbrv.py bib refs.bib --dry-run` |
| Explicit .bib output path | `python3 jabbrv.py bib refs.bib --output out.bib` |
| Expand .bib abbreviations | `python3 jabbrv.py bib refs.bib --expand` |
| Batch text list | `python3 jabbrv.py batch journals.txt` |
| Batch as NDJSON stream | `python3 jabbrv.py batch journals.txt --stream` |
| Inspect cache state | `python3 jabbrv.py cache status` |
| Download missing cache files | `python3 jabbrv.py cache update` |
| Rebuild cache from scratch | `python3 jabbrv.py cache rebuild` |
| Machine-readable CLI contract | `python3 jabbrv.py schema` |
| Schema for one subcommand | `python3 jabbrv.py schema lookup` |

### Output format

Stdout is a stable JSON envelope when the CLI is **not** attached to a terminal
(piped or captured by an agent), and a human table/indented view when run on a
TTY. To force a format: `--format json|table|human|auto`. `--json` remains as a
back-compat alias for `--format json`. Flags may appear before or after the
subcommand.

Envelope shape (always the same fields for every subcommand):

- Success: `{ "ok": true, "data": ..., "meta": { "schema_version", "cli_version", "cache", "latency_ms" } }`
- Partial success (batch): `{ "ok": "partial", "data": { "succeeded": [...], "failed": [...] }, "meta": {...} }`
- Error: `{ "ok": false, "error": { "code", "message", "retryable", ... }, "meta": {...} }`

### Exit codes

| Code | Meaning |
|------|---------|
| `0`  | success (including partial success) |
| `1`  | runtime / upstream error |
| `2`  | validation / bad input (missing file, bad flag) |
| `3`  | not found (the looked-up journal does not exist) |

### Error codes (inside `error.code`)

`not_found`, `file_not_found`, `validation_error`, `runtime_error`. Each carries
a `retryable: bool` so agents can branch retry logic.

## Workflow

### Step 1: Detect Intent

| Intent | Action |
|--------|--------|
| Single journal name/abbreviation | Use `lookup` (auto-detect) or `abbrev`/`expand` (explicit direction) |
| "What's the abbreviation for X?" | Use `abbrev` |
| "What journal is X?" | Use `expand` |
| Partial or uncertain name | Use `search` for fuzzy matching |
| Fix journal names in .bib file | Use `bib` |
| List of journals to process | Use `batch` |

### Step 2: Execute

Run the appropriate `jabbrv.py` command. The script handles:

1. **Local cache lookup** (instant, ~25K journals from JabRef)
2. **AbbrevISO API** fallback (algorithmic ISO 4 abbreviation, forward only)
3. **NLM Catalog** fallback (biomedical journals, bidirectional)

First run downloads JabRef CSV cache files automatically (~2-5 MB).

### Step 3: Present Results

- Show the full name, abbreviation, and source
- Note the standard (ISO 4 vs MEDLINE) when relevant
- For .bib processing: show the change summary before confirming

## ISO 4 vs MEDLINE

Two common abbreviation standards exist:

| Standard | Periods | Example | Used by |
|----------|---------|---------|---------|
| **ISO 4** | Yes | Nat. Med. | Most publishers, BibTeX |
| **MEDLINE** | No | Nat Med | PubMed, NLM databases |

JabRef provides ISO 4 style. NLM Catalog provides MEDLINE style. AbbrevISO computes ISO 4 algorithmically from LTWA (List of Title Word Abbreviations).

## Common Abbreviation Patterns

| Word | Abbreviation | Word | Abbreviation |
|------|-------------|------|-------------|
| Journal | J. | International | Int. |
| American | Am. | European | Eur. |
| Science/Sciences | Sci. | Medicine/Medical | Med. |
| Biology/Biological | Biol. | Chemistry/Chemical | Chem. |
| Physics/Physical | Phys. | Engineering | Eng. |
| Research | Res. | Review/Reviews | Rev. |
| Society | Soc. | National | Natl. |
| Proceedings | Proc. | Transactions | Trans. |
| Letters | Lett. | Communications | Commun. |
| Applied | Appl. | Computational | Comput. |

**Note:** Single-word titles (e.g., "Nature", "Science", "Cell") are NOT abbreviated per ISO 4 rules.

## Integration Examples

### With Zotero

```bash
# Export BibTeX from Zotero, then standardize journal names
zot export COLLECTION_KEY --format bibtex > refs.bib
python3 jabbrv.py bib refs.bib
```

### With LaTeX

```bash
# Before compiling, ensure all journal names are abbreviated
python3 jabbrv.py bib references.bib
# Use the output file (references_abbrev.bib) in your LaTeX document
```

### Batch Processing

Create a text file with one journal name per line:

```
Nature Medicine
Journal of Biological Chemistry
Proceedings of the National Academy of Sciences
```

Then run:

```bash
python3 jabbrv.py batch journals.txt
```

## Troubleshooting

| Issue | Solution |
|-------|---------|
| "No result found" | Try `search` with partial name for fuzzy matching |
| Cache download fails | Check network connection, retry with `update-cache` |
| Wrong abbreviation style | JabRef = ISO 4 (with dots), NLM = MEDLINE (no dots) |
| BibTeX field not detected | Ensure format is `journal = {Name}` (curly braces) |
