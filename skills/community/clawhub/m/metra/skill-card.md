## Description:

Provides Chicago Metra commuter rail information, including train arrivals, vehicle tracking, service alerts, schedules, station lookup, route details, and fare calculations for Metra lines in the Chicago metropolitan area.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and transit-focused agents use this skill to answer natural-language questions about Chicago Metra arrivals, schedules, service alerts, routes, stations, and fares.

### Deployment Geography for Use:

United States (Chicago metropolitan area)

## Known Risks and Mitigations:

Risk: The skill sends the configured METRA_API_KEY to Metra GTFS-RT endpoints for real-time transit data.

Mitigation: Use a dedicated Metra developer key, store it in the environment, and rotate or revoke it if it is exposed.

Risk: Real-time commands may fail until the missing gtfs-realtime.proto file is supplied.

Mitigation: Confirm the artifact includes scripts/gtfs-realtime.proto before relying on train arrivals, vehicle positions, or service alerts.

Risk: The protobufjs dependency was flagged by server security guidance as needing an update.

Mitigation: Update protobufjs to a patched version and reinstall dependencies before production use.

Risk: Static GTFS schedule data is cached under ~/.metra/gtfs and may become stale.

Mitigation: Run the refresh-gtfs command periodically and after Metra publishes schedule updates.

## Reference(s):

- [Metra Skill on ClawHub](https://clawhub.ai/brianleach/skills/metra)
- [brianleach ClawHub Profile](https://clawhub.ai/user/brianleach)
- [Metra Developer Resources](https://metra.com/developers)
- [Metra GTFS Static Schedule Feed](https://schedules.metrarail.com/gtfs/schedule.zip)
- [Metra GTFS Published Timestamp](https://schedules.metrarail.com/gtfs/published.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transit times, train numbers, route names, station matches, fare details, alerts, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
