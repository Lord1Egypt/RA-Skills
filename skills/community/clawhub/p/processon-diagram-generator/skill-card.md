## Description:

ProcessOn Diagram Generator helps agents turn natural-language or code-context requests into ProcessOn diagrams, including flowcharts, architecture diagrams, ER diagrams, org charts, timelines, roadmaps, infographics, and sketch redraws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilizhang](https://clawhub.ai/user/leilizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users can use this skill when they need an agent to create editable ProcessOn diagrams from structured or partially structured diagram requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram prompts and related context may be sent to ProcessOn.

Mitigation: Do not use the skill with secrets, proprietary architecture details, regulated data, or other sensitive information unless ProcessOn is approved for that use.

Risk: The skill stores a local bearer token for ProcessOn authorization.

Mitigation: Use it only in environments where local token storage is acceptable, and reauthorize or clear stored credentials when changing users or trust boundaries.

Risk: The skill can perform npm-based dependency setup and update flows.

Mitigation: Prefer a version pinned to a reviewed release or commit and review package installation behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leilizhang/skills/processon-diagram-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and links to generated diagram previews and editable ProcessOn files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require browser-based ProcessOn authorization before diagram generation.]

## Skill Version(s):

2.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
