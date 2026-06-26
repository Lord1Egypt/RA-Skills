## Description: <br>
A customs declaration assistant that helps users upload trade documents, classify document types, extract structured customs data, generate customs Excel output, and run compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axlemax](https://clawhub.ai/user/axlemax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade and customs operations users use this skill to process user-selected invoices, packing lists, bills of lading, and related customs documents through the DaoFei/Leap platform. It supports document upload, classification review, declaration data extraction, Excel result download, and non-blocking compliance guidance. <br>

### Deployment Geography for Use: <br>
Global; customs guidance is tailored to China customs declaration workflows. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends selected customs documents to the DaoFei/Leap platform, and those files may contain commercially sensitive trade data. <br>
Mitigation: Use the skill only when authorized to transmit the selected documents, confirm the file list before upload, and delete local task folders when they are no longer needed. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Configure LEAP_API_KEY through the platform environment settings and do not paste the key into chat or commit it to files. <br>
Risk: Task-management commands such as list, cancel, and retry can affect platform tasks. <br>
Mitigation: Use list, cancel, and retry only for tasks that belong to the current user and workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axlemax/openclaw-skill-customs) <br>
- [DaoFei/Leap service homepage](https://platform.daofeiai.com) <br>
- [API_REFERENCE.md](artifact/references/API_REFERENCE.md) <br>
- [COMPLIANCE_RULES.md](artifact/references/COMPLIANCE_RULES.md) <br>
- [FIELD_GUIDE.md](artifact/references/FIELD_GUIDE.md) <br>
- [FILE_TYPES.md](artifact/references/FILE_TYPES.md) <br>
- [INDUSTRY_RULES.md](artifact/references/INDUSTRY_RULES.md) <br>
- [INTERACTION.md](artifact/references/INTERACTION.md) <br>
- [MODIFICATION.md](artifact/references/MODIFICATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with JSON snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local task files such as classification results, customs payloads, downloaded Excel outputs, and compliance notes during user-approved workflows.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
