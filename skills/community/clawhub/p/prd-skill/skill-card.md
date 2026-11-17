## Description:

Generate structured Product Requirements Documents (PRD) from natural language user requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tc1993](https://clawhub.ai/user/tc1993)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and developers use this skill to turn natural-language app or feature ideas into structured PRDs covering functional requirements, user flows, technical specifications, and implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save PRDs and start downstream development workflow steps without an explicit confirmation gate.

Mitigation: Require user confirmation before writing PRDs to disk or sending generated requirements to other skills or sessions.

Risk: Generated PRDs may contain incorrect assumptions or sensitive business details from the user's requirements.

Mitigation: Review generated PRDs before downstream implementation and avoid forwarding sensitive content unless the user has approved it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tc1993/skills/prd-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown PRD with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized requirements, user flows, technical specifications, assumptions, and downstream workflow guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
