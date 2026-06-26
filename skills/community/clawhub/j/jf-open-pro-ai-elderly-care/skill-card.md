## Description: <br>
JF Open Pro AI Elderly Care helps authorized users monitor JF Tech elderly-care devices for falls, abnormal behavior, service status, alert thresholds, and daily or weekly activity and diet statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, care-service operators, and authorized caregivers use this skill to query and manage JF Tech elderly-care monitoring for bound online devices with an active service plan. <br>

### Deployment Geography for Use: <br>
China mainland, Asia, Europe, and North America, based on the documented JF endpoint regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive monitoring data about an elderly or vulnerable person. <br>
Mitigation: Use it only with authorization to monitor the device and with appropriate notice or consent from the person being monitored. <br>
Risk: JF app secrets, authorization tokens, device serial numbers, and user IDs can expose accounts or monitored-device data if leaked. <br>
Mitigation: Store these values in protected environment variables or a secret manager and avoid passing them where command history or process lists may reveal them. <br>
Risk: The skill can disable monitoring or change abnormal-behavior thresholds. <br>
Mitigation: Confirm changes before applying them and restrict use on shared systems or unattended automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-ai-elderly-care) <br>
- [JF Open Platform](https://developer.jftech.com) <br>
- [JF signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh) <br>
- [JF timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh) <br>
- [JF service card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF credentials, authorization token, device serial number, user ID, and an online bound device with the elderly-care service plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
