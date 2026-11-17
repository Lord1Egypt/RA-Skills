## Description:

Manage VoIP calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage VoIP calls, automate voice-related tasks, and handle communication operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for VoIP communication authority and a VOIP_API_KEY.

Mitigation: Provide the API key only through protected secret handling and require explicit confirmation before placing, ending, or modifying calls.

Risk: The documented command references a VoIP manager script that is absent from the artifact.

Mitigation: Confirm the trusted VoIP service and script before installing or running the skill.

Risk: Broad voice and communication triggers may lead to ambiguous VoIP actions.

Mitigation: Constrain when the skill is invoked and confirm the intended action with the user before performing call operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-voip-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, JSON]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOIP_API_KEY and a trusted VoIP manager script; documented results use a JSON success/data object.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
