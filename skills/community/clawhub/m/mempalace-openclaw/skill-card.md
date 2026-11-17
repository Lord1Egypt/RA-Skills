## Description:

MemPalace archives AI conversations to local long-term storage and enables semantic search through OpenClaw commands for archive, search, and daily auto-save.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deveuper](https://clawhub.ai/user/deveuper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve agent conversation memory locally, search previous decisions or notes semantically, and optionally enable scheduled or hook-driven saves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain conversation and code content durably and later surface stored material verbatim to agents or tools.

Mitigation: Install only when durable local memory is intended, review what is archived, and avoid storing secrets or sensitive conversations.

Risk: Hook-driven or scheduled saves can automatically capture content without a fresh manual command.

Mitigation: Enable Stop, PreCompact, or cron auto-save only after confirming the desired capture behavior and review hook configuration before use.

Risk: Mining broad directories can index files that contain credentials, private data, or unrelated project content.

Mitigation: Mine narrowly scoped directories, filter sensitive files before ingestion, and avoid broad project roots unless they have been reviewed.

Risk: First-run setup can modify the active Python environment by installing the bundled package and runtime dependencies.

Mitigation: Use a dedicated virtual environment with pinned dependencies when installing or running the skill.

Risk: Wikipedia entity research can disclose the exact term being researched over the network.

Mitigation: Disable or avoid entity research when offline operation or lookup privacy is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deveuper/skills/mempalace-openclaw)
- [MemPalace upstream project referenced by the skill](https://github.com/milla-jovovich/mempalace)
- [Core package README](artifact/mempalace/README.md)
- [Hooks README](artifact/mempalace/hooks/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file or configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local conversation archives, ChromaDB indexes, SQLite data, hook state, and Python package/dependency changes during use.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
