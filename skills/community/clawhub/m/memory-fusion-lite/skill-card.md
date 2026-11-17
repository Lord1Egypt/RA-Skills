## Description:

Memory Fusion Lite helps Dreaming users maintain a rolling seven-day memory update area by incrementally scanning OpenClaw session logs, filtering recursion, and supporting weekly memory governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users with Dreaming enabled use this skill to keep MEMORY.md current through incremental daily extraction, a rolling recent-updates zone, anti-recursion safeguards, and weekly promotion or pruning of memory entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans private conversation logs as part of its memory workflow.

Mitigation: Install only where that access is acceptable, restrict file permissions and allowed paths, and run the scanner in preview before enabling automated use.

Risk: The workflow can change persistent agent memory and weekly archive files.

Mitigation: Keep backups of MEMORY.md and require review before promoting, pruning, or deleting memory entries.

Risk: Security evidence flags weak safeguards and a redaction bug.

Mitigation: Fix redaction before use and review scan output for sensitive content before it is summarized or written to memory.

## Reference(s):

- [Memory Fusion Lite ClawHub Release](https://clawhub.ai/dxiaofeng0811-lgtm/skills/memory-fusion-lite)
- [A-prime Rolling Seven-Day Zone](references/a-prime-zone.md)
- [Anti-Recursion Safeguards](references/anti-recursion.md)
- [Byte Cursor Incremental Scan](references/byte-cursor.md)
- [Memory Fusion Lite vs Dreaming](references/diff-from-dreaming.md)
- [Weekly Memory Governance](references/weekly-governance.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated memory-entry text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent memory files and weekly archive files when used with the documented cron workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2026.4.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
