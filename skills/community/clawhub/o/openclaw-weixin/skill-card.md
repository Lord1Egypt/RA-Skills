## Description:

OpenClaw Weixin Channel connects OpenClaw agents to WeChat through QR-code login, inbound message polling, and outbound text, image, video, voice, and file replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alichor](https://clawhub.ai/user/alichor)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to let an agent receive WeChat messages and respond with text, rich media, and files after a QR-code account authorization flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File upload, URL download, log upload, and token logging behavior could expose local files, logs, credentials, or context tokens.

Mitigation: Review the plugin before installation, run it in an isolated OpenClaw environment, avoid debug logging during login, and treat stored Weixin credentials and context-token files as secrets.

Risk: The log-upload command can send local log files to a remote endpoint.

Mitigation: Use the log-upload command only with a trusted HTTPS endpoint and confirm the target URL before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alichor/skills/openclaw-weixin)
- [OpenClaw install documentation](https://docs.openclaw.ai/install)
- [README.md](artifact/README.md)
- [API type definitions](artifact/src/api/types.ts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [WeChat channel messages, media attachments, file transfers, and Markdown setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the OpenClaw CLI and QR-code WeChat login; plugin line 2.0.x supports OpenClaw >=2026.3.22.]

## Skill Version(s):

2.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
