## Description:

Turns Obsidian into a dual-layer knowledge base for AI agents with daily incremental ingestion, structured indexing, and context injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warren2008-2020-spec](https://clawhub.ai/user/warren2008-2020-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers and teams use this skill to organize Obsidian notes into INBOX and WIKI layers so an agent can reuse summaries, Q&A cards, and concept cards during reports, analysis, and writing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent indexing and automatic context injection can expose sensitive Obsidian vault content.

Mitigation: Limit readable vault folders, exclude confidential notes, and define how generated memory summaries can be reviewed, deleted, or disabled.

Risk: Installer and scheduled workflow setup may run unverified commands or configuration.

Mitigation: Use a pinned or verified installer and review scheduled commands before enabling the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warren2008-2020-spec/skills/obsidian-knowledge-base)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with templates, directory conventions, Python example code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily summary and retrieval workflow guidance for selected Obsidian vault content]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
