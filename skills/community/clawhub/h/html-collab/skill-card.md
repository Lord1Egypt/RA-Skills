## Description:

Use this skill for HTML documents that will go through LLM-human review cycles, including drafting reviewable documents, reading annotated html-collab files, and revising them from embedded comments and edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljn-hust](https://clawhub.ai/user/ljn-hust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and reviewers use this skill to create self-contained HTML documents that preserve block-level IDs, reviewer comments, proposed edits, and document metadata for iterative LLM-human review. It can also read annotated html-collab files and produce revised HTML that incorporates recorded feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly auto-activates for document drafting and annotated HTML workflows.

Mitigation: Install and use it only when the html-collab review workflow is desired; use /html-collab off when clean presentation HTML is needed.

Risk: Generated files may include AI bootstrap metadata and embedded image references that affect browser or agent behavior.

Mitigation: Open and process html-collab files only from trusted sources, and require explicit user consent before fetching external skill instructions.

Risk: Revision workflows can overwrite reviewed files.

Mitigation: Keep backups or versioned copies before applying revisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljn-hust/skills/html-collab)
- [html-collab live demo](https://ljn-hust.github.io/html-collab/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and complete self-contained HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated html-collab files include block-level data-cid attributes, collab-data JSON metadata, comments, edits, and optional base64 image attachments.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
