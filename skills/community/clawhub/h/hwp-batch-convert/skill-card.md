## Description: <br>
Batch-convert Hancom HWP/HWPX documents on Windows into PDF and other export formats with planning, mock runs, JSON reporting, and optional whitelisted approval of known Hancom security prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document operations users use this skill to batch-convert folders or sets of Hancom HWP/HWPX files on Windows, usually to PDF or other office/export formats, while previewing planned work and collecting machine-readable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real conversion can fail or behave unexpectedly outside the intended Windows environment with Hancom HWP and pywin32 available. <br>
Mitigation: Preview work with --plan-only --json or validate paths with --mode mock before running real conversion. <br>
Risk: --auto-allow-dialogs can bypass repeated Hancom security prompts for trusted files. <br>
Mitigation: Use it only for trusted inputs; the skill limits clicks to the documented title, body text, and button whitelist and records auto_dialog_* fields for review. <br>
Risk: --overwrite can replace existing output files. <br>
Mitigation: Avoid --overwrite unless replacement is intended and confirm input and output folders during the plan-only preview. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twbeatles/hwp-batch-convert) <br>
- [Auto-allow dialog safety notes](references/auto-allow-dialogs.md) <br>
- [HwpMate reuse notes](references/hwpmate-reuse-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with command examples; optional JSON stdout and report JSON from the conversion script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write converted document files and a report JSON; real conversion depends on Windows, Hancom HWP, and pywin32.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
