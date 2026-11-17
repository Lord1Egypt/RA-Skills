## Description:

Connects selected calendars to an assistant so it can check availability, find and manage events, and manage calendar syncs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kochpaul](https://clawhub.ai/user/kochpaul)

### License/Terms of Use:

MIT-0

## Use Case:

People using an assistant to coordinate their calendars can check availability, find or manage events, and set up, inspect, pause, or delete calendar syncs with their permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar access could expose private event details or allow unwanted changes.

Mitigation: Grant only the necessary calendars, detail level, and write permissions; confirm calendars are writable before making changes.

Risk: Sharing an access key in chat could expose the connected calendars.

Mitigation: Keep the access key locally in the client environment, never in chat.

Risk: Created calendar syncs can continue after assistant access is revoked.

Mitigation: Pause or delete unwanted syncs separately, and confirm sync direction and detail level before creating one.

## Reference(s):

- [Kalender Sync ClawHub release](https://clawhub.ai/kochpaul/skills/kalender-sync)
- [Kalender Sync agent guide](https://kalender-sync.de/en/agents.md)
- [Kalender Sync Codex setup](https://docs.kalender-sync.de/en/ki-assistent/codex/)
- [Kalender Sync OpenClaw setup](https://docs.kalender-sync.de/en/ki-assistent/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with inline commands and calendar summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar reads, event changes, and sync operations depend on the calendars and permissions the user grants.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
