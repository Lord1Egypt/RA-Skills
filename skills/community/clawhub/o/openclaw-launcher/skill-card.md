## Description:

Create Windows desktop shortcuts and scripts for one-click OpenClaw startup on WSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinl1993](https://clawhub.ai/user/kevinl1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create or troubleshoot a Windows desktop launcher for OpenClaw Gateway running in WSL, including shortcut creation, port proxy setup, service start checks, icon setup, and keep-alive handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher reads a local OpenClaw auth token and opens a token-bearing localhost URL.

Mitigation: Review the generated scripts before use, never hardcode or share tokens, and keep launcher files in a user-private directory.

Risk: The launcher runs a hidden PowerShell script with execution-policy bypass and creates persistent launcher files.

Mitigation: Use it only from a trusted publisher, restrict permissions on the script directory, and remove the launcher files when they are no longer needed.

Risk: Port proxy setup may require Administrator privileges and the keep-alive process can remain active for up to a day.

Mitigation: Avoid routine Administrator launches, inspect the port proxy configuration when troubleshooting, and stop or clean up the keep-alive process when it is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinl1993/skills/openclaw-launcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell, batch, Bash, and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup and troubleshooting steps for Windows, WSL, and OpenClaw Gateway.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
