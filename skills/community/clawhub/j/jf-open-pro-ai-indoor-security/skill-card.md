## Description: <br>
Provides JF Tech indoor-security API guidance and scripts for checking service state, configuring abnormal-alarm reminders, querying alarms and statistics, and managing household members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and JF Tech indoor-security operators use this skill to operate device security features through JF Tech Open Platform APIs. It supports status checks, service changes, alarm review, household member management, and occupancy statistics after required credentials, device binding, and service subscription are configured. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles home-security credentials, household telemetry, and biometric member records. <br>
Mitigation: Use dedicated least-privilege credentials where possible, avoid exposing secrets in shell history or process-visible command lines, and restrict access to authorized operators. <br>
Risk: The skill can add, update, or delete members, upload face images, and change indoor-security service state. <br>
Mitigation: Require explicit human confirmation before member mutations, face-image uploads, or service state changes. <br>
Risk: Alarm media, occupancy statistics, and member records can reveal sensitive household activity. <br>
Mitigation: Minimize retention and sharing of returned data, and review outputs before storing or forwarding them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jftech/jf-open-pro-ai-indoor-security) <br>
- [JF Tech Open Platform](https://developer.jftech.com) <br>
- [JF Tech Signature Algorithm](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh) <br>
- [JF Tech Timestamp Algorithm](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh) <br>
- [JF Tech Package Card Usage](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF Tech credentials, device serial number, authorization token, and configured indoor-security service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
