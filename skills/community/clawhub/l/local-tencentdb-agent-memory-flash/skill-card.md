## Description:

Guides agents and users through local installation, configuration, validation, and troubleshooting of the TencentDB-Agent-Memory plugin for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to decide whether the memory plugin is already installed, install it when needed, configure local SQLite-backed memory and recall behavior, and verify that persistent memory works.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned third-party OpenClaw plugin.

Mitigation: Install only after confirming trust in the publisher, prefer a pinned and verified package version, and review the package before deployment.

Risk: The skill asks users to run a patch script that modifies OpenClaw behavior.

Mitigation: Inspect the patch script before running it, avoid elevated privileges, and confirm how to disable the plugin if behavior is unexpected.

Risk: The memory plugin stores conversation content, preferences, and tool-call results persistently.

Mitigation: Confirm storage expectations before use and document how to delete stored memories and logs.

Risk: Optional remote embedding configuration can send memory content to an external provider.

Mitigation: Use remote embeddings only when the provider and endpoint are approved for the data being stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcode-hans/skills/local-tencentdb-agent-memory-flash)
- [Publisher profile](https://clawhub.ai/user/cloudcode-hans)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation checks, OpenClaw plugin commands, configuration examples, validation prompts, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
