## Description:

Generate a daily morning briefing (weather, calendar, news, reminders) using the local `briefing` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddakju](https://clawhub.ai/user/ddakju)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for a daily summary of weather, calendar events, RSS news, and reminders, or to schedule an automated morning briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external npm CLI that was not present for inspection.

Mitigation: Install only if the package and publisher are trusted, and prefer a pinned, reviewed package version before routine use.

Risk: The CLI may handle sensitive calendar and reminder data.

Mitigation: Review macOS permissions and local configuration before granting access, and limit access to data needed for the briefing.

Risk: License activation may place a license key directly in shell history.

Mitigation: Use a safer activation method if available, or clear shell history and avoid sharing terminals or logs that contain license keys.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ddakju/skills/morning-briefing-pro)
- [npm package: @openclaw-tools/morning-briefing](https://www.npmjs.com/package/@openclaw-tools/morning-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Readable briefing text, compact summaries, or JSON from the local CLI, with setup and scheduling commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local `briefing` binary on macOS; calendar and reminder output depends on local permissions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
