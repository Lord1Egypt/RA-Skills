## Description:

Placeholder skill for image-to-video workflows on skills.video. Use when the user is asking about i2v generation and the concrete API contract has not been implemented yet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-video](https://clawhub.ai/user/skills-video)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this placeholder to respond to image-to-video requests on skills.video while the concrete provider API contract is still unavailable. It helps surface the current limitation, avoid invented request fields, and guide users toward verified model or endpoint documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally incomplete and may not provide a verified image-to-video API contract, endpoint, payload template, or helper command.

Mitigation: Treat the skill as placeholder guidance and verify the provider-specific API contract, endpoint, and execution examples before using it for real image-to-video generation.

Risk: Future examples could accidentally invent undocumented image input fields or upload semantics.

Mitigation: Use model-specific OpenAPI files or documentation as the source of truth before adding request fields, upload behavior, polling, or runtime handling.

## Reference(s):

- [I2V ClawHub skill page](https://clawhub.ai/skills-video/skills/i2v)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Placeholder guidance only; no API calls, helper commands, or executable workflow are implemented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
