## Description:

Sync Evernote notebooks to local Markdown, analyze your notes, and update USER.md plus Memory files so the AI has structured context about who you are.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxiaom](https://clawhub.ai/user/hxiaom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to sync Evernote or Yinxiang notebooks into local Markdown, analyze note content, and update USER.md plus memory files with structured personal context for an AI assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad private notebook access can expose sensitive personal notes to the agent during analysis.

Mitigation: Use a limited notebook set where possible and confirm the scope before syncing or analyzing notes.

Risk: Long-term memory updates can preserve sensitive or incorrect personal facts.

Mitigation: Review proposed USER.md and memory-file changes before writing, and remove or correct sensitive entries.

Risk: Scheduled sync can repeatedly update memory from personal notes without fresh review.

Mitigation: Delay recurring sync setup until disable and removal steps are clear.

Risk: Evernote tokens may be exposed if stored in shell profiles or command history.

Mitigation: Avoid storing tokens in persistent shell configuration or command history; prefer safer local secret handling.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Pandoc Installation](https://pandoc.org/installing.html)
- [Yinxiang Developer Token](https://app.yinxiang.com/api/DeveloperToken.action)
- [Evernote Developer Token](https://www.evernote.com/api/DeveloperToken.action)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, USER.md and memory-file Markdown, plus concise status text and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local evernote-backup database path and local Python, pandoc, evernote-backup, beautifulsoup4, and lxml dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
