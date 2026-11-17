## Description:

Garmin Connect integration for Clawdbot: sync fitness data (steps, HR, calories, workouts, sleep) every 5 minutes using OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to authenticate with Garmin Connect, sync activity, sleep, heart-rate, calorie, workout, and related health data, and format cached results for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin credentials and reusable OAuth session tokens can be exposed if passwords are passed on the command line or session files have broad permissions.

Mitigation: Use a safer browser or CLI authentication flow, avoid command-line password arguments, and restrict permissions on ~/.garth/session.json.

Risk: Sensitive health records can be persisted locally in cache files and exported into /tmp by the 30-day sync and dashboard scripts.

Mitigation: Store cache and export files in a private directory, restrict file permissions, delete exports when no longer needed, and avoid dashboard/export scripts unless required.

Risk: Recurring cron jobs can continue collecting and writing health data after initial setup.

Mitigation: Review cron entries before enabling them, run the sync under a least-privileged user, and remove scheduled jobs when ongoing sync is no longer needed.

Risk: The optional dashboard uses remote browser scripts while displaying health data.

Mitigation: Avoid opening generated dashboards with sensitive data unless needed, and prefer trusted or local assets for dashboard rendering.

Risk: Unpinned dependencies can change behavior or security posture over time.

Mitigation: Pin and review dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-garmin-connect)
- [Clawdbot](https://clawd.bot)
- [Garmin sign-in](https://sso.garmin.com/sso/signin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python usage examples, JSON cache data, and formatted text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local OAuth session files, recurring cron jobs, JSON health-data caches, and optional HTML dashboard exports.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
