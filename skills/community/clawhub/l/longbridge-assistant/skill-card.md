## Description:

Monitors a Longbridge brokerage portfolio, generates portfolio charts, and provides price-alert and portfolio-analysis guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p3dp](https://clawhub.ai/user/p3dp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect Longbridge brokerage holdings, produce portfolio visualizations, and receive configurable price alerts and investment-analysis guidance. It requires Longbridge OpenAPI credentials and should be treated as informational rather than trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses brokerage API credentials and reads real holdings data.

Mitigation: Use a minimally scoped read-only Longbridge token and store ~/.longbridge/env with owner-only permissions.

Risk: Bundled examples and alert rules may expose or imply personal portfolio details.

Mitigation: Remove or replace personal alert rules and portfolio examples before publishing or sharing the package.

Risk: Setup installs dependencies before the user has reviewed exact package versions.

Mitigation: Pin and review dependencies before running setup.sh.

## Reference(s):

- [Longbridge OpenAPI](https://open.longportapp.com)
- [ClawHub skill listing](https://clawhub.ai/p3dp/skills/longbridge-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Console text with setup commands, configuration snippets, portfolio analysis, alert messages, and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local portfolio_chart.png file and depends on Longbridge API responses and matplotlib availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact documentation also references v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
