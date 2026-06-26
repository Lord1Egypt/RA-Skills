## Description: <br>
Deploys the Huo Xiaoding Spring Boot service to a server by building the JAR, uploading it, backing up the previous version, restarting the service, and reporting status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adtomato](https://clawhub.ai/user/adtomato) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage the Huo Xiaoding service can use this skill to package the Spring Boot application, deploy the configured JAR to the configured server, restart the service, verify logs and status, and report the deployment outcome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broad deployment actions on a live server using a root SSH account. <br>
Mitigation: Require a final confirmation that shows the host, account, artifact path, and service name, and use a limited deployment account instead of root. <br>
Risk: The documented SSH commands disable host-key checking. <br>
Mitigation: Verify and pin the SSH host key before deployment instead of bypassing host-key checks. <br>
Risk: A deployment may replace and restart the configured service from the fixed local JAR path. <br>
Mitigation: Confirm the artifact path and intended service before execution, keep a timestamped backup, check logs after restart, and use the rollback procedure if verification fails. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell and shell command blocks plus deployment status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a fixed service, host, account, paths, and JAR name from the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
