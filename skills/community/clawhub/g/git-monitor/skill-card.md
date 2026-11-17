## Description:

Git Monitor helps agents add, list, check, and remove monitored Git repositories, pull updates, and summarize changes across GitHub, GitLab, Gitee, and other Git platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushenjie](https://clawhub.ai/user/gushenjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to track updates across Git repositories, synchronize local copies, and receive concise change summaries or Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe Git command execution can expose users to command-injection or unintended command behavior when repository inputs are not trusted.

Mitigation: Use only trusted repository URLs and review command proposals before execution; publisher should replace shell-string Git commands with argument-safe process calls.

Risk: Repository checks can overwrite local work when hard resets are used during synchronization.

Mitigation: Avoid monitoring repositories that contain uncommitted local work, and require explicit confirmation before destructive Git operations.

Risk: Feishu notifications can disclose commit and changed-file metadata to an external chat service.

Mitigation: Enable notifications only for repositories whose metadata may be shared with that chat, and require explicit consent before credential lookup or outbound messages.

Risk: Bundled configuration includes example monitored repositories and local paths.

Mitigation: Start releases from an empty configuration and let users add repositories intentionally after installation.

## Reference(s):

- [ClawHub Git Monitor Skill Page](https://clawhub.ai/gushenjie/skills/git-monitor)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository status, commit summaries, changed-file statistics, local path details, and notification setup guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
