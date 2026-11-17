## Description:

Notify when aircraft are overhead within a configurable radius using a local ADS-B SBS/BaseStation feed, with support for Clawdbot cron watchers and WhatsApp notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davestarling](https://clawhub.ai/user/davestarling)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up or troubleshoot ADS-B aircraft-overhead alerts from a local SBS/BaseStation feed, tune home coordinates, radius, cooldowns, and listen windows, and run a Clawdbot watcher that sends WhatsApp notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local ADS-B host settings, home coordinates, WhatsApp targets, cron timing, local state, logs, and optional cached photos.

Mitigation: Before installing, confirm the ADS-B feed host, home coordinates, WhatsApp target, and cron interval are yours, and periodically review the local adsb-overhead directory for state, logs, and cached photos.

Risk: Optional photo lookup can send aircraft hex identifiers to Planespotters and store thumbnails locally.

Mitigation: Disable photo lookup if you do not want aircraft hex identifiers sent to Planespotters or thumbnails stored locally.

## Reference(s):

- [SBS/BaseStation MSG fields](references/sbs-fields.md)
- [Skill release page](https://clawhub.ai/davestarling/skills/moltbot-adsb-overhead)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSONL]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts emit text alerts or JSONL alert records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime behavior can send WhatsApp messages through Clawdbot and may cache alert state and optional aircraft photos locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
