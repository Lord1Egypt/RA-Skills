## Description:

Markdown Studio helps agents create publication-ready Markdown documents, including technical docs, READMEs, reports, wikis, tables, code blocks, math, diagrams, and image references or embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge workers use this skill to generate structured Markdown documents such as technical documentation, READMEs, reports, wiki pages, tutorials, and reference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedding local images as base64 copies the image data directly into the generated Markdown.

Mitigation: Only embed images intended for inclusion in the final document; use file references for sensitive or large images.

Risk: Generated Markdown may require editorial review before publication.

Mitigation: Review generated documents for accuracy, formatting, links, and image handling before sharing or publishing.

## Reference(s):

- [Markdown Templates](artifact/references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/markdown-studio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with optional fenced code blocks, tables, Mermaid diagrams, math notation, and image references or base64-embedded images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown files to the workspace; base64 image embedding copies image data into the generated document.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
