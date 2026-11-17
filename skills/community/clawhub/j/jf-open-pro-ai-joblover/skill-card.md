## Description:

JFTech job patrol skill for monitoring on-duty status, sending arrival and departure notifications, detecting on-duty abnormal behavior, and reporting behavior statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and security teams use this skill to manage JFTech job-patrol monitoring, query service status, review on-duty alarms, manage patrol schedules, and inspect behavior statistics for authorized devices.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill accesses employee-monitoring data and alarm media for on-duty behavior.

Mitigation: Use it only in authorized deployments with appropriate workplace monitoring approvals and access controls.

Risk: The scripts require credentials and tokens and verbose mode can expose request details.

Mitigation: Provide credentials through protected runtime configuration, avoid verbose mode with real credentials, and redact logs before sharing.

Risk: The skill can disable monitoring or delete patrol plans.

Mitigation: Require human approval before service switch changes or patrol-plan deletion.

Risk: Calls may target the wrong JFTech regional endpoint.

Mitigation: Confirm the intended regional endpoint before API use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-joblover)
- [JFTech developer platform](https://developer.jftech.com)
- [JFTech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [JFTech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [JFTech package card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech credentials, an online bound device, and an enabled job-patrol package.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
