## Description:

Manage social publishing, scheduled posts, and content workflows in Postiz via the Postiz API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to create, schedule, review, and manage social media posts and publishing queues in Postiz through connected ClawLink tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and enable a persistent third-party ClawLink plugin without a pinned version or integrity check.

Mitigation: Review the ClawLink plugin provenance before installing, prefer a pinned or verified release if available, and remove or disable the plugin when the Postiz integration is no longer needed.

Risk: Connected Postiz actions may publish, edit, or delete social content.

Mitigation: Preview write operations and confirm the target resource and intended effect with the user before executing create, update, or delete calls.

## Reference(s):

- [Postiz](https://postiz.com/)
- [Postiz API Documentation](https://docs.postiz.com/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postiz-social)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [Postiz Social Publishing on ClawHub](https://clawhub.ai/hith3sh/skills/postiz-social)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live Postiz tool discovery through ClawLink before acting on specific capabilities.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
