## Description: <br>
杰峰开放平台室外安防技能。提供车辆检测、异常告警、智能检测、灵敏度设置、检测区域配置、推送计划管理等功能，全面提升室外安防监控能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate JF outdoor-security camera features from an agent, including AI analysis service toggles, alert configuration, detection zones, push schedules, vehicle records, statistics, and device credential sync. <br>

### Deployment Geography for Use: <br>
Global, with documented JF API regions for China Mainland, Asia, Europe, and North America. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change outdoor-security monitoring behavior, including service switches, alert settings, detection zones, push plans, and vehicle records. <br>
Mitigation: Require explicit user confirmation before service toggles, deletes, credential sync, or configuration changes. <br>
Risk: The skill handles JF application secrets, authorization tokens, device identifiers, and device login credentials. <br>
Mitigation: Use environment variables or a secret manager, avoid passing secrets directly on command lines, and rotate any credential-like values that may have been embedded or exposed. <br>
Risk: The security verdict is suspicious because the skill controls security-camera settings and sensitive credentials. <br>
Mitigation: Install only when the publisher is trusted and the user intends to grant an agent control over the relevant JF outdoor-security account and device. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-ai-outdoor) <br>
- [JF developer platform](https://developer.jftech.com) <br>
- [JF signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh) <br>
- [JF timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh) <br>
- [JF API documentation](https://docs.jftech.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, API calls, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF account, device, authorization, application credentials, and an active outdoor-security AI package.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
