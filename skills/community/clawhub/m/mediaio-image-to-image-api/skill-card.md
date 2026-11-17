## Description:

Transform existing images into new ones using AI via Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call Media.io image-to-image APIs for style transfer, image remixing, artistic enhancement, and task-result lookup from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Media.io API keys, prompts, image URLs, and generated task identifiers to Media.io.

Mitigation: Use only with images and prompts that are permitted by the user's Media.io account policies, and avoid private or regulated images unless that use is approved.

Risk: The security guidance notes a fixable input-validation weakness around task-result identifiers.

Mitigation: Validate or encode task IDs before passing them to the task-result helper, and keep use inside an isolated, pinned Python environment.

## Reference(s):

- [Media.io API Documentation](https://platform.media.io/docs/)
- [Media.io Developer Portal](https://developer.media.io/)
- [Media.io Pricing](https://developer.media.io/pricing.html)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/mediaio-image-to-image-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; API calls return JSON response payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key in API_KEY and sends prompts, image URLs, and task identifiers to Media.io.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
