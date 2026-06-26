# Obsidian Vault → ExpertPack Migration Guide

## What the Script Does (and Doesn't Do)

`convert.py` handles the mechanical transformation:
- Copies all `.md` files to the output directory (source untouched)
- Strips Dataview blocks (query blocks have no value as static content)
- Extracts inline `#hashtags` → frontmatter `tags:`
- Converts `[text](file.md)` markdown links → `[[wikilinks]]`
- Adds EP frontmatter fields: `title`, `type`, `tags`, `pack`, `created`
- Generates `manifest.yaml`, `overview.md`, `glossary.md`, `_index.md` per directory
- Copies `.obsidian/` config so the output opens in Obsidian immediately

What it **cannot** do automatically (requires agent judgment):
- EK triage (which content has real esoteric value vs. general knowledge)
- Lead summaries (1-3 sentence blockquote at top of high-traffic files)
- `propositions/` and `summaries/` retrieval layers
- `sources/_coverage.md` research audit
- Meaningful glossary entries
- File size splitting (files >3KB should be split)

## Pack Type Decision Tree

The script auto-detects type but the agent should verify. Override with `--type` when needed.

| Vault structure signals | Inferred type |
|------------------------|---------------|
| journals/, daily/, people/, mind/ | `person` |
| concepts/, workflows/, troubleshooting/, faq/ | `product` |
| phases/, checklists/, decisions/, steps/ | `process` |
| Mix of two or more above | `composite` |
| Ambiguous / general-purpose | `product` (safe default) |

**Composite packs:** If the vault clearly covers multiple distinct domains (e.g., a person's life + their work product), create a composite with sub-pack directories. Each sub-pack gets its own `manifest.yaml`. The top-level manifest declares type `composite` and lists sub-pack paths.

## Obsidian-Specific Patterns

### Wikilinks
Obsidian uses `[[wikilinks]]` — already EP-compatible. No change needed.
Pipe aliases (`[[file|display text]]`) are preserved as-is.
Heading links (`[[file#section]]`) are preserved — the `#section` part is stripped from the wikilink target during validation but kept in the raw link.

### Tags
Obsidian supports both frontmatter `tags:` and inline `#hashtags`.
The script merges both into frontmatter `tags:`. Review the merged tags after conversion — Obsidian `#nested/tags` are converted to `nested-tags` (slash → hyphen).

### Dataview
Dataview query blocks and inline expressions are stripped entirely. They are computed views, not knowledge. If a Dataview block surfaces important aggregated information, manually write that as static content before converting.

### Daily Notes
Daily note files (typically in `daily/` or `journal/`) are assigned type `journal` and prefix `meta-`. These tend to be low-EK but high personal-knowledge for person packs. Keep in Tier 2 (searchable), not Tier 1.

### Templates
Obsidian template files (usually in `templates/` or `_templates/`) should be excluded or moved to `assets/` in the EP. They are not content.

### Attachments
Non-markdown files (images, PDFs, etc.) are not copied by the script. Reference them in frontmatter `sources:` if they are evidence for content, or ignore if decorative.

### Orphaned Notes
Notes with no incoming wikilinks are flagged as orphans by `ep-validate`. Common in freshly-converted vaults. Resolution strategies:
- Add the file to a relevant `_index.md`
- Add `[[filename]]` references from topically related files
- Delete if the content has no value

## Post-Conversion Checklist

Run in this order:

```bash
# 1. Auto-fix common issues
python3 /path/to/ExpertPack/tools/validator/ep-doctor.py /path/to/output --apply

# 2. Validate (must reach 0 errors)
python3 /path/to/ExpertPack/tools/validator/ep-validate.py /path/to/output --verbose

# 3. Fix broken wikilinks from Obsidian cross-references
python3 /path/to/ExpertPack/tools/validator/ep-fix-broken-wikilinks.py /path/to/output --apply

# 4. Re-validate
python3 /path/to/ExpertPack/tools/validator/ep-validate.py /path/to/output
```

Then (agent-assisted):
- Add lead summaries to the 5-10 most important files
- Populate `glossary.md` with domain terms
- Create `propositions/` with atomic factual statements from high-EK content
- Run `expertpack-eval` to measure EK ratio

## RAG Configuration for OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["/path/to/your/converted-pack"],
        "chunking": { "tokens": 500, "overlap": 0 },
        "query": {
          "hybrid": {
            "enabled": true,
            "mmr": { "enabled": true, "lambda": 0.7 }
          }
        }
      }
    }
  }
}
```

Files are authored at 400–800 tokens — retrieval-ready by design, no external chunker needed.

## File Size Guidance

EP target: 1–3KB per file (~200–600 words). Files above 3KB should be split on natural topic boundaries using `##` headers as split points. The validator flags oversized files as warnings. Use editorial judgment — don't split arbitrarily.
