## Description:

Direct MiniMax API integration for speech synthesis, voice cloning, image generation, video generation, and music generation using local Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cytwyatt](https://clawhub.ai/user/cytwyatt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run MiniMax multimodal generation workflows from local scripts, including TTS, voice cloning, image generation, video generation, and music generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and local media, including possible voice recordings and reference images, to MiniMax.

Mitigation: Use only authorized media and avoid uploading personal or sensitive content unless the destination service and consent requirements are acceptable.

Risk: The configured MiniMax base URL can receive the MiniMax API key and uploaded media.

Mitigation: Use a dedicated revocable API key and verify that MINIMAX_BASE_URL points to the official HTTPS MiniMax endpoint before running commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cytwyatt/skills/minimax-tools-skill)
- [Publisher profile](https://clawhub.ai/user/cytwyatt)
- [Project homepage](https://github.com/cytwyatt/minimax-tools-skill)
- [MiniMax API notes](references/api-notes.md)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses from local Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is typically saved to local output files, while command results are reported as JSON.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
