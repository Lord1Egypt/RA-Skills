## Description: <br>
Kaipai processes images and videos through paid Kaipai API tasks for watermark removal and quality restoration, using inline execution for image jobs and spawned worker sessions for video jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaipai](https://clawhub.ai/user/kaipai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to submit media to Kaipai for image or video watermark removal, image restoration, or video quality restoration. It is suited for workflows where the user has configured Kaipai credentials and accepts paid API quota consumption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses paid Kaipai account quota and requires MT_AK and MT_SK credentials. <br>
Mitigation: Configure credentials only for accounts authorized for this use case, and make users aware that successful processing consumes account quota. <br>
Risk: Media inputs and outputs may be uploaded over the network and delivered through Feishu or Telegram helpers. <br>
Mitigation: Use the skill only for user-requested media and intended chat recipients; avoid internal, private, or arbitrary recipient flows unless explicitly trusted. <br>
Risk: Chat delivery can require Feishu or Telegram bot credentials. <br>
Mitigation: Limit bot credentials to the intended workspace or chat scope and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Kaipai Skill Page](https://clawhub.ai/kaipai/kaipai-skill) <br>
- [README](README.md) <br>
- [Agent Instructions](SKILL.md) <br>
- [Errors, Polling, and Environment Tuning](docs/errors-and-polling.md) <br>
- [IM Attachments](docs/im-attachments.md) <br>
- [Multi-Platform Delivery](docs/multi-platform.md) <br>
- [Feishu Video Send](docs/feishu-send-video.md) <br>
- [SDK README](sdk/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented CLI guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce media result URLs and chat delivery instructions after successful Kaipai processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
