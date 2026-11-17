## Description:

MTA Commuter helps agents look up LIRR, Metro-North, and NYC Subway schedules, trip options, nearby stations, service alerts, and track-watch notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ottomanelli](https://clawhub.ai/user/ottomanelli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan NYC-area commuter rail and subway trips, compare route options, check service disruptions, and request track-assignment watches for LIRR or Metro-North trains.

### Deployment Geography for Use:

Global; transit coverage is limited to the New York City metropolitan area.

## Known Risks and Mitigations:

Risk: Saved locations can include precise home, work, or recurring destination addresses.

Mitigation: Ask for explicit confirmation before saving locations, store only the minimum address or coordinate detail needed, and review or delete data/locations.json when it is no longer needed.

Risk: Track-watch requests create recurring background cron jobs that may continue polling if not scoped or cleaned up.

Mitigation: Confirm the train, station, notification channel, and time window before creating a watch, use auto-delete behavior where available, and verify or cancel remaining OpenClaw cron jobs after the notification window passes.

Risk: Track-watch functionality depends on unofficial myLIRR and myMNR endpoints that may change or become unavailable.

Mitigation: Treat track-watch results as best-effort and fall back to official MTA GTFS feeds or user-visible MTA resources when unofficial endpoint checks fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ottomanelli/skills/mta-commuter)
- [Publisher Profile](https://clawhub.ai/user/ottomanelli)
- [Project Homepage](https://github.com/ottomanelli/mta-commuter)
- [MTA Developer Resources](https://new.mta.info/developers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown and terminal text, with optional JSON output from supported CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local saved-location data and optional OpenClaw cron jobs when the user confirms those workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
