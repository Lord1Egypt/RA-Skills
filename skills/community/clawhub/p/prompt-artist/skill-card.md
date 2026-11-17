## Description:

Optimizes and generates text-to-image prompts for Midjourney, Nano Banana, Dreamina, and Qwen, including platform variations, style, lighting and composition modifiers, negative prompts, and Chinese/English input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevo11](https://clawhub.ai/user/elevo11)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn short image ideas into platform-ready prompts, prompt variants, style guidance, and negative prompts for common AI art platforms. It can also keep local prompt history and favorites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The billing command can send SkillPay charge requests using SKILLPAY_API_KEY and may charge a user account if run automatically.

Mitigation: Require explicit user approval for each billing action, and verify the user id, amount, and intended charge before running the billing command.

Risk: Generated image prompts and platform guidance may be unsuitable for a target image model or policy context.

Mitigation: Review generated prompts, negative prompts, and style modifiers before submitting them to image generation platforms.

## Reference(s):

- [Platform Specifications](references/platform-specs.md)
- [Prompt Artist on ClawHub](https://clawhub.ai/elevo11/skills/prompt-artist)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown or plain text prompt blocks, with JSON available from script flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local prompt history and favorites; billing actions can call SkillPay when explicitly run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
