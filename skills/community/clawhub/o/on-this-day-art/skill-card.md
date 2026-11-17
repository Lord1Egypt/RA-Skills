## Description:

Daily AI image generation from Wikipedia On This Day events using local ComfyUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asimons81](https://clawhub.ai/user/asimons81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to configure a local Windows/WSL ComfyUI workflow that selects Wikipedia On This Day events and generates daily historical images for local use or Discord posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can start an unauthenticated ComfyUI service on all network interfaces.

Mitigation: Keep ComfyUI bound to localhost or a restricted interface, and firewall port 8188 before use.

Risk: Wikipedia event text and generated prompts are untrusted inputs that can influence image generation and downstream posts.

Mitigation: Review selected events, prompts, and generated images before enabling unattended Discord posting.

Risk: The JSONL run log may retain event text, prompts, image paths, and timestamps.

Mitigation: Periodically delete or protect the run log according to local privacy and retention needs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/asimons81/skills/on-this-day-art)
- [ComfyUI Workflow - Detailed Setup Guide](references/SETUP.md)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [StabilityMatrix](https://lynxhou.io/StabilityMatrix)
- [Wikipedia On This Day API](https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/${date_param})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG image outputs and JSONL run logs on the local machine.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
