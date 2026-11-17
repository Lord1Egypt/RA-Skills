## Description:

Google Health CLI lets an agent read Google Health data through read-only OAuth and returns data points, daily roll-ups, exercise sessions, and other v4 responses as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use the CLI to retrieve consented Google Health metrics and exercise records as JSON for analysis. A Google Cloud OAuth client and a one-time browser authorization are required for read-only access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health, profile, or settings data returned as JSON may be logged, persisted, or forwarded by downstream agents and pipelines.

Mitigation: Use only the needed data types and narrowest time window, confirm the account owner's consent, and handle the output only in trusted contexts without unnecessary retention or forwarding.

Risk: Security analysis had partial coverage because some local path references could not be resolved.

Mitigation: Review the documented file, network, and browser-launch access requirements and decide whether they fit the intended environment before installation.

Risk: OAuth client credentials and the cached token are stored locally in plaintext.

Mitigation: Restrict access to the config file and token cache, keep them out of shared folders and logs, and revoke or rotate credentials if they may have been exposed.

## Reference(s):

- [Project homepage](https://github.com/stozo04/google-health-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON on stdout; operational messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw health records, daily roll-ups, and exercise session data for requested types and time windows.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
