## Description: <br>
Batch-convert Hancom HWP/HWPX documents to PDF, HWPX, DOCX, ODT, HTML, RTF, TXT, and image formats on Windows using HWP COM automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to plan and run batch conversion of Korean Hancom HWP/HWPX files, usually from folders or multi-file selections. It is intended for Windows environments with Hancom HWP installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an option that can automatically approve Hancom HWP security prompts during automation. <br>
Mitigation: Keep auto-allow disabled for untrusted documents, and enable it only in controlled conversion runs where bypassing those prompts is acceptable. <br>
Risk: Unattended conversion can process many local documents and write outputs or reports to target folders. <br>
Mitigation: Use plan-only or mock mode first to review target files and output paths before running real conversion. <br>


## Reference(s): <br>
- [Auto-Allow Dialogs](references/auto-allow-dialogs.md) <br>
- [HwpMate Reuse Notes](references/hwpmate-reuse-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/twbeatles/hwp-batch-convert-repo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json, files] <br>
**Output Format:** [Markdown guidance with Python or PowerShell commands, optional JSON reports, and converted document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Real conversion requires Windows, Hancom HWP, and pywin32; mock and plan-only modes are available for validation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
