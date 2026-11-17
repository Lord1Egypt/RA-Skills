## Description:

Processes images and videos for watermark removal and quality restoration using Kaipai AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaipai](https://clawhub.ai/user/kaipai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to remove watermarks or restore image and video quality through Kaipai AI. Processing sends selected media to Kaipai and consumes account quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media is sent to Kaipai and processing consumes paid account quota.

Mitigation: Obtain clear authorization for the media upload and quota use before processing; disclose all quota-consuming stages for multi-stage work.

Risk: Optional messaging delivery uses account credentials and sends results to a conversation; saved result links may expose processed media.

Mitigation: Protect messaging credentials and result links, and send results only to the intended conversation.

Risk: Billing or recovery details may depend on current server guidance.

Mitigation: Check the Kaipai account administrator or official server-provided billing and recovery guidance; do not assume prices or plan terms.

## Reference(s):

- [Kaipai on ClawHub](https://clawhub.ai/kaipai/skills/kaipai-skill)
- [Multi-platform delivery](docs/multi-platform.md)
- [IM attachment handling](docs/im-attachments.md)
- [Error handling and polling](docs/errors-and-polling.md)
- [Feishu video delivery](docs/feishu-send-video.md)

## Skill Output:

**Output Type(s):** [Images, Videos, Text]

**Output Format:** [Processed image or video files and result URLs, with a concise status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processing uses Kaipai account quota; optional delivery sends results to a selected conversation.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
