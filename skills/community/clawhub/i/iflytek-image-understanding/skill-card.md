## Description:

Iflytek Image Understanding analyzes a single JPG or PNG image with iFlytek Spark Vision and returns a description or an answer to a user question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to describe image contents, ask visual questions, or extract information from a selected image through iFlytek's image-understanding service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected image contents and prompts are sent to iFlytek's remote image-understanding API.

Mitigation: Use only images and prompts approved for iFlytek processing, and avoid sensitive documents, faces, receipts, screenshots, or proprietary images unless that processing is acceptable under your policies.

Risk: The skill requires user-provided iFlytek credentials.

Mitigation: Provide credentials through managed environment variables or a secrets manager, limit access to them, and rotate them if exposure is suspected.

## Reference(s):

- [iFlytek Image Understanding Service](https://www.xfyun.cn/services/image_understanding)
- [iFlytek Image Service Console Documentation](https://console.xfyun.cn/services/image)
- [ClawHub Skill Page](https://clawhub.ai/iflytek.skills/skills/iflytek-image-understanding)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text response, with optional raw WebSocket JSON frames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-image, single-turn command output; supports JPG, JPEG, and PNG images up to 4MB; response token limit is configurable from 1 to 8192.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
