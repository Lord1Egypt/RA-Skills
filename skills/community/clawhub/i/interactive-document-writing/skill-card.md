## Description:

Guides agents through interactive, chapter-by-chapter creation, revision, audit, and delivery of long-form documents such as white papers, proposals, manuals, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiargcn](https://clawhub.ai/user/jiargcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and writing-focused agents use this skill to co-create or revise long-form documents through one-question-at-a-time discovery, outline design, chapter drafting, audit, final review, and delivery. It is especially suited to Chinese-first workflows that need persistent progress tracking across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read relevant workspace documents while preparing or revising long-form content.

Mitigation: Run it only in workspaces containing documents the agent is allowed to inspect.

Risk: The skill may create or update Markdown documents and .doc-progress-* state files near the document.

Mitigation: Review file changes before accepting them, especially when revising an existing document.

Risk: The skill may suggest a pandoc conversion command for Word output.

Mitigation: Approve and run conversion commands only after reviewing the exact command and input/output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiargcn/skills/interactive-document-writing)
- [Example session](references/example-session.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance, Shell commands]

**Output Format:** [Markdown documents, structured review reports, progress files, and optional shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first interaction; may create or update Markdown documents and .doc-progress-* state files near the working document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
