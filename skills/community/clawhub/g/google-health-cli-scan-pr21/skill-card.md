## Description:

Reads Google Health v4 data through read-only OAuth and returns data points, daily roll-ups, and exercise sessions as JSON for an agent to use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use the CLI to read health and fitness data from an account whose owner has authorized access, then process the JSON for a requested task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious and reports a possibility of authenticated Google requests being redirected.

Mitigation: Review the release before installation and confirm authenticated requests go only to the intended Google OAuth and Health API services.

Risk: The security review reports that configurable OAuth scopes could exceed the stated read-only purpose.

Mitigation: Check the scopes shown during authorization and grant only the read-only Health access needed for the task.

Risk: The security review was partial because some referenced paths were missing.

Mitigation: Verify the unavailable referenced files against the release source before use.

Risk: Command output can contain sensitive health, profile, settings, and local account information that downstream tools may log or transmit.

Mitigation: Use the narrowest data types and time window, run only with the account owner's consent, and keep output in trusted contexts.

Risk: OAuth client credentials and the cached token are sensitive local files.

Mitigation: Restrict credential files, keep them out of shared locations and logs, and do not commit them.

## Reference(s):

- [Project repository](https://github.com/stozo04/google-health-cli)
- [Release downloads](https://github.com/stozo04/google-health-cli/releases)
- [OAuth setup guide](https://github.com/stozo04/google-health-cli/blob/main/OAUTH_SETUP.md)
- [Machine contract](https://github.com/stozo04/google-health-cli/blob/main/docs/MACHINE_CONTRACT.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON data on stdout, with command-line examples and setup guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON data is returned without interpretation; callers choose what to process.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
