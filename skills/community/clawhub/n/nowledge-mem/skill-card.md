## Description:

Enables OpenClaw to use shared Nowledge Mem memory locally or remotely for persistent multi-tool AI context storage and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wey-gu](https://clawhub.ai/user/wey-gu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to connect agents to local or remote Nowledge Mem so they can search, save, recall, and manage persistent cross-tool memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin can automatically persist conversations into a searchable memory store by default.

Mitigation: Use Incognito sessions, #nmem-skip, captureExclude, or disable sessionDigest for confidential sessions; avoid storing secrets or regulated data unless persistent retention is acceptable.

Risk: Remote mode and privileged memory injection can expose sensitive context if the backend or transport is not trusted.

Mitigation: Prefer local mode or an HTTPS remote server with appropriate authentication, and review the plugin before installing it in sensitive environments.

Risk: Runtime use of the nmem CLI can depend on the installed command available to OpenClaw.

Mitigation: Install and pin a trusted nmem CLI yourself before enabling the plugin.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wey-gu/skills/nowledge-mem)
- [Nowledge Mem](https://mem.nowledge.co)
- [OpenClaw](https://openclaw.ai)
- [Nowledge Mem remote access guide](https://mem.nowledge.co/docs/remote-access)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance covers installation, local or remote configuration, verification, memory search and save behavior, and privacy controls.]

## Skill Version(s):

0.8.34 (source: changelog and package.json, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
