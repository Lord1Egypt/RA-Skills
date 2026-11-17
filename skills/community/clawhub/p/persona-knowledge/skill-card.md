## Description:

Persistent, incremental, searchable persona knowledge base. Ingests data from Obsidian vaults, chat exports, X/Twitter archives, and more into a MemPalace-backed store with a Karpathy LLM Wiki knowledge layer. Exports training/ directories for persona-model-trainer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create, incrementally update, search, and export local persona datasets from notes, chats, social archives, and other source files for downstream persona training.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local storage and exports can contain private messages or sensitive persona data.

Mitigation: Use the skill only with datasets suitable for persistent searchable storage, sanitize sources before ingestion, and keep OPENPERSONA_KNOWLEDGE in a private directory.

Risk: Imported archives can include passwords, financial identifiers, SSNs, private DMs, or third-party messages.

Mitigation: Review and sanitize archives before import, avoid sensitive or non-consensual third-party content, and prefer dry-run or wiki-only modes where possible.

Risk: Deleting a dataset may require removing multiple generated artifacts.

Mitigation: Verify deletion of source backups, MemPalace data, wiki files, and training exports when removing a dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neiljo-gy/skills/persona-knowledge)
- [Source Formats](artifact/references/source-formats.md)
- [Wiki Schema](artifact/references/wiki-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated local JSON, JSONL, Markdown, and metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local knowledge directories, wiki pages, source backups, search results, and training exports.]

## Skill Version(s):

0.2.2 (source: evidence.json release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
