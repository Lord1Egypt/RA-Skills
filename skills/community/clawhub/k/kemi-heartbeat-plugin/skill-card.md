## Description: <br>
Injects a visual heartbeat animation and real-time status indicator into the OpenClaw Web UI to show Kemi's active state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang77160](https://clawhub.ai/user/yang77160) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to add a visible heartbeat effect and status indicator to the Web UI so Kemi's online, thinking, or busy state is easier to see. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npx install step may fetch and execute package code outside the provided skill artifact. <br>
Mitigation: Review the install command and package source before running it. <br>
Risk: The skill intentionally changes visible OpenClaw Web UI behavior. <br>
Mitigation: Install it only when the heartbeat animation and status indicator are desired, and verify the UI change in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang77160/kemi-heartbeat-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/yang77160) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and inline shell command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces UI injection guidance for an agent; no credentials, data access, or network calls are indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
