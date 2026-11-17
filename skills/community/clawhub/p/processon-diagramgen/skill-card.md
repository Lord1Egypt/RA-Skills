## Description:

ProcessOn Diagram Generator helps agents turn natural-language or code-context requests into ProcessOn diagrams with preview and editable links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilizhang](https://clawhub.ai/user/leilizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to create editable ProcessOn flowcharts, architecture diagrams, ER diagrams, organization charts, timelines, roadmaps, infographics, and sketch redraws from prompts or code context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram prompts and included code or architecture details may be sent to ProcessOn's external service.

Mitigation: Avoid sensitive internal systems unless endpoint settings, data handling, and authorization scope are approved.

Risk: The setup flow can install or run npm tooling and store authorization tokens on the user's machine.

Mitigation: Review the setup script, use a pinned release, install mcporter deliberately, and control token storage before deployment.

Risk: The artifact directs agents to route broad diagram requests through this external service.

Mitigation: Use the skill only for explicit diagram-generation needs and review generated links and content before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leilizhang/skills/processon-diagramgen)
- [ClawHub publisher profile](https://clawhub.ai/user/leilizhang)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown text with authorization prompts, status messages, preview links, edit links, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams are returned through external ProcessOn preview and edit URLs after browser authorization.]

## Skill Version(s):

2.5.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
