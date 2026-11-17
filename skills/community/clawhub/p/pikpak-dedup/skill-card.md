## Description:

Identifies likely duplicate or alternate-version files in a PikPak folder and prepares reviewed removal commands without executing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users use this skill to find likely duplicate or multiple-version media files, compare candidates, and decide which files to keep. It produces a frozen report and, only after explicit per-item approval, prints removal commands for separate user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Name or metadata matches can identify different files as candidates, and do not prove identical content.

Mitigation: Inspect each candidate and the report's completeness before approving any item.

Risk: A printed removal command may cause irreversible data loss if executed without confirming recovery behavior and intent.

Mitigation: Verify recovery behavior and explicitly authorize each target before executing commands; the skill itself never executes them.

Risk: An unintended PikPak folder or an untrusted CLI could expose or affect private files; live CLI compatibility is unverified.

Mitigation: Use a trusted PikPak CLI, explicitly select the authorized folder, and keep reports private.

## Reference(s):

- [Upstream design and implementation notes](references/upstream-design.md)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [ClawHub skill page](https://clawhub.ai/pipiguai87-alt/skills/pikpak-dedup)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands]

**Output Format:** [JSON or readable text reports; shell removal commands are printed only after explicit per-item approval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate matches are not proof of identical content. Commands are never executed by the skill.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
