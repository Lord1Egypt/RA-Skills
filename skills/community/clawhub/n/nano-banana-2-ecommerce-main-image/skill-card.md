## Description:

Nano Banana 2 电商主图 helps agents design channel-specific ecommerce product main images and run a fixed Nano Banana 2 image-generation workflow through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketplace operators, and developers use this skill to create product main-image variants for ecommerce channels while preserving product facts, crop safety, and thumbnail readability. Operators should check the target platform's current rules before publishing generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and downloads are not tightly controlled.

Mitigation: Install in an isolated virtual environment, pin dependencies where possible, and use a non-sensitive output directory until download containment is reviewed.

Risk: Reference images are uploaded to AI Hive for generation.

Mitigation: Upload only approved product images that are acceptable to send to AI Hive, and strip sensitive or unpublished information before use.

Risk: Generated ecommerce imagery can misstate product facts or imply unsupported platform affiliation, claims, prices, or certifications.

Mitigation: Review generated images against the listed SKU facts and current platform rules before publishing.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/nano-banana-2-ecommerce-main-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; the helper can return JSON task status and download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the fixed public_model_nano_banana_2 image model with user-provided prompts, optional reference images, routing mode, batch size, and model parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
