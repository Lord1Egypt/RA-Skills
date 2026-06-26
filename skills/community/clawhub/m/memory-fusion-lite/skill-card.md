## Description: <br>
Memory Fusion Lite adds lightweight memory maintenance for OpenClaw users with Dreaming enabled, using incremental session scanning, a rolling seven-day memory zone, anti-recursion safeguards, and weekly memory governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users who already run Dreaming use this skill to keep MEMORY.md fresher through daily incremental extraction and weekly promotion or pruning of recent memory entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw conversation history, which may contain sensitive personal, project, or credential-adjacent information. <br>
Mitigation: Install only in workspaces where session-log processing is intended, confirm where summarization data is sent, and review generated memory entries before relying on them. <br>
Risk: The skill updates local memory files and can prune or promote entries during scheduled runs. <br>
Mitigation: Test manual commands first, keep backups of MEMORY.md, and verify weekly pruning behavior before enabling automatic schedules. <br>


## Reference(s): <br>
- [A Prime Zone](references/a-prime-zone.md) <br>
- [Anti Recursion](references/anti-recursion.md) <br>
- [Byte Cursor](references/byte-cursor.md) <br>
- [Diff From Dreaming](references/diff-from-dreaming.md) <br>
- [Weekly Governance](references/weekly-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MEMORY.md rolling-zone updates, weekly archive notes, and status summaries when executed in a configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2026.4.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
