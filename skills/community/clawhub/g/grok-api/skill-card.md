## Description: <br>
Calls the xAI Grok API through a LeonAI proxy for text chat, reasoning, image generation and editing, and video generation using an OpenAI-compatible interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lygjoey](https://clawhub.ai/user/lygjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send prompts and media generation requests to Grok models through a configured LeonAI proxy, including chat, reasoning, image, and video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media requests, and the Grok API key are sent to the configured LeonAI proxy or GROK_BASE_URL endpoint. <br>
Mitigation: Install only if the proxy and endpoint are trusted, use a dedicated revocable key, and avoid sending secrets, personal data, or regulated information. <br>
Risk: API use can consume quota or incur billing through the configured Grok-compatible service. <br>
Mitigation: Monitor usage and billing limits, and keep the API key scoped and revocable. <br>
Risk: Image generation examples expose an option to enable NSFW output. <br>
Mitigation: Disable NSFW generation unless the deployment policy permits it and review generated media before use or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lygjoey/grok-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and CLI or API responses as text, JSON, and media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROK_API_KEY and uses GROK_BASE_URL, defaulting to a LeonAI proxy; generated image and video URLs may expire.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
