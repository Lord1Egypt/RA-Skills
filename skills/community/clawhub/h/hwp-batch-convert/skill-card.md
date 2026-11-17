## Description:

Batch-convert Hancom HWP and HWPX documents on Windows into PDF and other export formats with plan-only, mock, real conversion, and machine-readable report workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and Korean document workflow users use this skill to plan and run batch conversion of HWP/HWPX files on Windows systems with Hancom HWP installed. It is suited for folder-level or multi-file exports to PDF and common document or image formats, with optional JSON reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional security-dialog auto-approval may click a matching Hancom or spoofed dialog outside the intended conversion flow.

Mitigation: Use plan-only first, prefer running without --auto-allow-dialogs, and enable auto-approval only in a controlled desktop session with trusted documents.

Risk: Real conversion depends on a Windows desktop environment with Hancom HWP and pywin32 available.

Mitigation: Use mock mode to validate paths and output structure before running real conversion on the target Windows host.

## Reference(s):

- [Hwp Batch Convert README](README.md)
- [Auto-Allow Dialogs](references/auto-allow-dialogs.md)
- [HwpMate Reuse Notes](references/hwpmate-reuse-notes.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, JSON]

**Output Format:** [Markdown guidance with shell commands; converter output may include converted files and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports plan-only and mock modes before real Windows Hancom HWP conversion.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
