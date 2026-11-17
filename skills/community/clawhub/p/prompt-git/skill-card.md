## Description:

Git for your prompts. Track every change, diff versions, rollback mistakes, never lose a good prompt again. All local, zero dependencies, works offline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers, prompt engineers, and other AI users use Prompt Git to save, diff, tag, search, export, import, and roll back text prompts in a local offline repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poisoned shared, synced, or imported PromptGit repository metadata may expose local file contents.

Mitigation: Review the skill before installing in those workflows, keep PromptGit repositories private, and import or sync only trusted repository metadata.

Risk: Prompt history is stored as local JSON and text files and may contain sensitive prompts or regulated data.

Mitigation: Avoid storing secrets or regulated data unless filesystem permissions, encryption, and access controls protect the storage directory.

Risk: Overwrite, manual deletion, or concurrent PromptGit processes can cause data loss or repository corruption.

Mitigation: Back up the repository before using overwrite or manual deletion workflows and avoid running multiple PromptGit commands against the same repository simultaneously.

## Reference(s):

- [Prompt Git ClawHub listing](https://clawhub.ai/theshadowrose/skills/prompt-git)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code references, JSON configuration examples, and local file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented workflow is local and offline, uses Python standard library scripts, and writes prompt history, exports, and markdown files on the user's filesystem.]

## Skill Version(s):

1.0.2 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
