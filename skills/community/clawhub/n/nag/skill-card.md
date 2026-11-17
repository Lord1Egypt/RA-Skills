## Description:

Persistent reminder system that keeps bugging you until you confirm completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Nag to set up recurring reminders that continue through cron and heartbeat checks until the user confirms completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron jobs and heartbeat checks can keep reminding the user across sessions after the reminder is no longer wanted.

Mitigation: Review each schedule before installing and remove the related cron job plus nag-config and state entries when the reminder should stop.

Risk: Broad confirmation phrases may mark the wrong reminder as complete when multiple reminders are active.

Mitigation: Use specific confirmation patterns and resolve ambiguous matches against reminders that are currently in their nag window.

Risk: Tone-based escalation can generate messages that are more forceful than intended.

Mitigation: Set explicit message text or conservative tone guidance for reminders where wording matters.

## Reference(s):

- [Nag Config Examples](references/config-examples.md)
- [ClawHub Nag Skill Page](https://clawhub.ai/madebydia/skills/nag)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with JSON configuration examples and shell script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reminder setup guidance, heartbeat instructions, cron scheduling guidance, and state/configuration examples.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
