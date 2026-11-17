## Description:

Starts a local web viewer for browsing, refreshing, backing up, deleting, and exporting OpenClaw chat history, including reset backup sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lengyhua](https://clawhub.ai/user/lengyhua)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to launch a local history browser, inspect chat sessions in chat or raw JSON views, export sessions through API endpoints, and create manual backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes sensitive local chat history through an unauthenticated web server.

Mitigation: Run it only on trusted machines and networks, do not expose or forward the port, and stop the server when finished.

Risk: The deletion feature can permanently remove chat history and backups.

Mitigation: Back up or export important sessions before deletion and use the feature only for history you are authorized to manage.

Risk: The server listens more broadly than the documentation states.

Mitigation: Treat it as unsafe for shared hosts or reachable network environments unless binding and access controls are hardened first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lengyhua/skills/openclaw-history-viewer)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local web server and may create, export, or delete local chat-history files.]

## Skill Version(s):

1.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
