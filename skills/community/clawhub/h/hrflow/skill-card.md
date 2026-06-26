## Description: <br>
Automate HR workflows including benefits enrollment, onboarding, and payroll integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and People Ops teams use this skill to draft and operate workflows for onboarding, benefits enrollment, payroll sync validation, employee communications, document signing, and audit reporting across HR systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests powerful HR, payroll, and messaging access without enough concrete limits for sensitive employee workflows. <br>
Mitigation: Install only in an authorized HR or People Ops environment, start with least-privilege test credentials, and require human approval for payroll, benefits, provisioning, purchasing, and employee-record changes. <br>
Risk: Employee data, audit logs, and integration outputs may include sensitive personal, payroll, or benefits information. <br>
Mitigation: Verify where logs and employee data are stored before using real employee information, and keep production secrets scoped to the minimum systems needed. <br>


## Reference(s): <br>
- [ClawHub Hrflow Skill Page](https://clawhub.ai/ncreighton/hrflow) <br>
- [Declared Skill Homepage](https://github.com/ncreighton/empire-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with workflow examples, reports, configuration variables, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference HRIS, payroll, messaging, email, document-signing, and compliance integrations that require separate credentials and human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
