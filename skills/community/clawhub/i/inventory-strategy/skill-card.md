## Description:

Generates retail inventory health diagnostics and action strategies using sell-through rate, stock-to-sales ratio, category quadrants, item drill-downs, and HTML/XLSX reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators, planners, and inventory analysts use this skill to diagnose inventory health, locate risky categories or brand-season combinations, and generate staged action plans. The workflow depends on an authorized metric-query skill for inventory and sales metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on metric-query access to inventory and sales data.

Mitigation: Install and run it only where the metric-query dependency is trusted and authorized for the relevant business data.

Risk: Generated HTML reports and XLSX action plans may contain commercially sensitive inventory, pricing, brand, and season data.

Mitigation: Store, transmit, and share generated files according to the organization's business data handling rules.

Risk: Operational recommendations can be misleading if metric names, time constraints, or source data are incorrect.

Mitigation: Confirm metric and dimension names through the required gateway search, preserve the specified time constraints, and review outputs before acting on promotions, replenishment, or clearance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/inventory-strategy)
- [Final HTML report specification](artifact/references/report-html-spec.md)
- [Step 1.5 dynamic health sensing reference](artifact/references/dynamic-sensing.md)
- [Quadrant classification and action-rule code](artifact/references/classify-code.py)
- [Stage 1 HTML output template](artifact/references/step2-output-template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON query payloads, generated HTML reports, and XLSX action plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged outputs and pauses for user confirmation between diagnosis, drill-down, and action-plan phases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
