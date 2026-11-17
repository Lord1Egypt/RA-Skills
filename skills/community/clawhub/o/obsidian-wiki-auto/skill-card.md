## Description:

Builds and maintains a personal Obsidian knowledge wiki using OpenClaw-oriented sub-agents for file organization, content extraction, page creation, indexing, and maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayxjw](https://clawhub.ai/user/jayxjw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn source files in an Obsidian vault into organized Markdown wiki pages, entity and concept pages, indexes, logs, and synthesis notes. It supports manual and scheduled maintenance workflows for a personal knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended operation can read, move, rewrite, and generate wiki content without confirmation.

Mitigation: Run the skill manually before scheduling it, restrict it to a dedicated vault, and review generated pages and logs.

Risk: Raw source files may contain secrets or sensitive documents that the skill can ingest into generated pages.

Mitigation: Keep secrets and sensitive documents out of the raw folder and maintain backups of the vault.

Risk: Automatic dependency installation can change the local Python environment.

Mitigation: Pin or pre-provision required packages before unattended use and avoid scheduled runs until dependency behavior is verified.

Risk: Weak path scoping can affect unintended files if vault paths are not controlled.

Mitigation: Confirm path containment and use a dedicated Obsidian Wiki vault for this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayxjw/skills/obsidian-wiki-auto)
- [ClawHub publisher profile](https://clawhub.ai/user/jayxjw)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown wiki pages, JSON status objects, shell commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates files under an Obsidian Wiki vault, including source summaries, entity pages, concept pages, synthesis pages, index.md, and log.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
