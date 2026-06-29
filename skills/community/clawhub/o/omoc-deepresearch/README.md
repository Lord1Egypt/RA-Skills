# Deep Research

Source-grounded deep research workflow for OpenClaw.

Use `/deepresearch <question>` when a quick answer is not enough: literature
mapping, due diligence, state-of-the-art reviews, factual investigations, or
research that needs to survive context resets.

## What It Does

- creates a durable ledger under `.deepresearch/<slug>/`
- splits work into research lanes
- records sources, atomic claims, notes, and confidence
- keeps evidence separate from inference
- supports resumable long-running research
- composes with OMOC/team/ralph for parallel or repeated research cycles

## Commands

```bash
python scripts/deepresearch.py init --question "What should we believe about X?" --slug x
python scripts/deepresearch.py lane add --slug x --name "counterevidence" --question "What would falsify this?"
python scripts/deepresearch.py source add --slug x --title "Paper or source title" --url "https://..." --kind paper --reliability high
python scripts/deepresearch.py claim add --slug x --text "Atomic factual claim" --source S001 --status supported --confidence high
python scripts/deepresearch.py note add --slug x --text "Interim synthesis or open question"
python scripts/deepresearch.py brief --slug x
```

## Quality Bar

Deep Research is deliberately conservative: it builds an evidence ledger first,
then synthesizes. Important claims should have sources, uncertainty should be
visible, and conflicting evidence should be kept instead of smoothed away.

For scientific or technical work, prefer primary papers, reviews, official docs,
and authoritative databases. For recent or unstable facts, browse and cite fresh
sources.
