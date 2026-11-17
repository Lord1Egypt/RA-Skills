## Description:

为商品图片批量添加品牌 logo 或版权文字水印，支持控制位置、透明度和大小，帮助保护原创素材并提升品牌辨识度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketplace operators, and developers use this skill to prepare local ImageMagick or ffmpeg commands for adding logo or copyright watermarks to single images or image batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local ImageMagick or ffmpeg commands and may require installing ImageMagick.

Mitigation: Confirm the local tools and package sources before execution, and review generated commands before running them.

Risk: Batch watermark runs can write many output files and may overwrite originals if paths are chosen incorrectly.

Mitigation: Review output paths before execution and prefer a separate output directory such as watermarked/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-image-watermark-add)
- [QHKit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include output directory guidance and generated file list instructions for batch watermark runs.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
