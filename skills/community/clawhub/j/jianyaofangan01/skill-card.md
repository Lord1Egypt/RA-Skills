## Description: <br>
This skill guides users through a structured Chinese-language workflow for drafting brief IT planning or work proposals and producing Word documents from a user-provided .docx template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomm1399](https://clawhub.ai/user/tomm1399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, proposal writers, and IT project teams use this skill to draft government, state-owned-enterprise, IT planning, cybersecurity, and informatization proposals through staged background, current-state, requirements, planning, and budget sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposal content may include confidential business, government, security, budget, or infrastructure information. <br>
Mitigation: Use non-sensitive or redacted inputs unless the user has approved the environment and sharing path for that information. <br>
Risk: The workflow can persist proposal state locally as JSON files. <br>
Mitigation: Delete saved proposal state when the work is complete and avoid storing sensitive details in resumable state files. <br>
Risk: The workflow can upload generated documents to Feishu cloud storage. <br>
Mitigation: Confirm the target Feishu folder and cloud-upload approval before upload, or request local-only output for sensitive proposals. <br>


## Reference(s): <br>
- [Proposal template reference](references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON state examples, Python/docx code snippets, and generated .docx document workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save and resume proposal state in local JSON files and can guide upload of generated documents to a user-specified Feishu cloud folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
