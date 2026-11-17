## Description:

批量把商品图处理成干净的纯白底图：自动识别商品主体、去除杂乱背景，适配平台白底图规范。当用户要求抠图、做白底图、去背景、商品图变纯色底、批量处理商品图背景时必须触发。关键词：LinkPix、qhkit、抠图、批量抠图、白底图、去背景、去底、纯色背景、主图白底、平台白底规范、商品图清理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营者可用它批量将商品实拍图转换为纯白背景主图，并在发布前检查生成结果中的商品文字、标识和结构。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to iqinghu.com for processing, and the service’s image-retention practices were not verified.

Mitigation: Only upload images you are comfortable sending to the service.

Risk: Generative redraw may change product text, logos, or structure.

Mitigation: Review generated images against the source before using them as product listings.

Risk: Image processing consumes account credits.

Mitigation: Check the estimate and available credit balance before processing large batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-white-background)
- [@iqinghu/qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [Generated white-background JPG/PNG images with command and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch jobs process images individually; generated redraws may change product details. Output is not a transparent alpha-channel image.]

## Skill Version(s):

0.1.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
