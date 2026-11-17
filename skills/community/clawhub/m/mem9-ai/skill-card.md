## Description:

Persistent cloud memory plugin for OpenClaw. This document routes setup, troubleshooting, and uninstall flows and defines config boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c4pt0r](https://clawhub.ai/user/c4pt0r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, reconnect, troubleshoot, or remove mem9 as persistent cloud memory across sessions and machines. It guides configuration changes, plugin installation, verification, and cleanup while preserving API-key and local-history boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: mem9 acts as persistent cloud memory and may receive conversation-derived content when conversation access is enabled.

Mitigation: Get explicit user consent before enabling conversation access, disclose the configured API URL, and do not upload local history or memory files during setup.

Risk: The setup stores and reuses a mem9 API key, which could expose account memory if copied into logs, history, or chat transcripts.

Mitigation: Keep the API key only in the documented plugin config path and user handoff, avoid local memory or history notes, and store the key in a secure vault.

Risk: The documented install command installs an unpinned plugin package.

Mitigation: Use a pinned, reviewed plugin version with integrity verification before deployment where release control matters.

Risk: Incorrect OpenClaw config paths or setup ordering can leave the memory plugin unavailable or the gateway unhealthy.

Mitigation: Restrict edits to the documented OpenClaw keys, install the plugin before switching the memory slot, read back config before restart, and use the troubleshooting flow when verification fails.

## Reference(s):

- [mem9 OpenClaw Memory](https://mem9.ai/openclaw-memory)
- [mem9 Website](https://mem9.ai/)
- [mem9 GitHub Project](https://github.com/mem9-ai/mem9)
- [OpenClaw Plugin README](https://github.com/mem9-ai/mem9/blob/main/openclaw-plugin/README.md)
- [mem9 Memory Dashboard](https://mem9.ai/your-memory/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes setup, troubleshooting, uninstall, and post-setup memory-use workflows for OpenClaw.]

## Skill Version(s):

1.0.48 (source: server release metadata; artifact frontmatter says 1.0.49)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
