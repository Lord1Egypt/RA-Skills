## Description:

自动填写 PingCode/PMS 系统工时记录。支持批量填写多天的工时，自动登录、选择事项类型、填写事项、工时、日期和说明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ww12355](https://clawhub.ai/user/ww12355)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workflow automation users use this skill to run a Playwright script that logs into PingCode/PMS and enters worklog records for one or more dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation can log into a company PMS account and submit worklog entries automatically.

Mitigation: Review the configured dates, work item, hours, and description before every run, and run it only when automatic submission is intended.

Risk: Screenshots saved during login, success, and error flows may contain company or account data.

Mitigation: Delete or disable screenshots when they are not needed, and store any retained screenshots in an approved location.

Risk: The script launches Chromium with --no-sandbox.

Mitigation: Remove --no-sandbox where the local environment supports normal browser sandboxing, and avoid running the script with privileged OS permissions.

Risk: Using broad or global Playwright dependencies can make runtime behavior harder to reproduce.

Mitigation: Prefer a pinned local Playwright dependency for repeatable execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ww12355/skills/pms-worklog)
- [Publisher profile](https://clawhub.ai/user/ww12355)
- [PingCode/PMS login](https://pms.aispeech.com.cn)
- [PingCode/PMS worklog page](https://pms.aispeech.com.cn/workspace/workload/insight)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs an agent to run a Playwright automation script that prints progress and saves screenshots.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
