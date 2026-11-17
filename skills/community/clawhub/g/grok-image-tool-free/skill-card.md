## Description:

轻量级AI图片生成工具，通过浏览器自动化操作Grok Imagine生成并保存图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to drive Grok Imagine through browser automation for single-image generation, then save the result locally for creative drafts, social media assets, or concept validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Grok browser session through browser and desktop automation.

Mitigation: Invoke it only for explicit image-generation tasks and review browser actions before they run.

Risk: The skill may issue desktop mouse, keyboard, and shell commands to save and locate generated files.

Mitigation: Review proposed desktop-agent and shell commands, and confirm writes to the Downloads folder are acceptable.

Risk: The trigger wording is broad for an automation skill with local file-writing behavior.

Mitigation: Limit use to the documented Grok Imagine single-image workflow rather than general automation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grok-image-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Grok Imagine](https://grok.com/imagine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline browser and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an execution plan/status narrative and may guide the agent to locate generated image files in the user's Downloads folder.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
