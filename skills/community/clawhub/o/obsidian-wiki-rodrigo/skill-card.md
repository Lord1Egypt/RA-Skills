## Description:

Work with Rodion's Obsidian vault via Nextcloud, including ingest, query, lint, and wiki maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodrigo09313](https://clawhub.ai/user/rodrigo09313)

### License/Terms of Use:

MIT-0

## Use Case:

Users managing this specific Obsidian knowledge base use the skill to add source material, query wiki content, lint notes, update index and log pages, and sync changes through Nextcloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or ambiguous prompts could cause unintended Obsidian wiki edits or sync actions.

Mitigation: Use explicit ingest, write, and sync commands, and review planned file changes before allowing the agent to apply them.

Risk: Nextcloud sync can propagate local vault changes to connected clients.

Mitigation: Run the sync step only after confirming the intended Obsidian files were created or modified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rodrigo09313/skills/obsidian-wiki-rodrigo)
- [Wiki Operations](references/operations.md)
- [Nextcloud Sync](references/sync.md)
- [Wiki Structure](references/wiki-structure.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, text responses, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Obsidian wiki files and request a Nextcloud file scan after changes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
