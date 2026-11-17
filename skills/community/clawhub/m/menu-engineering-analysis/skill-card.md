## Description:

Guides a Kasavana-Smith analysis of one restaurant menu over a defined sales period, classifying items by contribution margin and popularity and producing a draft operator review report with action recommendations and data-quality flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant chefs, GMs, multi-unit operators, and culinary directors use this skill to review one menu over a defined sales period before pricing, recipe, or menu-layout changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential menu, recipe-cost, vendor-term, or unit-sales data may be pasted into the agent session.

Mitigation: Use only approved agent environments for sensitive restaurant data and keep pasted inputs limited to what is needed for the draft report.

Risk: Draft recommendations could be mistaken for final pricing, recipe, or menu-layout decisions.

Mitigation: Require operator review before changing prices, recipes, printed menus, POS records, or delivery-platform listings.

Risk: Missing or implausible item-level inputs can produce misleading classifications.

Mitigation: Apply the skill's data-quality gates, flag unresolved issues, and exclude incomplete items from classification until the operator confirms the data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/menu-engineering-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Draft Markdown report with calculation tables, data-quality flags, action playbook, quick wins, menu-design recommendations, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output that requires operator review before price, recipe, menu, POS, or delivery-platform changes.]

## Skill Version(s):

0.1.2 (source: server evidence release.version and artifact CHANGELOG.md, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
