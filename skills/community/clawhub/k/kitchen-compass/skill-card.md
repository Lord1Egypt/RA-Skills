## Description: <br>
Build and operate a portable Kitchen Compass meal-planning workspace for setup, recipe normalization, catalog querying, weekly dinner planning, inventory updates, weekly deal briefs, and meal history while keeping reusable engine files separate from household data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drewsadik-ctrl](https://clawhub.ai/user/drewsadik-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Kitchen Compass to create a local household meal-planning data root, normalize recipes into a stable markdown contract, query dinner and side options, generate weekly plans, record meal history, manage remembered inventory, and prepare manual weekly deal briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes household recipes, preferences, inventory notes, store/deal notes, and meal history in the selected data root. <br>
Mitigation: Use a dedicated Kitchen Compass data root and keep sensitive household notes out of that folder if they should not be available to the agent. <br>
Risk: Recipe pages, retailer URLs, and weekly deal notes can be stale, incorrect, or unsuitable for the household. <br>
Mitigation: Review recipe sources, retailer URLs, and curated deal briefs before asking the agent to rely on them for planning. <br>
Risk: Remembered inventory is approximate household memory, not a real-time stock system. <br>
Mitigation: Use explicit inventory updates and confirmed-use commands, and treat planner inventory boosts as decision support rather than proof that ingredients are available. <br>


## Reference(s): <br>
- [Kitchen Compass ClawHub release page](https://clawhub.ai/drewsadik-ctrl/kitchen-compass) <br>
- [Kitchen Compass setup flow](references/setup-flow.md) <br>
- [Kitchen Compass runtime contract](references/runtime-contract.md) <br>
- [Kitchen Compass recipe schema](references/recipe-schema.md) <br>
- [Kitchen Compass planning logic](references/planning-logic.md) <br>
- [Kitchen Compass inventory logic](references/inventory-logic.md) <br>
- [Weekly Deal Brief and Combined Deal Sheet](references/weekly-deal-brief.md) <br>
- [Kitchen Compass user-data layout](references/user-data-layout.md) <br>
- [Kitchen Compass portable boundary rules](references/live-vs-portable-boundary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated JSON and Markdown household planning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes a user-selected local household data root; generated planning, query, history, inventory, and deal outputs are rebuildable from authored household files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
