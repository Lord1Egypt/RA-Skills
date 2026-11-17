## Description:

Guides users through configuring Codex, Claude Code, or an application to use OceanToken models and troubleshooting API access errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceantoken](https://clawhub.ai/user/oceantoken)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect their coding agent or application to OceanToken, manage API-key setup, and resolve common API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration edits may replace working provider settings.

Mitigation: Review proposed changes and obtain approval before editing; back up existing settings and prefer a separate profile.

Risk: API keys may be exposed in plaintext settings or committed files.

Mitigation: Use environment variables or git-ignored local settings, and do not commit credentials.

Risk: Using the provider sends prompts and API traffic to OceanToken.

Mitigation: Enable the provider only when the user intends to route traffic through OceanToken.

## Reference(s):

- [OceanToken homepage](https://oceantoken.ai)
- [OceanToken API keys](https://app.oceantoken.ai/ui/?page=api-keys)
- [OceanToken model list](https://api.oceantoken.ai/v1/models)

## Skill Output:

**Output Type(s):** [Configuration instructions, Code, Shell commands, Troubleshooting guidance]

**Output Format:** [Markdown with TOML, JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration changes require user approval.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
