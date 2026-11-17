## Description:

Use MiniMax image-01 model to generate images from text prompts. Supports high-quality PNG output, downloaded from Hailuo CDN. Install when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to generate image files from text prompts through MiniMax's image-01 model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and any invoked text-to-speech text are sent to MiniMax or the configured endpoint.

Mitigation: Use only prompts and text that are appropriate to share with the configured service, and confirm the endpoint is trusted before execution.

Risk: The security summary reports undeclared text-to-speech behavior and overbroad network handling that could expose user content or an API key.

Mitigation: Review the skill before installation, prefer a revised version that documents or removes TTS, and restrict MINIMAX_BASE_URL to trusted HTTPS MiniMax hosts.

Risk: Generated media is downloaded from a returned URL without documented validation of URL trust or response size.

Mitigation: Validate generated media download URLs and sizes before using outputs in sensitive workflows.

Risk: The security guidance identifies temporary-file creation that should be replaced with secure temporary-file handling.

Mitigation: Use a revised implementation with secure temporary-file creation before production deployment.

## Reference(s):

- [MiniMax Platform](https://platform.minimax.io)
- [MiniMax API endpoint](https://api.minimax.io)
- [ClawHub skill page](https://clawhub.ai/jlin53882/skills/minimax-img)
- [Publisher profile](https://clawhub.ai/user/jlin53882)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSON response containing a local media path, source URL, and file size]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image mode writes a PNG file to a local temporary path and returns the generated media URL.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
