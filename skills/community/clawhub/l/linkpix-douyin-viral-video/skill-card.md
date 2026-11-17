## Description:

Guides agents through creating Douyin-focused product videos with the Qinghu AI service, from selecting a model and uploading media to tracking and delivering the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin merchants, livestream teams, and short-video creators use this skill to plan and generate vertical promotional videos from prompts and product images, then retrieve the finished video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service requires an API key.

Mitigation: Configure the key securely and avoid exposing it in shared output or logs.

Risk: Source images and other reference media are uploaded to the external service.

Mitigation: Upload only media you are authorized and comfortable sharing with Qinghu AI.

Risk: Generating a video spends account credits and submitted jobs cannot be canceled.

Mitigation: Show the parameters and estimated charge where available, then obtain explicit approval before submission.

Risk: Installing or upgrading qhkit changes the local tool environment.

Mitigation: Review the package installation, pin its version in controlled environments, and avoid persistent PATH changes unless intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-douyin-viral-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Video links]

**Output Format:** [Markdown text with inline commands and a video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status and credits charged; completed video is hosted by the service.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
