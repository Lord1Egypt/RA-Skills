## Description:

Create AI-powered videos via the Hooked Video API, including script-to-video, prompt-to-video, UGC ads, TikTok slideshows, avatar and voice selection, video status checks, and trend discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ycfra](https://clawhub.ai/user/ycfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to help agents create, manage, and retrieve AI-generated videos through Hooked's API. It supports content workflows for social video, UGC ads, avatar-led videos, slideshows, and trend-inspired video creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts, scripts, product URLs, images, or webhook payloads may contain secrets, regulated data, or confidential business material sent to Hooked for processing.

Mitigation: Avoid sending sensitive material unless sharing it with Hooked is acceptable, and review prompts, scripts, product URLs, images, and webhook destinations before use.

Risk: The skill depends on an external Hooked API key, paid video-generation credits, rate limits, and remote service availability.

Mitigation: Install from a trusted source, keep the API key protected, monitor usage and credits, and handle rate-limit or failed-render responses in agent workflows.

## Reference(s):

- [Hooked API Documentation](https://docs.hooked.so)
- [Hooked Dashboard](https://hooked.so)
- [Hooked API Key Settings](https://hooked.so/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/ycfra/skills/hooked)
- [Publisher Profile](https://clawhub.ai/user/ycfra)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Hooked API endpoint guidance, request bodies, polling steps, webhook guidance, and video download instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
