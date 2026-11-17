## Description:

Generates images from user prompts with Grok Imagine and guides saving the generated files and sending them through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and workflow teams use this skill to generate AI images from prompts in Grok Imagine, save the results locally, and optionally send selected image files through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Grok in a browser and broad desktop automation during image generation and saving.

Mitigation: Run it only for explicit Grok image-generation requests and review browser and desktop actions before allowing execution.

Risk: Generated images may be saved or sent without a clearly confirmed destination.

Mitigation: Confirm the save path, selected generated file, Feishu recipient, and message content before allowing any send action.

Risk: Prompts and generated images may be exposed to external services used by the workflow.

Mitigation: Avoid sensitive prompts or private image content unless the user has approved use of Grok and Feishu for that material.

## Reference(s):

- [Grok Imagine](https://grok.com/imagine)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/grok-image)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, files]

**Output Format:** [Markdown instructions with inline JavaScript, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image files saved locally and optionally sent through Feishu when the agent has the required browser, desktop, and messaging tools.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
