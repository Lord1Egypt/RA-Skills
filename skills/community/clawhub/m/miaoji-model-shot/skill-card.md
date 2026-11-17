## Description:

Generates apparel model-shot composition plans, shooting guidance, and AI image prompts from clothing or accessory descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers, apparel brands, designers, and merchandising teams use this skill to plan model-shot concepts, multi-angle compositions, props, lighting, and AI drawing prompts for clothing product displays. It is intended for planning and prompt generation, not for creating or replacing images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is primarily Chinese-language, which may lead to misunderstanding for teams that cannot review Chinese instructions.

Mitigation: Install only where Chinese-language usage is acceptable, or ask the publisher for clearer language support before operational use.

Risk: The bundled prompt generator accepts an unbounded count value, which can produce excessive output if used carelessly.

Mitigation: Keep --count to a small reasonable number until the publisher adds bounds checking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/miaoji-model-shot)
- [Style templates](artifact/references/style-templates.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and optional JSON or plain-text output from the bundled prompt generator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces planning guidance and prompts only; it does not generate image files or call image-generation APIs.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
