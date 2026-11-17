## Description:

Build and maintain a structured local knowledge base. Classify incoming content, save it as reusable Markdown, organize inbox items, and keep the knowledge base consistent over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaochuanchao](https://clawhub.ai/user/shaochuanchao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize and maintain a local Markdown knowledge base, classify incoming notes or documents, and organize uncertain items through an inbox workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update local files under knowledge/.

Mitigation: Use it in a dedicated or clearly chosen workspace and review proposed paths before writing.

Risk: Bulk inbox organization can move many files or mark low-value items for removal.

Mitigation: Review organization reports first, prefer archiving, and require explicit confirmation before deletion.

Risk: Content may be misclassified or saved with uncertain source attribution.

Mitigation: Use the inbox fallback for medium or low confidence items and preserve source, confidence, and related metadata in each entry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaochuanchao/skills/kb-manager)
- [README](README.md)
- [Classification Rules](docs/classification-rules.md)
- [Naming Rules](docs/naming-rules.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries, directory structures, save paths, filenames, organization reports, and occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local files under knowledge/ when asked; uses inbox, archive, templates, and confidence notes to preserve reviewability.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
