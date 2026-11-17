## Description:

Secure iCloud Calendar operations for OpenClaw with CalDAV and macOS native bridge providers. Use when tasks require calendar listing, event retrieval, event creation, event updates, event deletion, or credential setup via keyring, environment variables, or a config file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h8kxrfp68z-lgtm](https://clawhub.ai/user/h8kxrfp68z-lgtm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to connect OpenClaw agents to iCloud calendars, list calendars and events, and create, update, or delete calendar entries. It is most relevant when calendar automation needs explicit credential handling and provider selection between CalDAV and the macOS Calendar bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to iCloud calendars and an app-specific password.

Mitigation: Use app-specific passwords, prefer keyring storage, and install only in environments where calendar access is acceptable.

Risk: Credential handling can send iCloud credentials to a configurable CalDAV URL.

Mitigation: Keep ICALENDAR_SYNC_CALDAV_URL unset unless the destination has been audited.

Risk: Debug HTTP output may expose sensitive Apple response data.

Mitigation: Avoid --debug-http with real credentials and review logs for sensitive data before sharing.

Risk: Update and delete commands can change or remove calendar events.

Mitigation: Require explicit confirmation before agent-driven update or delete commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h8kxrfp68z-lgtm/skills/icalendar-sync)
- [README](artifact/README.md)
- [Security policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown guidance with inline shell commands and JSON event payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reflect calendar read results or state-changing create, update, and delete operations depending on the selected command.]

## Skill Version(s):

2.4.1 (source: server release metadata and changelog, released 2026-03-06; package metadata lists 2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
