## Description:

OAuth token refresh management for Google APIs via the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[herry3zz](https://clawhub.ai/user/herry3zz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure gog CLI authentication, refresh Google API tokens, and run common Gmail and Drive commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad Google mail, file, and calendar access guidance that may exceed a token-refresh-only use case.

Mitigation: Confirm the intended Google account and services before use, and grant only the Google API scopes required for the task.

Risk: File keyring mode can weaken token protection if the password or storage location is poorly managed.

Mitigation: Prefer the OS keychain or a managed secret store; if file mode is required, use a strong password and restrict local file permissions.

Risk: The artifact includes a hard-coded email address and credential path.

Mitigation: Replace them with explicit local configuration for the intended account and credentials file before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/herry3zz/skills/google-gog)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account, credential path, token storage, re-authentication, automation, Gmail, and Drive command guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
