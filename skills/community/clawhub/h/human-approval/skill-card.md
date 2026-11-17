## Description:

Soft human-in-the-loop approval gate. Asks the user for confirmation before the agent executes high-risk actions like deleting files, sending emails, or running destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openauthority](https://clawhub.ai/user/openauthority)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add an interactive approval checkpoint before destructive, irreversible, external, or financial actions. It is intended as a soft, conversational gate for sessions where the user is present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a soft approval helper that relies on the model to pause before high-risk actions.

Mitigation: Use it as an interactive visibility layer; for stronger enforcement, use a policy or plugin mechanism that blocks high-risk tools outside the model.

Risk: The security evidence says the release requests unrestricted Bash access even though the approval workflow should only need confirmation behavior.

Mitigation: Review tool permissions before installing and avoid granting unrestricted shell authority unless the OpenClaw environment requires it and the extra authority is acceptable.

## Reference(s):

- [Human Approval on ClawHub](https://clawhub.ai/openauthority/skills/human-approval)
- [OpenAuthority Plugin HITL Policies](https://github.com/Firma-AI/openauthority)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style conversational prompts and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces approval prompts with action, target, risk, reversibility, and approve/reject/modify response options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
