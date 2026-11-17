## Description:

Generates images from prompts and reference image URLs using LinkFox-hosted image generation models, with controls for model, resolution, aspect ratio, quality, and output count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit images from a text prompt plus one or more reference image URLs. It is suited for product images, creative variations, and batch image generation through LinkFox services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, reference image URLs, API keys, and account data to LinkFox services.

Mitigation: Use only with trusted LinkFox endpoints, review the data being submitted, and restrict access to environments containing LinkFox API credentials.

Risk: The skill can create or retrieve an API key and stores credential-bearing configuration guidance for users.

Mitigation: Confirm where API keys are stored, rotate exposed keys, and keep credential environment variables limited to sessions that need this skill.

Risk: The onboarding flow can initiate paid order flows when credits are insufficient.

Mitigation: Require an explicit user billing choice before running order commands and verify plan identifiers and payment method before purchase.

Risk: Endpoint URLs can be overridden by environment variables, which can redirect credential-bearing network calls.

Mitigation: Control `LINKFOX_TOOL_GATEWAY`, `LINKFOX_AGENT_API_URL`, `LINKFOX_LOGIN_API_URL`, and `LINKFOX_AGENT_USER_API_URL` in deployment environments.

## Reference(s):

- [AI Image Generation API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Text status messages, JSON API responses, local image file paths, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful image generation saves downloaded image files under the session media directory and writes the full API response under the session data directory.]

## Skill Version(s):

1.2.3 (source: server release evidence; artifact _meta.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
