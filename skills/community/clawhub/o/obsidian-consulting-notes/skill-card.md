## Description:

Helps agents organize consulting knowledge bases in Obsidian by converting Word, PDF, and Markdown documents into atomic Markdown notes with folder classification, YAML tags, and related-note prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d997gq7vsq-svg](https://clawhub.ai/user/d997gq7vsq-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants and knowledge-base maintainers use this skill to split long consulting documents into Obsidian-ready atomic notes, classify them into diagnosis, solution, or deliverable libraries, and add standardized tags. It also supports cleanup reports and tag completion for existing Markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keyword-based classification can rename, move, or retag notes incorrectly.

Mitigation: Process small batches, review the proposed file list before confirming changes, and keep a backup of the Obsidian workspace.

Risk: Document splitting can discard context or create misleading atomic notes when source material has multiple overlapping topics.

Mitigation: Review generated note summaries, target folders, and YAML tags before accepting writes.

## Reference(s):

- [Consulting Knowledge Base Taxonomy](references/taxonomy.md)
- [Detailed Operation Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter and text operation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file creation, renaming, movement, and tag updates for user confirmation before writing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
