## Description:

Manage MUFI events by creating and connecting festivals, campaigns, frame templates, and frames with specified details and images via admin.muinfilm.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Authorized MUFI administrators and operators use this skill to create events, campaigns, frame templates, and frame designs, then connect those records and upload required image assets in the MUFI admin console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent changes in a live-looking MUFI admin system.

Mitigation: Use it only when authorized to administer the target MUFI environment, confirm whether the target is production or test, and review each record before saving.

Risk: An authenticated browser profile may allow the agent to act through an existing admin session.

Mitigation: Avoid using an authenticated browser profile unless you are comfortable with the agent acting through that session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/mufi-admin)
- [MUFI admin console](https://admin.muinfilm.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline browser automation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ordered admin workflow steps, required fields, image dimensions, and browser automation tips.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
