## Description:

Renders Chinese market charts from standardized bars data with moving averages, MACD indicators, and HTML, PNG, or JSON export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevershu](https://clawhub.ai/user/forevershu)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to generate Chinese market chart artifacts from standardized bars data for market review, reporting, or downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may be written outside the documented output folder when unsafe output stem values are used.

Mitigation: Use trusted output stem values only and add path containment before relying on generated files in shared or production workspaces.

Risk: Generated charts execute mutable remote JavaScript.

Mitigation: Pin or vendor the ECharts dependency and review generated HTML before relying on chart exports.

Risk: The security verdict requires review before installation.

Mitigation: Review the skill before installing and use it only in workspaces where generated files are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/forevershu/skills/market-chart-renderer)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [HTML, PNG, and JSON files plus JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default exports are written under output/generated/images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
