## Description:

Routes broad or cross-domain Mermail requests to focused workflows while preserving separate authorization for each action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Mermail users and agents use this skill to route ambiguous or multi-part email, workspace, integration, and wallet requests to the appropriate focused skills in a safe order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing can lead to high-impact email, workspace administration, integration, or payment actions.

Mitigation: Review the connected Mermail profile and focused skills; require separate user authorization for each action.

Risk: Untrusted email or tool content could influence workflow selection.

Mitigation: Treat inbound content as data and route only from the user's request.

## Reference(s):

- [Mermail skill documentation](https://docs.mermail.app/ai/skills)
- [Mermail skill release](https://clawhub.ai/mermail/skills/mermail)
- [Mermail routing reference](references/routing.md)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies focused skills and distinguishes completed, pending, and approval-dependent actions.]

## Skill Version(s):

1.2.13 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
