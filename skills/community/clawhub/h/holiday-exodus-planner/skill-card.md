## Description:

Generates a Chinese holiday travel decision report with off-peak travel windows, leave suggestions, destination choices, budget ranges, and clear do/don't recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a brief Chinese public-holiday travel intent into an actionable off-peak travel plan. It is intended for holiday timing, leave-day, destination, budget, and avoid-list decisions, not for booking, visa handling, daily commuting, or generic travel inspiration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report widget loads third-party JavaScript.

Mitigation: Bundle the chart library locally, or add integrity and Content Security Policy controls if remote assets remain.

Risk: The report widget renders generated report fields as HTML.

Mitigation: Render report data with textContent or equivalent escaping, and sanitize any intentionally allowed HTML before display.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/holiday-exodus-planner)
- [Evaluation rules](references/evaluation_rules.md)
- [Report template](references/report_template.md)
- [Widget data specification](references/widget_data_spec.md)
- [Example report](references/example_report.md)
- [Holiday planning data](assets/holidays.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Chinese Markdown decision report plus optional widget JSON for visualization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured recommendations and warnings; does not book travel, compare live prices, purchase tickets, or execute external actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
