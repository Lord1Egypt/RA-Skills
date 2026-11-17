## Description:

Multi Agent Group Chat forwards sub-agent replies from sessions_send tasks back to the originating Telegram or Feishu group chat after automatically detecting the source chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to let multiple OpenClaw agents coordinate in shared Telegram or Feishu group chats, with sub-agent results posted back for group visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agent replies may be posted into shared group chats without enough per-chat control.

Mitigation: Enable the skill only in groups where participants consent to automatic posting, and prefer deployments with per-chat opt-in and destination allowlists.

Risk: Incorrect or overly broad session metadata could route a reply to the wrong chat.

Mitigation: Use hosts that provide trustworthy session metadata and prefer versions with stronger parent-session validation.

Risk: Response-content logging can expose private or sensitive agent output.

Mitigation: Prefer a version that avoids logging response content and review logs before use in private workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harven-droid/skills/multi-agent-group-chat)
- [ClawHub project homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and usage guidance for an OpenClaw group-chat plugin; runtime behavior posts agent reply text to the detected chat destination.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, openclaw.plugin.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
