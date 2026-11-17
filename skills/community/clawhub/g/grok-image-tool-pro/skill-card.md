## Description:

Grok图片生成-专业版 helps agents automate batch image-generation workflows with prompt queues, browser automation, local file export, post-processing, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to generate and manage batches of Grok images, export them in common image formats, and coordinate downstream post-processing or delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command and file access may affect local files outside the intended image workflow.

Mitigation: Run the skill only with explicit output directories and review any proposed file or shell actions before execution.

Risk: Browser automation may operate against an already logged-in Grok session.

Mitigation: Use a dedicated browser profile or account session and confirm prompts and actions before generation.

Risk: Generated images may be sent to Feishu or callback destinations.

Mitigation: Confirm messaging destinations and callback URLs before enabling delivery steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grok-image-tool-pro)
- [Grok Imagine](https://grok.com/imagine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser automation, local file writes, image post-processing, callback notification, and optional Feishu delivery.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
