## Description:

Tracks, commits, compares, and restores OpenClaw configuration changes with local Git history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Git Watcher to create local versioned checkpoints of OpenClaw configuration, inspect diffs and history, and restore a known-good configuration after a regression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify and commit files under ~/.openclaw, including configuration and credential-related paths.

Mitigation: Back up ~/.openclaw before commit or restore operations, avoid tracking live credentials, and review the exact files being staged.

Risk: Restore behavior can overwrite local OpenClaw configuration data.

Mitigation: Review the preview diff, require explicit confirmation before restore, and keep the previous state available for undo or recovery.

Risk: Diff, log, and commit-message output may expose sensitive configuration details.

Mitigation: Treat generated output as sensitive, redact credentials before sharing, and avoid publishing raw logs or diffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/git-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Git commits, restore tracked OpenClaw configuration files, and report validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
