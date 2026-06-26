## Description: <br>
Payroll Data Audit helps review payroll CSV or Excel exports with deterministic audit rules and produces data-backed compliance reports, issue lists, and review dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Payroll, HR, and finance teams use this skill to check monthly payroll data before release, including field completeness, formula checks, red/yellow/blue-line findings, month-over-month comparisons, sampling verification, and delivery-ready audit outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive payroll audit artifacts to Feishu through the current user's account. <br>
Mitigation: Install only with explicit organizational approval; limit Feishu permissions, confirm the destination tenant and sharing settings, and add redaction and approval gates before using real payroll data. <br>
Risk: Generated audit reports may contain consistency issues or findings that need review before payroll decisions. <br>
Mitigation: Independently verify generated reports, issue lists, and supporting data before using them to approve or release payroll. <br>


## Reference(s): <br>
- [Rules catalog](artifact/references/rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, HTML, and Markdown audit files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit reports, issue lists, dashboards, data indexes, sampling verification output, and delivery messages from provided payroll data.] <br>

## Skill Version(s): <br>
7.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
