## Description:

Manage secrets via macOS Keychain by migrating plaintext secrets, reading and writing keychain entries, bridging selected secrets to files for bash tools, auditing leaks, and diagnosing access issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[euda1mon1a](https://clawhub.ai/user/euda1mon1a)

### License/Terms of Use:


## Use Case:

Developers and operators running OpenClaw on macOS use this skill to move API keys from plaintext files into macOS Keychain, audit secret directories, and generate commands and configuration for Python and bash access patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-impact secrets and includes file fallback and plaintext bridge behavior.

Mitigation: Use it only after review; require explicit opt-in for bridge files, keep bridge files securely created, and avoid valuable credentials until the fallback path behavior is approved.

Risk: Service names and filesystem paths influence where secrets are read or written.

Mitigation: Validate service names and paths before use, restrict operations to intended secret directories, and review generated commands before execution.

Risk: The artifact includes copy-pastable credential-handling examples and dependency installation guidance.

Mitigation: Remove unsafe password or secret examples before operational use and pin or isolate dependency installation for each Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/euda1mon1a/skills/keychain-bridge)
- [Publisher profile](https://clawhub.ai/user/euda1mon1a)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local macOS Keychain and filesystem guidance for agent execution; no network endpoints are described by the artifact.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
