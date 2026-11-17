## Description:

Build and operate a portable Kitchen Compass meal-planning workspace for setting up a household data root, converting recipes into the Kitchen Compass markdown contract, building and querying the dinner-and-side catalog, generating weekly dinner plans, and recording meal history while keeping reusable engine files separate from household-specific data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drewsadik-ctrl](https://clawhub.ai/user/drewsadik-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Households and agents with local filesystem access use Kitchen Compass to maintain a separate household data root, normalize recipes, query dinner and side catalogs, build weekly plans, track remembered inventory and meal history, and prepare guided weekly deal briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes a local household data folder that may contain recipes, preferences, inventory, meal history, store notes, and generated reports.

Mitigation: Use a private data root, avoid storing sensitive household details unnecessarily, and review the data root before sharing or backing it up to shared locations.

Risk: Imported recipe links or copied recipe content may carry inaccurate source details or unwanted changes into the household catalog.

Mitigation: Review imported recipe links and normalized recipe markdown before saving them as household source material.

Risk: Skipping validation can allow malformed recipe markdown to affect catalog, query, or planner output.

Mitigation: Leave validation enabled during normal catalog builds and run recipe validation after edits.

Risk: Remembered inventory is approximate household memory, not real-time stock state.

Mitigation: Require explicit inventory updates and user-confirmed usage before changing stored inventory quantities.

Risk: Weekly deal workflows are manual or guided and retailer-specific retrieval may be brittle.

Mitigation: Treat deal briefs as decision support, review per-store inputs before combining them, and do not rely on deals as automatic planner scoring.

## Reference(s):

- [Setup Flow](references/setup-flow.md)
- [Recipe Schema](references/recipe-schema.md)
- [Runtime Contract](references/runtime-contract.md)
- [Planning Logic](references/planning-logic.md)
- [Inventory Logic](references/inventory-logic.md)
- [Weekly Deal Brief and Combined Deal Sheet](references/weekly-deal-brief.md)
- [User Data Layout](references/user-data-layout.md)
- [Portable Boundary Rules](references/live-vs-portable-boundary.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text, Markdown recipe and planning views, JSON data files, and shell commands for local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local to a user-selected Kitchen Compass data root; generated files are rebuildable from authored recipes, household settings, inventory, deal inputs, and history.]

## Skill Version(s):

1.0.1 (source: server release evidence; pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
