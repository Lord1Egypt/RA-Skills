## Description:

智能擦除商品图片中的人物、水印、文字及杂物，并自动补全背景，完成商品修图与素材优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request removal of watermarks, text, people, or other unwanted elements from product images, then review the generated background and product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to an online service, and generation can consume account credits.

Mitigation: Upload only intended images and use a dedicated service key.

Risk: Externally downloaded CLI releases may change or introduce issues.

Mitigation: Review or pin CLI releases and check proposed upgrade commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-image-eraser)
- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Generated images, Shell commands, Guidance]

**Output Format:** [Generated image files or URLs, with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generative edits may alter product details; review text, logos, and product structure after generation.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
