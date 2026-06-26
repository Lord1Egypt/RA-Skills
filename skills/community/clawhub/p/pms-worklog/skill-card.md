## Description: <br>
自动填写 PingCode/PMS 系统工时记录，支持批量填写多天的工时，自动登录、选择事项类型、填写事项、工时、日期和说明。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ww12355](https://clawhub.ai/user/ww12355) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees who use PingCode/PMS can use this skill to automate routine worklog entry for one or more dates. It is intended for cases where the user has reviewed the target work item, hours, dates, and description before running the automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can log into PMS and submit business work records automatically without a final confirmation step. <br>
Mitigation: Run it only when you intend to submit records, and review the configured dates, work item, hours, description, selectors, and submit behavior before execution. <br>
Risk: The skill uses PMS account credentials and may save screenshots containing PMS information. <br>
Mitigation: Use environment variables for credentials, avoid hardcoding secrets, and delete saved PMS screenshots after troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ww12355/pms-worklog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell and JavaScript configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The automation can submit PMS worklog records and save troubleshooting screenshots when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
