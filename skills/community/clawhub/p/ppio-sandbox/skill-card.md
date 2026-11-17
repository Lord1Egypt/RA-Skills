## Description:

Run browser operations and untrusted code in a secure PPIO cloud sandbox (Firecracker VM).

This skill is ready for commercial/non-commercial use.

## Publisher:

[piston4711](https://clawhub.ai/user/piston4711)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route web browsing, unfamiliar builds, downloaded scripts, and other untrusted execution into an isolated PPIO cloud sandbox instead of their local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move local files to and from an internet-enabled cloud sandbox.

Mitigation: Avoid uploading secrets or broad project folders, and treat downloaded sandbox files as untrusted.

Risk: The skill requires a PPIO or E2B API key and creates billable sandbox sessions.

Mitigation: Install only when comfortable granting that key, reuse sandboxes where appropriate, and kill sandboxes when finished.

Risk: The security evidence reports broad sandbox and network settings.

Mitigation: Prefer versions with pinned dependencies and restricted local transfer paths before wider deployment.

## Reference(s):

- [PPIO Sandbox: Browser Use Integration](references/browser-use.md)
- [PPIO Browser Use Documentation](https://ppio.com/docs/sandbox/integrate-browser-use)
- [Ppio Sandbox on ClawHub](https://clawhub.ai/piston4711/skills/ppio-sandbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sandbox command output is truncated to preserve the agent context window.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
