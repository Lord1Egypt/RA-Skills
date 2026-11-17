## Description:

Generates short-lived, mobile-friendly ngrok preview links for local artifacts and optionally shares them in Telegram so users can view OpenClaw outputs remotely without manual file transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wynnsu](https://clawhub.ai/user/wynnsu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to publish task-specific generated files through a temporary ngrok preview link, especially when the user needs to inspect outputs on a phone or remote device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public ngrok preview links can expose selected artifacts to anyone with the URL and may remain reachable beyond the advertised expiry if not stopped.

Mitigation: Publish only narrow, non-sensitive task artifacts; use a short TTL; run the provided down command with --delete-session-dir when the preview is no longer needed; and run cleanup for expired sessions.

Risk: Unsafe session identifiers or broad directory sources can expand the amount of local data copied into the preview cache or affect cleanup behavior.

Mitigation: Use simple task-bound session IDs without path characters, avoid workspace-root or broad directory sources, and verify status before deleting session data.

## Reference(s):

- [Ngrok Preview Troubleshooting](references/troubleshooting.md)
- [ngrok download](https://ngrok.com/download)
- [ClawHub skill page](https://clawhub.ai/wynnsu/skills/ngrok-preview)
- [Publisher profile](https://clawhub.ai/user/wynnsu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The preview command returns public_url, expires_at, session_id, stop_command, and status_command.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
