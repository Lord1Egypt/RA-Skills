## Description:

Local file knowledge base with LLM-powered indexing and Q&A that scans local documents, extracts summaries, tags, and tables of contents, and answers questions by retrieving relevant files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[congshengwu](https://clawhub.ai/user/congshengwu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to build a lightweight local knowledge base over selected documents, refresh per-file metadata, and ask cited questions against indexed content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recursively process private documents in the selected folder.

Mitigation: Use a narrowly scoped test folder, avoid broad home or cloud-sync directories, and exclude financial, legal, credential-heavy, or otherwise sensitive files.

Risk: The security summary flags unsafe shell path templates.

Mitigation: Review generated shell actions before execution and prefer sandboxed directories until path-safe handling and explicit privacy prompts are added.

Risk: Document text is processed for summaries and question answering.

Mitigation: Install only when users are comfortable making the chosen folder searchable by the agent and having document text used for indexing and answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/congshengwu/skills/personal-kb-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with cited source lists, progress summaries, JSON metadata files, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates .kb-config.json in the working directory and .kb-meta.json in the selected watched directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
