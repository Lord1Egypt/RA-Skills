## Description:

Scan MCP server configuration files for security vulnerabilities using mcpsec across OWASP MCP Top 10 risk categories, with auto-discovery for Claude Desktop, Cursor, VS Code, and custom config paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit local MCP server configuration files for prompt injection, hardcoded secrets, missing authentication, insecure transport, excessive permissions, and related MCP risks. It is intended for local read-only scans that report findings by severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated binary install command can download and install an external executable without enforced checksum validation before the executable reads sensitive MCP configuration files.

Mitigation: Verify the release archive against a pinned checksum with sha256sum -c before extracting, or build the scanner from audited source.

Risk: MCP configuration files may contain API keys or tokens that the scanner must read to detect hardcoded secrets.

Mitigation: Run the scanner with least privilege, limit scans to intended config paths, and use an isolated environment for higher-security workflows.

Risk: Installing the external binary into a system-wide path can broaden the effect of a compromised or incorrect executable.

Mitigation: Prefer a user-local install path and review the scanner source or binary provenance before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/mcpsec)
- [mcpsec scanner repository](https://github.com/pfrederiksen/mcpsec)
- [mcpsec v1.0.0 checksums](https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/checksums.txt)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output, with optional JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-filtered findings; quiet mode suppresses clean results.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
