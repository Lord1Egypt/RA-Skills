## Description: <br>
AI image and video generation via Vydra.ai API. Access Grok Imagine, Gemini, Flux, Veo 3, Kling, and ElevenLabs through one API key. Agents can self-register and generate images automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShoafSystems](https://clawhub.ai/user/ShoafSystems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure Vydra API access, generate images, videos, and voice output, check credits, and route paid media-generation requests through supported model endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use paid external media-generation APIs and consume credits. <br>
Mitigation: Use a dedicated API key, monitor credit usage, and require explicit approval before registration, buying credits, or high-cost video generation. <br>
Risk: Prompts, media URLs, and generated media may be sent to or retrieved from an external service. <br>
Mitigation: Review prompts and media URLs before use, avoid sensitive inputs, and require approval before posting generated media publicly. <br>
Risk: API credentials could be exposed if stored or transmitted carelessly. <br>
Mitigation: Prefer environment variables or a secret manager, restrict credential-file permissions, and send Vydra API keys only to vydra.ai endpoints. <br>


## Reference(s): <br>
- [Vydra API Documentation](references/api-docs.md) <br>
- [Vydra](https://vydra.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/ShoafSystems/image-and-video-generation-vydra) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with inline bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes a VYDRA_API_KEY environment variable or equivalent secret-managed API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
