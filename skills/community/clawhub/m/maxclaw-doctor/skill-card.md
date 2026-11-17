## Description:

Provides file protection for OpenClaw workflows by indexing file operations and supporting deleted-file recovery and modification rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to protect project files during OpenClaw-assisted edits by recording modifications, moving deletions into recoverable storage, and guiding rollback or restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes curl-to-bash installers, sudo package installs, and shell-profile edits.

Mitigation: Review installation commands separately and execute them manually only when they match the user's platform and trust policy.

Risk: MiniVCS can copy, move, restore, and retain files available to the user account outside a project directory.

Mitigation: Use it only on an explicit project directory and avoid secrets, credentials, and sensitive files.

Risk: Retained MiniVCS backups may contain file contents after the original task is complete.

Mitigation: Verify cleanup of ~/.openclaw/minivcs records and backups when they are no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oreoandyuumi/skills/maxclaw-doctor)
- [Python macOS downloads](https://www.python.org/downloads/macos/)
- [Python Windows downloads](https://www.python.org/downloads/windows/)
- [Tsinghua Homebrew mirror guide](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file-operation records, diffs, snapshots, trash backups, and cleanup notices through MiniVCS.]

## Skill Version(s):

1.0.0 (source: target metadata, release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
