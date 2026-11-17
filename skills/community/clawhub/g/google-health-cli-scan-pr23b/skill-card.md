## Description:

Read Google Health v4 data through read-only OAuth and return data points, daily roll-ups, exercise sessions, or API responses as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can retrieve selected Google Health metrics or daily totals for agent workflows. Use the account owner's consent, request only the data needed, and handle the JSON output as sensitive health information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags possible overwriting or deletion of unrelated local files during authentication.

Mitigation: Confirm the token-cache path before authentication or logout; use GOOGLE_HEALTH_TOKEN_CACHE to select a dedicated CLI cache path.

Risk: Large API responses may be silently truncated, leaving results incomplete.

Mitigation: Request only the required data types and narrow date windows; split broad queries into smaller windows and check the returned counts.

## Reference(s):

- [Project homepage](https://github.com/stozo04/google-health-cli)
- [Machine contract](artifact/docs/MACHINE_CONTRACT.md)
- [OAuth setup](artifact/OAUTH_SETUP.md)
- [Google Health API](https://health.googleapis.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [JSON records and roll-ups on stdout; shell command examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only health data results can contain sensitive personal information.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
