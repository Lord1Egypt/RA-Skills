## Description:

Scan a PikPak folder for likely ad and promotional files, group candidates for review, and print a cleanup command only for explicitly approved items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users use this skill to review a folder for likely promotional clutter and prepare a manually approved cleanup command. It does not delete files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner's coverage is partial, and the host runtime permissions are unknown; folder scanning and report writing may exceed the scope a user intended.

Mitigation: Authorize only the intended folder and review the available tool permissions before scanning.

Risk: Reports can contain private file paths, and a printed cleanup command can remove cloud files if run.

Mitigation: Keep reports in a controlled private location, review the complete frozen report and exact IDs, and run no cleanup command without explicit approval and verified recovery behavior.

## Reference(s):

- [PikPak Ad Cleaner release](https://clawhub.ai/pipiguai87-alt/skills/pikpak-ad-cleaner)
- [Connected apps transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [Connected apps speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [Upstream design notes](references/upstream-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown scan summary, JSON report, and explicitly approved cleanup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Files are grouped as high, review, or protected candidates; cleanup commands are printed for approved IDs and are never executed by the skill.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
