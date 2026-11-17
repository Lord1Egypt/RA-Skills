## Description:

Helps creators adapt a reference video's script into a MiniMax H3 product-promotion video through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to analyze a short-form reference video, adapt its script to their own product, and request a promotional video with voiceover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed if shared or stored insecurely.

Mitigation: Keep the Qinghu API key in local agent configuration and avoid sharing it beyond the intended setup.

Risk: Reference videos and product images are uploaded to an external service for processing.

Mitigation: Upload only material the user is authorized and comfortable sharing with Qinghu.

Risk: Video generation consumes credits and submitted tasks cannot be canceled.

Mitigation: Check the estimate, recap key generation parameters, and obtain explicit user approval before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-minimax-h3-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Video links]

**Output Format:** [Markdown with script comparisons, CLI commands, and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task status and charged credits; video generation uses the Qinghu service.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
