## Description:

用户明确指定 GPT Image 2.6 / 智慧模型2.6，要做通用文生图、图生图、智能修图、创意插画或画质增强时使用。明确指定电商主图、白底图、场景图、投流图等用途时，优先使用对应的 2.6 专项技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商、设计、营销和办公用户可用此技能按文字提示生成图片，或用参考图进行创作、背景替换、细节优化和创意修图。它也可生成商品图、海报、插画和场景效果图。

### Deployment Geography for Use:

Global; the documented setup uses Qinghu's CN site.

## Known Risks and Mitigations:

Risk: Prompts and selected reference images are sent to Qinghu.

Mitigation: Tell users where their prompts and images are sent, and include only reference material they are authorized to share.

Risk: Image generation spends credits.

Mitigation: Estimate and present the cost, then obtain user confirmation and verify sufficient balance before generating.

Risk: The external qhkit CLI implementation was not audited, and QHKIT_BASE_HOST can override the configured environment.

Mitigation: Verify the CLI package and any QHKIT_BASE_HOST override before providing a token; keep tokens out of task JSON and replies.

Risk: Generative repainting can change image details, so it may not preserve pixels or existing text exactly.

Mitigation: Keep the original image and check the generated result; use a non-generative workflow when exact pixel-level repair or text preservation is required.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-generate)
- [Qinghu API Keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Image files, JSON, Text, Shell commands]

**Output Format:** [Generated image files; JSON request and result files; text prompts and status reports.]

**Output Parameters:** [Model, prompt, size preset, quality, language, image count, and optional reference images.]

**Other Properties Related to Output:** [Prompts are limited to 5,000 characters. Generated results should be checked for image count, dimensions, format, visual consistency, and key text.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
