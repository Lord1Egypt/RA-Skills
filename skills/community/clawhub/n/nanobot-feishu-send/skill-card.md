## Description:

Guides an agent to send local images, files, audio, and video to Feishu through nanobot's message tool, with attachments supplied through the media field.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and nanobot users use this skill to prepare Feishu attachment messages for the current chat or a specified chat_id. It helps the agent place local file paths in media, select supported attachment types, and avoid sending only path text in content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local paths placed in media upload the actual local file contents to Feishu and share them with the current or specified chat.

Mitigation: Confirm the file contents and recipient or chat_id before sending; avoid sending secrets, credentials, configuration files, or private documents.

Risk: Feishu credentials and nanobot configuration can be exposed if users share app secrets or mishandle ~/.nanobot/config.json.

Mitigation: Keep ~/.nanobot/config.json private, restrict local access to the current user, and do not disclose appSecret values in chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinyuqinfeng/skills/nanobot-feishu-send)
- [README](artifact/README.md)
- [Chinese README](artifact/README.zh-CN.md)
- [Security guidance](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, text]

**Output Format:** [Markdown guidance with JSON message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on local file paths, the media field, optional Feishu chat_id targeting, and supported attachment extensions.]

## Skill Version(s):

0.1.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
