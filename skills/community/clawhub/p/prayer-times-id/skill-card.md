## Description: <br>
Schedules Indonesian prayer-time reminders in OpenClaw using AlAdhan timings, location settings, Ramadan detection, and daily quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zckyachmd](https://clawhub.ai/user/zckyachmd) <br>

### License/Terms of Use: <br>
BSD-3-Clause <br>


## Use Case: <br>
OpenClaw users in Indonesia use this skill to fetch daily prayer times for a configured location and create one-shot reminder events for the current day. <br>

### Deployment Geography for Use: <br>
Indonesia <br>

## Known Risks and Mitigations: <br>
Risk: Configured location coordinates are sent to AlAdhan when the skill fetches prayer times. <br>
Mitigation: Review prayer_config.json before running and use only the intended location coordinates. <br>
Risk: Running the engine without dry-run creates OpenClaw reminder jobs for the current day. <br>
Mitigation: Run node engine.js --dry-run first, then run node engine.js only when the reminder jobs should be created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zckyachmd/prayer-times-id) <br>
- [AlAdhan timings API](https://api.aladhan.com/v1/timings) <br>
- [AlAdhan Gregorian to Hijri API](https://api.aladhan.com/v1/gToH) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON execution summary with OpenClaw cron reminder events] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prayer_config.json for location, timezone, calculation method, and optional AlAdhan tuning; --dry-run avoids creating jobs.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
