## Description:

Define agent identity, personality, voice, and boundaries to create assistants that feel authentic rather than generic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mugiwarasolos2](https://clawhub.ai/user/mugiwarasolos2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use this skill to define an assistant's identity, voice, role boundaries, adaptation style, and reusable identity templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for adapting to user preferences over time, which can create privacy or stale-preference concerns when paired with persistent memory.

Mitigation: Review or reset stored preferences when needed, and keep adaptation rules transparent and scoped to the current user context.

Risk: Agent boundary guidance may influence assistants to act autonomously within an approved scope.

Mitigation: Keep explicit confirmation requirements for spending, external communications, deletion, and other high-impact actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mugiwarasolos2/skills/help-pair)
- [Agent Voice & Personality](artifact/voice.md)
- [Agent Role Boundaries](artifact/boundaries.md)
- [Agent Learning & Adaptation](artifact/adaptation.md)
- [Agent Identity Templates](artifact/templates.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only skill with no detected credentials, MCP tools, or API calls.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
