## Description:

Reads Google Health data through read-only OAuth and returns data points, daily rollups, and exercise sessions as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use the CLI through an agent to retrieve consented Google Health metrics, daily rollups, and exercise sessions for analysis or task-specific reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A confirmed response-truncation issue may leave returned health data incomplete.

Mitigation: Check results for completeness before relying on them; use narrower time windows and compare critical results with the source when needed.

## Reference(s):

- [Google Health CLI project](https://github.com/stozo04/google-health-cli)
- [OAuth setup guide](OAUTH_SETUP.md)
- [Machine contract and JSON output reference](docs/MACHINE_CONTRACT.md)
- [ClawHub release page](https://clawhub.ai/stozo04/skills/google-health-cli-scan-pr23c)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON arrays and objects, with command and setup guidance in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes raw health records, server-side daily rollups, and parsed exercise sessions; results depend on the requested type and time window.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
