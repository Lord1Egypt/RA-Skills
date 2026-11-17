## Description:

Hermes Memory CN gives an AI assistant a local long-term memory layer for storing, searching, organizing, decaying, archiving, importing, and exporting user memories with Chinese-optimized vector search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream978](https://clawhub.ai/user/dream978)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add persistent local memory to an agent, including preferences, facts, portfolio notes, strategies, lessons, and relationship queries. It is especially oriented toward Chinese-language semantic search and local personal knowledge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad conversation memories, including preferences, trading details, and other personal context on disk.

Mitigation: Use it only for data you are comfortable storing locally, avoid secrets or regulated data, and periodically review or delete stored memories and exports.

Risk: Markdown exports and generated skill drafts may write files that overwrite existing Markdown or instruction content.

Mitigation: Restrict exports and drafts to reviewed directories, inspect generated files before promotion, and keep backups for any directories the scripts can write to.

## Reference(s):

- [Installation guide](artifact/references/install.md)
- [AGENTS.md integration guide](artifact/references/integration.md)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Hugging Face mirror endpoint](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite-backed memory records, relationship data, Markdown exports, and skill draft files when the user runs the bundled scripts.]

## Skill Version(s):

1.4.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
