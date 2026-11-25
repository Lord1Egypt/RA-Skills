## Description:

帮助短视频创作者分析热门视频的镜头结构、改写为商品脚本，并通过青虎AI生成可灵 Kling 3.0 风格的视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

短视频运营者、剪辑师和跨境卖家可用它拆解抖音、快手或 TikTok 视频的镜头节奏，再改写成适配自己商品的脚本并生成营销视频。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags requests to share an API key in chat and unpinned setup tools; the scan is partial.

Mitigation: Do not paste API keys into chat. Configure secrets through the supported local configuration or environment variable, pin and review package versions, and resolve the missing scan reference before deployment.

Risk: Reusing source video footage or dialogue may copy protected material.

Mitigation: Borrow only the structure and creative approach; rewrite the script and use original or authorized media.

## Reference(s):

- [LinkPix Kling 3.0 Clone on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-kling-3-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Text, Video, Shell commands, Configuration instructions]

**Output Format:** [Markdown scripts and guidance, shell commands, and generated video assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a reference video link and product image; model and duration depend on available options.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
