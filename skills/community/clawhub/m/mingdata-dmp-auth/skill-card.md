## Description: <br>
Manages Mingdata DMP API credentials and provides a unified gateway for signing requests, validating credentials, and calling Mingdata DMP APIs for related skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Mingdata DMP access credentials and route related DMP audience, insight, and delivery skills through a shared authenticated API caller. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived Mingdata DMP credentials that could be exposed through chat, logs, persistent configuration, or local credential files. <br>
Mitigation: Use a scoped secret manager or controlled environment variables, avoid pasting secrets into ordinary chat, restrict credential-file permissions to the owner, and rotate credentials if they may have been exposed. <br>
Risk: Shared credentials may be reused across related DMP skills and sessions. <br>
Mitigation: Use least-privileged DMP credentials, review installed dependent skills before enabling shared access, and remove or rotate credentials when the access is no longer needed. <br>
Risk: The skill sends signed HTTP requests to Mingdata DMP endpoints based on caller-supplied endpoint paths and JSON payloads. <br>
Mitigation: Review endpoint paths and request bodies before execution, confirm outbound access to open.mingdata.com is expected, and monitor API activity for unintended calls. <br>


## Reference(s): <br>
- [Mingdata Open Platform](https://open.mingdata.com) <br>
- [Mingdata Dmp Auth release page](https://clawhub.ai/mingri26/mingdata-dmp-auth) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mingdata DMP credentials and outbound HTTPS access to open.mingdata.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
