## Description:

Save magnet links, URLs and share links into PikPak, then check each task by its exact ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users can follow the guided steps to save links they are authorized to access, confirm the exact task and file IDs, and review task receipts. The skill also provides an offline checker for task JSON; it does not provide a persistent queue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A task submission or share restore may have succeeded even when the command times out or returns an error, so repeating it can create duplicate work.

Mitigation: Record the exact task or approved file IDs; stop and reconcile uncertain results before authorizing another submission or restore.

Risk: Downloads can consume account quota or overwrite local files.

Mitigation: Use a trusted PikPak CLI installation and confirm the account, selected files, destination path, and overwrite risk before each operation.

## Reference(s):

- [Upstream design, scope, and limitations](references/upstream-design.md)
- [PikPak connected-app download speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON task-receipt output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guided single-operation steps; the offline receipt checker reports a task status as JSON.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
