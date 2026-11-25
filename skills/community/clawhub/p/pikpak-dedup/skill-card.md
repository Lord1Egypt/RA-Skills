## Description:

Analyze PikPak file listings to identify name-based duplicate and version candidates, then produce a report for human review without moving files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users can review likely duplicate or multi-version media in an explicitly authorized folder before deciding whether to act on any listed item.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filename-based grouping can include files that are not duplicates, and duration is not analyzed.

Mitigation: Review each candidate and its metadata manually; do not treat a candidate group as proof of identical content.

Risk: The benign security verdict has medium confidence and partial scan coverage because some referenced paths were absent from the bundle.

Mitigation: Treat the verdict as limited assurance and review the complete packaged files before relying on it.

Risk: Printed cleanup commands may cause data loss if run, and recoverability is not established.

Mitigation: Verify the current recovery behavior and approve the exact item IDs before any external execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipiguai87-alt/skills/pikpak-dedup)
- [Upstream design notes](references/upstream-design.md)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [Czkawka duplicate detection documentation](https://github.com/qarmin/czkawka/blob/eb8b91dbb4d25dff416202674ee0de84ee4b5e5c/instructions/Instruction_Core.md#L37-L47)
- [rclone hash comparison implementation](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/fs/operations/operations.go#L48-L122)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands]

**Output Format:** [JSON candidate report; optionally printed shell command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidates are heuristic and require review; command text is printed only for explicitly approved IDs from a frozen report and is not executed.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
