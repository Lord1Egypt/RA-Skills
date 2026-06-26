## Description: <br>
Generate PPTs using services provided by PI (Presentation Intelligence). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmcbbkad](https://clawhub.ai/user/xmcbbkad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a topic, outline, prompt, or supported source document into a generated PowerPoint presentation through the PI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded documents are sent to the configured PI service for processing. <br>
Mitigation: Use only trusted PI service endpoints, scope PI credentials, and avoid submitting confidential or sensitive documents unless that service use is approved. <br>
Risk: PI credentials are required in environment variables and could be exposed through shared shells, command histories, or logs. <br>
Mitigation: Provide PIPPT_APP_ID and PIPPT_APP_SECRET through a secure runtime environment and avoid pasting secrets into shared command lines or logs. <br>


## Reference(s): <br>
- [PI website](https://www.pi.inc/) <br>
- [ClawHub skill page](https://clawhub.ai/xmcbbkad/pi-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Console text with a generated PowerPoint URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated deck is produced by the PI service and can be viewed, edited, downloaded, and reused from the returned URL.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
