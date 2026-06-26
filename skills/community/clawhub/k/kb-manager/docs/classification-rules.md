# Classification Rules

Always classify by **primary purpose**, not by source website, file type, or where the content came from.

A PDF, article, transcript, webpage, or chat summary can belong to different categories depending on why the user wants to keep it.

## Category definitions

- `01_reference`: official docs, APIs, specs, commands, stable product docs, durable factual references
- `02_learning`: tutorials, walkthroughs, concept explanations, study notes, teaching-oriented materials
- `03_projects/<project-name>`: project discussions, plans, meeting notes, design docs, architecture notes, implementation decisions
- `04_research`: research, comparisons, investigations, experiments, competitor analysis, tradeoff analysis
- `05_playbooks`: SOPs, procedures, repeatable workflows, operational runbooks
- `06_prompts`: prompts, reusable instructions, agent patterns, prompt templates
- `00_inbox`: uncertain items that should not be force-classified yet

## Classification priority

When more than one category could apply, use this priority order:

1. project-specific content -> `03_projects`
2. reusable operating workflow -> `05_playbooks`
3. reusable prompt or instruction asset -> `06_prompts`
4. stable reference or specification -> `01_reference`
5. learning or explanation-oriented material -> `02_learning`
6. comparative or investigative material -> `04_research`
7. uncertain classification -> `00_inbox`

## Confidence rules

- **High confidence**: save directly into the target category
- **Medium confidence**: save into `00_inbox` and note the most likely destination
- **Low confidence**: do not force classification; ask for minimal clarification if necessary, or keep it in inbox when the user wants to preserve it first

When in doubt, prefer `00_inbox` over a wrong permanent category.
