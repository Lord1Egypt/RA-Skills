## Description:

Guides an agent to create a 30-second Kling 4 action montage from three or four key frames, then select and cut the usable seconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use the skill to plan a fast-paced AI action montage from reference stills, send a generation request through Varg, and trim the strongest moments into a shorter clip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and prompts are sent to Varg and downstream model providers for processing.

Mitigation: Avoid private or sensitive material unless you understand and accept how it will be processed.

Risk: The installation example does not pin a version.

Mitigation: Review the install target and pin the intended release version when reproducibility matters.

Risk: The security scan was partial because two local references could not be resolved, so the evidence is incomplete.

Mitigation: Review the unresolved references and reassess the skill when complete scan evidence is available.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vargai/skills/kling-4-action-montage)
- [Varg how-to](https://varg.ai/how-to)
- [Varg MCP server](https://mcp.varg.ai/mcp)
- [Kling 4 Halloween film reference](https://www.youtube.com/watch?v=WzXKggH-0Io)

## Skill Output:

**Output Type(s):** [Video-generation prompts, Shell commands, Guidance]

**Output Format:** [Markdown guidance with prompt examples and bash, curl, and ffmpeg commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for a 30-second take and trimming selected segments; generation requires a Varg account or API key and may incur provider charges.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
