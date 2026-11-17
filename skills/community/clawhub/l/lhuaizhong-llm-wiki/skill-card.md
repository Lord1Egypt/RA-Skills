## Description:

Build and maintain a local Markdown knowledge wiki that compounds over time from notes, documents, transcripts, chat logs, research material, and project context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhuaizhong](https://clawhub.ai/user/lhuaizhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn scattered source material into a maintained local Markdown wiki, including Obsidian-friendly ingest, query, reindex, lint, and scaffold workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update local Markdown wiki files in a target vault.

Mitigation: Point it only at vaults the agent is allowed to read and edit, and review important note changes before relying on them.

Risk: Using --force with the bundled scaffold initializer can replace existing starter scaffold files.

Mitigation: Use --force only when replacing SCHEMA.md, INDEX.md, README.md, logs, or starter hub pages is intended.

Risk: Wiki summaries can become stale, unsupported, or misleading if source provenance is not preserved.

Mitigation: Keep source pointers on high-value claims, preserve disagreement explicitly, and run lint or reindex workflows as the vault grows.

## Reference(s):

- [Operations](artifact/references/operations.md)
- [Publish Notes](artifact/references/publish-notes.md)
- [Scaffold](artifact/references/scaffold.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with occasional bash commands and generated Markdown or Python-backed scaffold files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update files in a user-selected local knowledge vault; --force can replace starter scaffold files.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
