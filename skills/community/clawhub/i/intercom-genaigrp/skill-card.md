## Description: <br>
Routes explicit opt-in messages between OpenClaw sessions for internal bot-to-bot coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravikadam](https://clawhub.ai/user/ravikadam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to send transparent, explicitly addressed messages to another session with !target syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages can expose private information to an unintended session if the target key is wrong or the content includes secrets. <br>
Mitigation: Verify the target session key before sending and avoid secrets or private data unless the receiving session is trusted and intended to see it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ravikadam/intercom-genaigrp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Plain text instructions and routed message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Only acts on explicit !target messages; the optional helper formats sessionKey and message fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
