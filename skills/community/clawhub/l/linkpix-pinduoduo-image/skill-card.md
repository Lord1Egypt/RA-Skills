## Description:

通过青虎 AI 为拼多多等电商平台生成商品主图套图、详情图和促销活动图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

拼多多商家、运营人员和设计师可用它生成商品主图套图、详情长图和促销活动海报，并为商品图片制作白底或场景化视觉方案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing an API key in chat could expose account access.

Mitigation: Enter keys through a secure local configuration flow; rotate any key already shared.

Risk: Installing or automatically updating the CLI and its dependencies can introduce unreviewed software.

Mitigation: Use reviewed, pinned dependencies and retain control over updates.

Risk: Product images and prompts are sent to Qinghu AI, and confirmed generation jobs spend credits and cannot be canceled.

Mitigation: Upload only approved images and prompts, and review generation settings and the estimate before confirming a job.

## Reference(s):

- [LinkPix skill release](https://clawhub.ai/autoagc/skills/linkpix-pinduoduo-image)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Text, Shell commands, Configuration instructions]

**Output Format:** [Generated image files or image URLs, with text and shell commands for setup and generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are generated from selected options and any supplied product images or copy; image count, size, and quality depend on the request.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
