## Description:

Secret redaction MCP server for OpenClaw agents. Prevents API keys, DB credentials, SSH keys, emails, IPs, JWTs, and 30+ other secret types from leaking to LLM providers. Includes guard command, API proxy, canary tokens, encrypted vault, git history scanning, org posture scanning, file watcher, and dashboard. Use when reading/writing files that may contain secrets, setting up agent security, or auditing for credential exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Pastewatch MCP and CLI workflows that redact secrets from file reads and writes, scan code or command output, and add a proxy guard before outbound LLM API traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release recommends installing an external binary that may not be pinned to an immutable artifact.

Mitigation: Install only from a trusted publisher and release process; prefer pinned, signed, checksum-verified, or package-manager-verifiable builds.

Risk: The proxy can inspect sensitive prompts, headers, and provider traffic that pass through it.

Mitigation: Run the proxy with the least privilege practical, limit it to required providers and ports, and review audit logging and retention settings before use.

Risk: The documented system-wide systemd setup creates a persistent service in the request path.

Mitigation: Use the system-wide service only when needed, document rollback steps, and prefer project-scoped or user-scoped operation for narrower deployments.

## Reference(s):

- [ClawHub Pastewatch MCP Release](https://clawhub.ai/ppiankov/skills/pastewatch-mcp)
- [Pastewatch Canonical Source](https://github.com/ppiankov/pastewatch)
- [Agent-Native CLI Convention](https://ancc.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, configuration snippets, MCP tool descriptions, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pastewatch-cli and mcporter binaries; proxy mode can inspect outbound LLM API traffic.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
