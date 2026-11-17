## Description:

指导短视频创作者从参考视频提取脚本、改写商品卖点，并通过青虎AI生成 HappyHorse 1.1 风格的短视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Short-video creators and e-commerce teams use this skill to analyze a shared video, adapt its shot structure to a product, and request a promotional video through 青虎AI after reviewing the script and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating qhkit and providing an API key grants third-party tooling access to the video service.

Mitigation: Install only from a trusted source, prefer pinned or platform-managed dependencies, and handle the API key securely.

Risk: Reference videos, images, and prompts may be uploaded to 青虎AI.

Mitigation: Confirm permission to use the media and avoid sharing sensitive content without authorization.

Risk: Generation spends service credits and tasks cannot be cancelled after submission.

Mitigation: Show the model, inputs, duration, and estimated cost; obtain explicit approval before generation.

Risk: Video replication may copy protected footage or dialogue too closely.

Mitigation: Adapt the structure and creative approach without reproducing original media or dialogue.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-happyhorse-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with script comparisons, shell commands, and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires user approval of the script, settings, and estimated credits.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
