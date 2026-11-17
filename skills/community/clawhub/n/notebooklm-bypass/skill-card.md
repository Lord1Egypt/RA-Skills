## Description:

Programmatic NotebookLM control with auto-recovery for authentication errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antaripnandi](https://clawhub.ai/user/antaripnandi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run NotebookLM CLI commands and recover from authentication-expired failures with explicit user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recovery flow extracts and persistently stores Google/NotebookLM session cookies.

Mitigation: Install only if cookie handling is acceptable, prefer supported NotebookLM login when possible, and use a dedicated low-privilege browser profile.

Risk: Stored auth payload files or persistent environment variables can expose active session credentials if the local environment is compromised.

Mitigation: Avoid persistent environment-variable storage where possible, delete ~/.notebooklm/storage_state.json and ~/.notebooklm/auth_payload.json after use, and revoke or refresh the Google session if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antaripnandi/skills/notebooklm-bypass)
- [OpenClaw Framework](https://github.com/openclaw/openclaw)
- [NotebookLM](https://notebooklm.google.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and CLI instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user permission before running the authentication recovery script.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
