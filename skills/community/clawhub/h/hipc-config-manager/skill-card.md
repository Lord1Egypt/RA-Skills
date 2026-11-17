## Description:

Manages and validates HIPC API secrets before related HIPC business skills run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[377739442](https://clawhub.ai/user/377739442)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check whether a HIPC API secret is configured and to save a format-validated secret for prod or dev HIPC API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the HIPC API secret in plaintext at ~/hipc_config.json.

Mitigation: Use a low-privilege or revocable HIPC credential, avoid sharing logs or command history that may contain the secret, and rotate the credential after setup in exposed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/377739442/skills/hipc-config-manager)

## Skill Output:

**Output Type(s):** [JSON, Configuration]

**Output Format:** [JSON status response and local configuration file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores the HIPC API secret in plaintext at ~/hipc_config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
