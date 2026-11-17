## Description:

Guides agents in creating Xiaohongshu product-promotion videos through the qhkit video-generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Xiaohongshu creators, buyers, and marketing teams use this skill to plan and request short product videos, including vlogs, unboxings, and image-to-video promotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference media is shared with the qhkit service.

Mitigation: Upload only media the user agrees to share with the service.

Risk: Installing qhkit or Node introduces ordinary setup and software supply-chain exposure.

Mitigation: Prefer a vetted or pinned qhkit installation and review global npm or Node setup before allowing it.

Risk: A disclosed qhkit API key could allow unauthorized service use.

Mitigation: Keep the key confidential and use a scoped, revocable credential where possible.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-xiaohongshu-viral-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Video links]

**Output Format:** [Markdown with qhkit commands, task updates, and generated video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires user confirmation before submitting a credit-consuming task.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
