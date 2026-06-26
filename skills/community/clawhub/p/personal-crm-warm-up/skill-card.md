## Description: <br>
Identifies contacts you haven't reached out to recently and suggests low-pressure ways to reconnect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this local personal CRM assistant to identify overdue relationship touchpoints and draft low-pressure outreach messages from their own contacts file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled contacts file can contain personal contact names, relationship categories, last interaction dates, and discussion topics. <br>
Mitigation: Review or replace contacts.json before use, and keep the skill local as documented. <br>
Risk: A custom contactsPath causes the skill to read the specified local file. <br>
Mitigation: Only provide a custom contactsPath when you intentionally want the skill to use that file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liverock/personal-crm-warm-up) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with a summary table and drafted outreach messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports limit and category filters; environment variables configure overdue thresholds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
