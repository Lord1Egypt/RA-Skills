---
name: obsidian-to-expertpack
description: "Convert an existing Obsidian Vault into an agent-ready ExpertPack. Restructures vault content for EK optimization, RAG retrieval, and OpenClaw integration. Creates a copy — source vault is never modified. Use when: a user wants to make their Obsidian Vault usable by AI agents, convert OV to EP, drop their vault into OpenClaw as a knowledge pack, or make their notes RAG-ready. Triggers on: 'obsidian to expertpack', 'obsidian vault to ep', 'convert obsidian', 'OV to EP', 'obsidian agent ready', 'make my vault ai ready', 'obsidian knowledge pack', 'obsidian rag'."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
      pip:
        - pyyaml
---

# Obsidian Vault → ExpertPack

Converts an Obsidian Vault into a structured **ExpertPack** — agent-ready, RAG-optimized, and OpenClaw-compatible. Source vault is never modified; output is a clean copy.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack)

> **Companion skills:** Install `expertpack` for full EP workflows. Install `expertpack-eval` to measure EK ratio after conversion.

## Step 1: Analyze the Vault

Before running the script, inspect the vault:

1. List the top-level directories — these map to EP content sections
2. Identify the **pack type** based on structure:
   - `journals/`, `daily/`, `people/`, `mind/` → **person**
   - `concepts/`, `workflows/`, `troubleshooting/`, `faq/` → **product**
   - `phases/`, `checklists/`, `decisions/`, `steps/` → **process**
   - Mix of the above → **composite**
3. Note any `templates/` or `_templates/` folders — exclude from conversion
4. Estimate content volume and identify the highest-EK directories

The script auto-detects type (`--type auto`) but verify your judgment matches before proceeding. See `references/migration-guide.md` for the full decision tree.

## Step 2: Run the Conversion Script

```bash
python3 /path/to/ExpertPack/skills/obsidian-to-expertpack/scripts/convert.py \
  /path/to/obsidian-vault \
  --output ~/expertpacks/my-pack-slug \
  --name "My Pack Name" \
  [--type auto|person|product|process|composite] \
  [--dry-run]
```

Always do a `--dry-run` first to preview what will be converted.

**What the script produces:**
- All `.md` files copied with EP frontmatter (`title`, `type`, `tags`, `pack`, `created`)
- Inline `#hashtags` extracted into frontmatter `tags:`
- Dataview query blocks stripped (computed views, not knowledge)
- `[text](file.md)` links converted to `[[wikilinks]]`
- `manifest.yaml`, `overview.md`, `glossary.md` at pack root
- `_index.md` in each content directory
- `.obsidian/` config copied (pack opens in Obsidian immediately)

For detailed handling of Obsidian-specific patterns (nested tags, daily notes, templates, attachments): read `references/migration-guide.md`.

## Step 3: Validate & Fix

```bash
# Fix common issues first
python3 /path/to/ExpertPack/tools/validator/ep-doctor.py ~/expertpacks/my-pack-slug --apply

# Must reach 0 errors
python3 /path/to/ExpertPack/tools/validator/ep-validate.py ~/expertpacks/my-pack-slug --verbose

# Fix any broken wikilinks (cross-vault references)
python3 /path/to/ExpertPack/tools/validator/ep-fix-broken-wikilinks.py ~/expertpacks/my-pack-slug --apply
```

Do not proceed until `ep-validate` reports **0 errors**.

## Step 4: Agent-Assisted Enhancement

After validation, enhance retrieval quality:

1. **Lead summaries** — add a 1-3 sentence blockquote at the top of the 5-10 most important files
2. **Glossary** — populate `glossary.md` with domain-specific terms (this is Tier 1 — always loaded)
3. **Propositions** — create `propositions/` with atomic factual statements extracted from high-EK files
4. **EK triage** — identify low-EK files (general knowledge) and compress or remove them
5. **File size** — split files >3KB on `##` header boundaries

## Step 5: Configure RAG in OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["/path/to/your/converted-pack"]
      }
    }
  }
}
```

Restart OpenClaw after config change. The pack is now searchable in every session.

## Step 6: Measure EK Ratio

```bash
clawhub install expertpack-eval
```

Run evals to score how much esoteric knowledge the pack contains vs. what the model already knows. Target EK ratio >0.6 for high-value packs.
