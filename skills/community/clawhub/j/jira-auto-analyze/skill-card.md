## Description: <br>
Jira Auto Analyze checks Jira tickets for required environment, channel, version, and log details, then uses configured rules to assign or return tickets with replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei19820201](https://clawhub.ai/user/liuwei19820201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations engineers use this skill to review new Jira tickets in filter 13123, check whether required troubleshooting information is present, and route complete tickets according to configured assignment rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded real-looking Jira credentials may expose account access if installed as-is. <br>
Mitigation: Remove the stored password, rotate the exposed credential, and load a per-user or least-privilege service account secret from a secure secret source. <br>
Risk: The skill can modify live Jira tickets by assigning issues and adding comments. <br>
Mitigation: Run dry-run first, require authorization for the target Jira filter, and enable monitoring and rollback before scheduled live execution. <br>
Risk: Incorrect filter or assignment rules could route tickets to the wrong owner or return tickets unnecessarily. <br>
Mitigation: Confirm filter 13123 and all assignment, rejection, and priority rules with the owning team before production use. <br>
Risk: Debug login or screenshot scripts may capture sensitive Jira session or ticket information. <br>
Mitigation: Avoid debug login and screenshot workflows except in controlled troubleshooting environments with approved data handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwei19820201/jira-auto-analyze) <br>
- [usage_guide.md](references/usage_guide.md) <br>
- [jira_structure.md](references/jira_structure.md) <br>
- [Configured Jira server](http://jira.51baiwang.com) <br>
- [Ticket submission standard](http://confluence.51baiwang.com/pages/viewpage.action?pageId=80049485) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode before making live Jira ticket changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
