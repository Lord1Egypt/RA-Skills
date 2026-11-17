## Description:

全流程会议助理虾 helps users turn meeting audio into transcripts, meeting notes, action items, and confirmed Feishu task notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team operators use this skill to process Chinese meeting recordings into transcripts, summaries, and action-item lists. It can prepare Feishu task notifications for identified owners, with user confirmation required before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted audio file path could cause unsafe command execution in the transcription command.

Mitigation: Use only trusted audio file paths and rewrite the transcription step to pass paths as arguments to a fixed script before using it with untrusted files.

Risk: Meeting transcripts and Feishu messages may contain sensitive business or personal information.

Mitigation: Review generated summaries, recipient matches, and message contents before sending any Feishu notifications.

Risk: Direct curl use requires manual token and payload handling for Feishu messages.

Mitigation: Prefer the openclaw-lark tool path when available, and use the direct Feishu Message API path only after checking credentials, recipients, and JSON payloads.

## Reference(s):

- [Feishu Message API Quick Reference](references/feishu-message-api.md)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu user lookup API](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50&user_id_type=open_id)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, API calls]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples; transcript text files; Feishu message payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local SenseVoice/FunASR dependencies and Feishu credentials; asks for user confirmation before distributing tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
