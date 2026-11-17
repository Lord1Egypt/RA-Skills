## Description:

Generates and edits AI images for product imagery, background changes, style transfer, product compositing, and model swaps using LinkFox's multimodal image service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route image-generation and image-editing requests to LinkFox, including text-to-image, image-to-image, product compositing, background replacement, style transfer, and model swapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local reference images uploaded through the skill become public URLs for use by the image-generation API.

Mitigation: Confirm each upload with the user first, avoid sensitive or private images, and remind the user that uploaded URLs are public and temporary.

Risk: The skill uses an external paid LinkFox image service with billing and account onboarding flows.

Mitigation: Confirm cost-sensitive actions before calling the service, stop on authentication or billing errors, and route users through the documented onboarding flow only when they approve.

Risk: API keys may be exposed if copied into shell startup files or chat history.

Mitigation: Prefer a secret manager or protected environment configuration and avoid printing or storing API keys in shared logs.

Risk: Automatic feedback reporting can send task context to a separate LinkFox feedback endpoint.

Mitigation: Do not send feedback automatically unless the user explicitly approves the exact content being reported.

Risk: The skill persists generated responses and cache files in local linkfox directories.

Mitigation: Review saved response files for sensitive prompts or generated content and remove local cache/session data when it is no longer needed.

## Reference(s):

- [AI drawing API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown image display, JSON API responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated-image responses may be cached locally for 24 hours and full responses may be saved under a local linkfox session directory.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
