## Description:

Monitors a living room Dirigera air sensor every five minutes and plays a continuous Mac speaker alert when PM2.5 or CO2 readings exceed configured danger thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-2](https://clawhub.ai/user/maverick-2)

### License/Terms of Use:


## Use Case:

Home automation users and developers use this skill to run a local, cron-scheduled backup smoke alert for a living room Dirigera air sensor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local alarm reads a Dirigera bearer token from disk.

Mitigation: Protect the token file with restrictive permissions and rotate any token previously used without those controls.

Risk: The detector disables TLS certificate verification when calling the Dirigera hub.

Mitigation: Enable TLS verification or pin the hub certificate before unattended use.

Risk: Alert audio generation uses a predictable temporary file path.

Mitigation: Replace the fixed /tmp audio path with a securely created temporary file.

Risk: A cron-based local alarm can fail if the hub, token, sensor, audio tools, or host are unavailable.

Mitigation: Use it only as a backup to regular smoke alarms and test manual and scheduled runs before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-2/skills/living-room-smoke-detector)
- [Publisher profile](https://clawhub.ai/user/maverick-2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown with bash snippets and JSON state examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup and usage instructions for a macOS cron job, plus a Python detector script that updates a JSON state file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
