## Description: <br>
Converts PDF, DOC, DOCX, and PPTX office documents to Markdown with legacy .doc extraction support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lkyyyy320](https://clawhub.ai/user/Lkyyyy320) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert office documents into Markdown so agents can read, summarize, analyze, or process document content in text-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports automatic Python package installation and raw shell commands on user-controlled file paths. <br>
Mitigation: Use trusted documents and safely named paths; prefer preinstalling python-pptx and replacing shell-string execution with argument-array execution before deployment. <br>
Risk: Converted document text, preview output, file paths, errors, and stack traces may expose confidential document information. <br>
Mitigation: Run the skill only where logs and output locations are controlled, and avoid confidential documents unless those controls are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lkyyyy320/office-to-md-v2) <br>
- [OpenClaw office-to-md documentation](https://docs.openclaw.ai/skills/office-to-md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files] <br>
**Output Format:** [Markdown files with JSON or console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a .md file next to the source document and may include preview text, output path, file type, and conversion statistics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact package metadata lists 2.0.0 and nested converter metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
