## Description:

Analyze synced health data across Oura, Withings, Hevy, Strava, WHOOP, and Eight Sleep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filipe-m-almeida](https://clawhub.ai/user/filipe-m-almeida)

### License/Terms of Use:


## Use Case:

External users and agents use Health Sync to set up remote onboarding, sync health-provider data, and answer personal health trend questions across sleep, recovery, activity, workouts, and body metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an npm-distributed health-sync command while handling health records and credentials.

Mitigation: Use a pinned and verified health-sync version and run it under a restricted account or sandbox.

Risk: Remote onboarding imports encrypted archives that contain provider credentials or tokens and writes local credential and SQLite files.

Mitigation: Protect generated credential and database files with access controls, backup controls, and retention limits.

Risk: Eight Sleep synchronization may collect data about other bed occupants.

Mitigation: Confirm collection scope and consent before enabling or analyzing related occupant data.

Risk: Health analysis may be based on stale data if synchronization fails.

Mitigation: Run sync before analysis and clearly disclose any sync failure or data freshness limitation.

## Reference(s):

- [Health Sync ClawHub Listing](https://clawhub.ai/filipe-m-almeida/skills/health-sync)
- [Setup Reference](references/setup.md)
- [Oura Schema](references/oura.md)
- [Withings Schema](references/withings.md)
- [Hevy Schema](references/hevy.md)
- [Strava Schema](references/strava.md)
- [WHOOP Schema](references/whoop.md)
- [Eight Sleep Schema](references/eightsleep.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include setup steps, sync status, SQL-backed health trend analysis, and practical interpretation of provider data.]

## Skill Version(s):

0.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
