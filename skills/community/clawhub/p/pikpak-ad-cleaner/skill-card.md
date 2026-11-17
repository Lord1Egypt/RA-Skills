## Description:

Scans authorized PikPak folders for possible advertising or promotional files, produces a reviewable risk-tier report, and only prints cleanup commands after explicit approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review an explicitly authorized PikPak folder for likely advertising or promotional files. It produces a report for manual review and, only after explicit approval, prints cleanup commands for separate execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filename-based rules can misclassify files and do not prove that a candidate's contents are advertising.

Mitigation: Keep reports private and manually review candidates; scan only a folder the user explicitly authorized.

Risk: A printed cleanup command may target the wrong item, and PikPak deletion recoverability is not established.

Mitigation: Before separately executing a command, verify the frozen report, each approved ID, and current recovery behavior; this skill never executes cleanup commands.

## Reference(s):

- [Upstream design notes](references/upstream-design.md)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands, Guidance]

**Output Format:** [JSON scan report and review guidance, with optional shell cleanup commands printed only after approval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only scanning; cleanup commands are proposals and are never executed by the skill.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
