## Description: <br>
Sends internal company messages through a configured Jiuwu HTTP message gateway for one or more employee codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[05u](https://clawhub.ai/user/05u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operations staff, and agent operators use this skill to send internal notifications or reminders to one or more company contacts through the Jiuwu gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be sent to the wrong employee codes, especially when using comma-separated batch recipients. <br>
Mitigation: Review recipient codes and message text before each send; use smaller batches for sensitive notifications. <br>
Risk: The default gateway URL uses plain HTTP on an internal address. <br>
Mitigation: Set JIUWU_MESSAGE_GATEWAY_URL to the trusted environment endpoint and prefer HTTPS or a protected internal network. <br>
Risk: The skill transmits message content to the configured Jiuwu gateway. <br>
Mitigation: Install only when the publisher and gateway are trusted, and avoid sending sensitive content unless the gateway is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/05u/jiuwu-message) <br>
- [Publisher profile](https://clawhub.ai/user/05u) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; the send script returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JIUWU_MESSAGE_GATEWAY_URL for non-default gateway configuration; supports comma-separated batch recipient codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
