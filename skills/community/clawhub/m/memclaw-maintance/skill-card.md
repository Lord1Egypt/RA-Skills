## Description:

MemClaw Maintenance Guide provides installation, configuration, troubleshooting, migration, and maintenance guidance for the MemClaw OpenClaw memory plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and configure MemClaw, migrate existing OpenClaw memories, and run maintenance or troubleshooting for persistent local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to make MemClaw the default memory system and store profile or session data persistently.

Mitigation: Confirm this memory posture with the user, back up existing memory files and AGENTS.md, and avoid storing sensitive information unless the configured providers and retention policy are acceptable.

Risk: Relevant memory content may be sent to configured LLM and embedding providers.

Mitigation: Review provider configuration, API key handling, and data-sharing expectations before enabling the plugin.

Risk: The documented plugin install command uses an unpinned package path.

Mitigation: Pin or verify the MemClaw package version and source before installation when possible.

Risk: Migration and maintenance can change persistent memory indexes and derived memory layers.

Mitigation: Run maintenance in dry-run mode first where supported and keep backups before migration, pruning, or reindexing.

## Reference(s):

- [MemClaw Maintenance Tools Reference](./references/tools.md)
- [MemClaw Troubleshooting Guide](./references/troubleshooting.md)
- [MemClaw daily-use skill](https://clawhub.ai/sopaco/memclaw)
- [MemClaw project repository](https://github.com/sopaco/cortex-mem)
- [MemClaw plugin README](https://raw.githubusercontent.com/sopaco/cortex-mem/refs/heads/main/examples/%40memclaw/plugin/README.md)
- [MemClaw GitHub Issues](https://github.com/sopaco/cortex-mem/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with JSON configuration snippets and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw configuration examples, AGENTS.md memory guidance, and MemClaw migration or maintenance tool payloads.]

## Skill Version(s):

0.9.31 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
