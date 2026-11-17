## Description:

This skill uses read-only OAuth to retrieve Google Health data as JSON, including data points, daily roll-ups, and exercise sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

Individuals and developers use this CLI to read consented Google Health data for an agent or script, retrieving selected metrics or exercise summaries as JSON. It requires a user-created Google Cloud OAuth client and one-time browser consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the release suspicious with high confidence, citing token-cache file handling and possible behavior beyond the stated purpose or network limits; analysis is partial.

Mitigation: Before installing, review the reported file deletion or overwrite and authenticated-request routing concerns, verify the configuration and behavior, and limit access to health data the account owner has consented to share.

## Reference(s):

- [Google Health CLI repository](https://github.com/stozo04/google-health-cli)
- [Google Health ClawHub release](https://clawhub.ai/stozo04/skills/google-health-cli-scan-pr23)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON data and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw data points, daily roll-ups, parsed exercise sessions, and local diagnostics; data output can contain sensitive health information and account or file-path details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
