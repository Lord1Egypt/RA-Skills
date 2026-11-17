## Description:

Runs adversarial multi-agent war-room evaluations that challenge strategic proposals through Analyst, Guardian, Treasurer, Builder, and Strategist roles, then synthesize a GO, NO-GO, or REWORK ruling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scytheshan-pixel](https://clawhub.ai/user/scytheshan-pixel)

### License/Terms of Use:


## Use Case:

Developers, operators, and decision makers use this skill to stress-test strategic decisions across finance, product, engineering, and hiring before committing resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write proposal context and final reports to local files, which may expose confidential strategy material if storage locations are not controlled.

Mitigation: Require explicit approval for file writes, use sanitized proposal context, and remove stored reports when retention is not required.

Risk: The skill can spawn subagents that read shared context, increasing the chance that sensitive decision data is distributed beyond the initiating interaction.

Mitigation: Limit inputs to information approved for subagent review and disable shared temp-file context for confidential proposals.

Risk: The post-ruling checklist can store decisions in memory, commit reports to Git, or update logs, creating additional persistence paths.

Mitigation: Require explicit approval before memory, Git, or log persistence and disable those steps in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scytheshan-pixel/skills/iris-war-room)
- [Domain adaptation reference](references/domains.md)
- [Prompt templates reference](references/prompts.md)
- [Role definitions reference](references/roles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with structured tables, ruling, scenario projections, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports to local files and may direct agents to use shared temporary proposal context.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
