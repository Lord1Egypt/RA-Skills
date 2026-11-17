## Description:

图像处理专业版 helps agents support enterprise image-processing workflows including batch operations, responsive image generation, CDN integration, accessibility optimization, and image-quality recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and operations teams use this skill to automate web image optimization, responsive image exports, accessibility checks, CDN upload workflows, and batch processing in agent-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command and write access combined with broad image-processing triggers can modify files or run unsafe commands.

Mitigation: Review generated commands before execution, run in a constrained workspace, and require explicit approval before batch writes.

Risk: CDN uploads, webhook callbacks, and external integrations can send images or metadata outside the local environment.

Mitigation: Confirm destinations, use HTTPS endpoints, and avoid sending sensitive images or metadata unless the user has approved the transfer.

Risk: The environment-variable discovery example can expose credential-related environment metadata.

Mitigation: Do not run credential-environment discovery examples during normal image-processing use, and avoid printing environment variables in logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/image-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, log, and error fields for image-processing workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
