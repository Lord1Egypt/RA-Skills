## Description:

Notebooklm helps agents use Google NotebookLM to add sources, ask cited questions, generate Studio content, download artifacts, and manage notebooks programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinzien1107-ctrl](https://clawhub.ai/user/kevinzien1107-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to automate NotebookLM research workflows, including importing sources, asking cited questions, creating study or presentation artifacts, and managing notebooks from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add local files, Google Drive documents, and bulk research results to an authenticated Google NotebookLM account.

Mitigation: Require explicit per-source approval before importing local files, Drive documents, or bulk research results.

Risk: The skill uses an unofficial client for undocumented Google APIs that may change or fail without notice.

Mitigation: Review the upstream client before installation and use the official NotebookLM web interface as a fallback for failed or changed operations.

Risk: The skill can perform account-affecting actions such as exports, sharing changes, profile switches, and global language changes.

Mitigation: Require explicit approval for those actions and prefer a dedicated Google account or isolated profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinzien1107-ctrl/skills/notebooklm-ksyun)
- [notebooklm-py upstream library](https://github.com/teng-lin/notebooklm-py)
- [notebooklm-py troubleshooting docs](https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and occasional JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require approval before long-running generation, filesystem downloads, note writes, destructive actions, sharing changes, or sensitive source imports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
