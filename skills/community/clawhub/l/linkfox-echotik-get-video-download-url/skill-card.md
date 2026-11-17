## Description:

Resolves a TikTok video URL into no-watermark and watermarked download URLs, playback URLs, and cover image URLs for saving or offline review of promotional video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, e-commerce operators, and agents use this skill to turn a specific TikTok video link into direct media, playback, and thumbnail URLs for asset archiving or offline analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends TikTok video URLs to LinkFox-hosted APIs and supports endpoint override through environment variables.

Mitigation: Install only if LinkFox-hosted processing is acceptable, review network actions, and keep endpoint environment variables at trusted defaults.

Risk: The bundled onboarding flow can handle account login, SMS-code based setup, billing, and payment actions.

Mitigation: Avoid entering SMS codes through the agent when possible and require explicit user review before any billing or payment step.

Risk: The skill requires a LinkFox API key and includes setup guidance that may place credentials in shell startup files.

Mitigation: Store API keys in a safer credential manager or controlled environment configuration and avoid exposing them in prompts or logs.

Risk: Automatic feedback reporting could disclose user prompts or URLs if used without review.

Mitigation: Do not send automatic feedback containing user prompts, TikTok URLs, API keys, or other sensitive task details.

## Reference(s):

- [EchoTik TikTok Video Download API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-get-video-download-url)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, guidance]

**Output Format:** [JSON response saved to disk, with stdout summary text or full JSON for small and inline responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TikTok video URL and LinkFox API key; returned download and playback URLs may expire.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
