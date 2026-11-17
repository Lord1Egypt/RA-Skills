## Description:

Restores damaged, old, and low-quality photos using Media.io OpenAPI photo enhancement, scratch and noise reduction, and black-and-white photo colorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit authorized image URLs to Media.io, poll asynchronous restoration tasks, and return edited photo preview URLs. It is suited for workflows that need API-based photo enhancement rather than local file processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-authorized image URLs to Media.io for processing, which may expose sensitive photo content to an external service.

Mitigation: Process only images the user owns or is authorized to process, and avoid sharing generated preview URLs when restored content is sensitive.

Risk: The skill depends on a MEDIAIO_API_KEY and credit-based API calls.

Mitigation: Keep API keys out of logs and responses, check credits before generation, and stop clearly when credits are insufficient.

Risk: Restored or colorized images are edited synthetic media and may be mistaken for original or verified imagery.

Mitigation: Present outputs as edited content and avoid implying identity verification or biometric certainty from generated images.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer platform](https://developer.media.io/)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-ai-photo-restorer)
- [ClawHub publisher profile](https://clawhub.ai/user/wondershare-boop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cURL examples, JSON request and response contracts, and polling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEDIAIO_API_KEY and curl; generated results are returned as Media.io preview URLs after asynchronous task completion.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
