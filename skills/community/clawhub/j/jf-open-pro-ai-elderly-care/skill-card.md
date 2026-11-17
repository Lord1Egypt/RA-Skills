## Description:

杰峰开放平台老人看护技能。适配独居、日间无人看护老人场景，全天候守护居家安全与健康，帮助家属实时掌握老人状态，轻松远程看护，消除照护顾虑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and care operations teams use this skill to manage JFTech elderly-care devices, query fall and abnormal-behavior alarms, review routine and diet statistics, and adjust elder-care monitoring settings.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill handles JF app secrets, authorization tokens, device identifiers, and elder-care records.

Mitigation: Install only from the trusted publisher, keep credentials in protected environment variables, avoid passing secrets on shared command lines, and rotate exposed credentials.

Risk: The skill can change elder-care monitoring settings, including service state and abnormal-behavior alert thresholds.

Mitigation: Review service-disable and threshold-change commands before execution and require operator confirmation for changes that affect monitoring coverage.

Risk: The security summary notes a hard-coded China API endpoint and missing confirmation safeguards.

Mitigation: Confirm the intended region before use and prefer explicit region or endpoint configuration where supported by the runtime environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-elderly-care)
- [JFTech developer platform](https://developer.jftech.com)
- [JFTech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [JFTech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [JFTech package card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech credentials, authorization token, device identifier, and an active elderly-care service package.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
