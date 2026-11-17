## Description:

Placeholder skill for image-to-image workflows on skills.video. Use when the user is asking about i2i generation and the concrete API contract has not been implemented yet.

This skill is for research and development only.

## Publisher:

[skills-video](https://clawhub.ai/user/skills-video)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this placeholder to handle image-to-image requests on skills.video without inventing unsupported API details while the concrete provider or model contract is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a placeholder and does not include a verified image-to-image API contract, endpoint, payload template, or helper command.

Mitigation: Tell users the workflow is not implemented yet, check for model-specific OpenAPI or documentation, and avoid inventing image input fields or upload semantics.

Risk: Users may expect actual image generation from this skill even though it only provides guidance.

Mitigation: Surface the limitation clearly and ask for the exact provider, model, or endpoint only when that information is necessary to continue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skills-video/skills/i2i)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance in the agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute image generation; defers real i2i execution until a verified provider or model API contract is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
