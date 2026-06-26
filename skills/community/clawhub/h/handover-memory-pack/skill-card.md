## Description: <br>
Organizes explicit and tacit knowledge for personnel departures or project handovers to reduce information loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and operations teams use this skill to turn handover inputs such as responsibilities, key contacts, tacit knowledge, unresolved items, and risks into reviewable handover drafts and action checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads user-provided files and can summarize sensitive handover material. <br>
Mitigation: Use scoped handover documents, avoid broad private directories, and redact secrets or sensitive personnel details before generating reports. <br>
Risk: Generated handover drafts may include incomplete or privileged operational details if the input is incomplete or overbroad. <br>
Mitigation: Review the draft before sharing, keep sensitive information as references instead of plaintext, and confirm high-risk or privileged items with the appropriate owner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/handover-memory-pack) <br>
- [README](artifact/README.md) <br>
- [Structured specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts and optional JSON or file output from a local Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local user-provided input and can run with python3 on Darwin, Linux, or Win32.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
