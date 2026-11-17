## Description:

Use this skill to query Google NotebookLM notebooks from agent coding environments for source-grounded, citation-backed answers, notebook management, source uploads, and media artifact generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicseek](https://clawhub.ai/user/magicseek)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to authenticate with Google NotebookLM, manage notebooks and sources, query notebook content, and generate NotebookLM media artifacts without leaving their coding agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist Google NotebookLM session credentials and, when used, Z-Library session data.

Mitigation: Use a dedicated Google account where possible, avoid shared machines, and review permissions for the skill data directory.

Risk: Notebook and source management commands can upload, sync, rename, or delete user content.

Mitigation: Review command targets before execution and prefer dry-run or explicit notebook selection for sync and delete workflows.

Risk: Untrusted input could cause unsafe command routing or repeated follow-up queries.

Mitigation: Do not let untrusted content choose script names or trigger automated query loops without user review.

## Reference(s):

- [NotebookLM Skill on ClawHub](https://clawhub.ai/magicseek/skills/nblm)
- [NotebookLM](https://notebooklm.google.com)
- [Authentication Notes](AUTHENTICATION.md)
- [nblm API Reference](references/api_reference.md)
- [nblm Troubleshooting Guide](references/troubleshooting.md)
- [nblm Usage Patterns](references/usage_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and NotebookLM response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also guide generation or download of NotebookLM media artifacts such as audio, slide decks, and infographics.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
