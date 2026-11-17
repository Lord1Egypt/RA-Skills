## Description:

Batch-converts Hancom HWP/HWPX documents to PDF, HWPX, DOCX, ODT, HTML, RTF, TXT, and image formats on Windows using HWP COM automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and document-processing agents use this skill to plan and run Korean-friendly batch conversion of Hancom HWP/HWPX files across folders or file lists, typically to PDF or office document formats. It is intended for Windows environments with Hancom HWP installed, with mock and plan-only modes available for validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional auto-allow feature can approve matching Hancom HWP security dialogs without manual review.

Mitigation: Use --auto-allow-dialogs only with trusted HWP/HWPX files in a controlled Windows desktop session, and review auto_dialog_events in stdout JSON or the report JSON after execution.

Risk: Batch conversion can write many output files and may place results beside source files or in a selected output folder.

Mitigation: Run --plan-only --json first, choose a controlled output directory when possible, and review planned output paths before real conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twbeatles/skills/hwp-batch-convert-repo)
- [Auto-allow dialog safety notes](references/auto-allow-dialogs.md)
- [HwpMate reuse notes](references/hwpmate-reuse-notes.md)
- [HwpMate project referenced by the skill](https://github.com/twbeatles/HwpMate)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON summaries, JSON report files, and converted document/image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports plan-only previews, mock execution, same-location or output-directory writes, collision renaming, and optional JSON reporting.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
