# Kitchen Compass portable boundary rules

## Goal
Keep the reusable engine inside the skill and keep real household state outside it.

## What ships in the skill

Ship only portable material:
- `SKILL.md`
- reusable scripts under `scripts/`
- contract/setup/layout references under `references/`
- reusable assets such as the recipe template
- sample household seed content with placeholder values only

## What belongs in the household data root

Keep real user state outside the skill:
- `household/*.json`
- `recipes/*.md`
- `inventory/items.json`
- `inventory/transactions.jsonl`
- optional notes like `inventory/freezer.md`
- optional manual deal inputs like `deals/weekly-deal-brief-input.json`
- `history/events.jsonl`

## What should not ship as portable source

Do not treat these as packaged source assets:
- generated query, planner, or rendered deal-brief outputs under `generated/`
- project reports, extraction notes, or one-off implementation docs
- real household recipes, freezer contents, manual weekly deal inputs, history, or family-specific notes

## Canonical-source rule

The installed skill directory is the canonical source for portable engine behavior, templates, and contract docs.

If a separate live or development workspace also exists:
- treat that copy as a consumer or mirror, not a second equal source of truth
- update the skill copy first for any shared engine or contract change
- sync the mirror in the same work item, or explicitly record that sync is still pending
- do not land independent behavioral edits in both copies and hope they stay aligned

## Privacy and portability rule

A packaged skill may ship placeholders and templates, but it should never carry a real household inside the skill directory.
