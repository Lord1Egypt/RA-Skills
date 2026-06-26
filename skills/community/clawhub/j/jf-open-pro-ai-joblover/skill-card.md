## Description: <br>
JF Tech Open Platform job patrol skill for monitoring employee on-duty status, sending on-duty, off-duty, and abnormal-behavior notifications, and querying behavior records and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and authorized developers use this skill to manage JF Tech job patrol service state, patrol plans, abnormal-behavior alarms, and behavior statistics for configured workplace devices. <br>

### Deployment Geography for Use: <br>
China mainland, Asia, Europe, and North America where the documented JF Tech endpoints are configured. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate employee-monitoring and workplace surveillance controls. <br>
Mitigation: Install and use it only for devices and employees that the operator is authorized to monitor, after confirming legal, labor, and privacy obligations. <br>
Risk: The skill uses sensitive API credentials, authorization tokens, device serial numbers, signatures, and alarm media. <br>
Mitigation: Store credentials in controlled environment variables, avoid pasting secrets into shell history or shared logs, restrict alarm media access, and rotate any real credentials that resemble examples. <br>
Risk: Verbose command output can expose generated curl commands, headers, signatures, tokens, or API responses. <br>
Mitigation: Disable verbose/debug output in shared environments and redact headers, tokens, signatures, device identifiers, and alarm links before sharing logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-ai-joblover) <br>
- [JF Tech developer platform](https://developer.jftech.com) <br>
- [JF Tech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh) <br>
- [JF Tech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh) <br>
- [JF Tech package card documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses when script flags request JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require JF Tech credentials, a device serial number, user authorization, and an enabled job patrol service package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
