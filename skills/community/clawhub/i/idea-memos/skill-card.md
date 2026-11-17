## Description:

小龙虾备忘录 — 记录即时想法，让 AI 更好辅助创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwbwbw](https://clawhub.ai/user/lwbwbw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a lightweight memo service for recording, searching, updating, and deleting idea notes through a web UI, CLI, and HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memo data may be exposed by an unauthenticated network service.

Mitigation: Run only on trusted machines and networks unless the service is bound to localhost, authentication is added, and wildcard CORS is removed.

Risk: System-level nginx setup guidance can alter host web server configuration.

Mitigation: Review each nginx command before use and avoid blindly removing the default site.

Risk: Memo deletion is permanent unless backups exist.

Mitigation: Back up the SQLite database before bulk changes or before using deletion workflows on important notes.

Risk: The web UI needs tag escaping fixes according to the security guidance.

Mitigation: Fix tag rendering before exposing the UI beyond a trusted local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwbwbw/skills/idea-memos)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite memo store and exposes web, CLI, and HTTP API workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
