## Description: <br>
Creates Chinese official documents (gongwen) following GB/T 9704-2012 and common enterprise formatting standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longjf25](https://clawhub.ai/user/longjf25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to draft or format Chinese official and formal work documents such as notices, reports, decisions, replies, letters, and meeting minutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation could apply official-document formatting guidance to unrelated tasks. <br>
Mitigation: Invoke the skill explicitly for Chinese official or formal work document tasks. <br>
Risk: Official, legal, financial, or policy-sensitive drafts may require domain review before use. <br>
Mitigation: Manually review and verify generated content before relying on it in formal settings. <br>
Risk: Template code may write generated documents to a user-selected path. <br>
Mitigation: Run document-generation examples only in intended workspaces and inspect generated files before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longjf25/gongwen-format) <br>
- [GB/T 9704-2012 reference](artifact/gb9704_2012.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and document-template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of DOCX files when the user chooses to run the provided JavaScript template with docx-js.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
