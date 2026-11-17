## Description:

Auto meeting notes and action item execution loop. Trigger this skill whenever the user mentions meeting notes, meeting summary, action items, follow-up, transcript, recording, Zoom summary, Teams meeting, Tencent Meeting, Feishu meeting, WeCom meeting, upload audio, upload video, meeting template, task creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, meeting owners, and operators use this skill to turn meeting transcripts or recordings into notes, decisions, and action items, then optionally push follow-up work to Notion, Feishu, or WeCom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings and transcripts may contain sensitive information, and cloud transcription can send audio to OpenAI when enabled.

Mitigation: Use local privacy mode for sensitive meetings and require an explicit user choice before enabling cloud transcription.

Risk: The security evidence reports unrelated review instructions, hidden promotional links, and under-scoped network behavior.

Mitigation: Review the skill before installation, remove unrelated review/promotion content, and validate all outbound URLs before use.

Risk: The recording downloader accepts external URLs and the security guidance calls for download size limits.

Mitigation: Restrict downloads to trusted sources and enforce configured file size limits before processing recordings.

Risk: Optional integrations require API keys for Feishu, WeCom, Notion, OpenAI, and SkillPay.

Mitigation: Use test credentials during review, store secrets only in a local .env file, and configure only the services needed for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dttnpole-commits/skills/meetingos)
- [MeetingOS API integration guide](artifact/api_integrations.md)
- [Notion integrations](https://www.notion.so/my-integrations)
- [Feishu OpenAPI](https://open.feishu.cn/open-apis)
- [WeCom API token endpoint](https://qyapi.weixin.qq.com/cgi-bin/gettoken)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, task text, Python helper code output, shell commands, and service configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local transcript text, meeting-note Markdown, action-item summaries, and optional outbound API updates when the user configures credentials.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
