## Description: <br>
Bidirectional bridge between Pilot Protocol and Slack channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect Pilot agents with Slack workspaces for outbound notifications and inbound Slack event handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Slack command interface can expose daemon status or peer information to chat participants. <br>
Mitigation: Use the skill only in a trusted Slack workspace and restrict inbound events to approved channels and users. <br>
Risk: Slack webhook URLs can grant message-posting access if disclosed. <br>
Mitigation: Protect webhook URLs as secrets and rotate them if exposure is suspected. <br>
Risk: The always-on bridge depends on an external relay implementation. <br>
Mitigation: Inspect the relay implementation before running the bridge and avoid exposing sensitive daemon information by default. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-slack-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, a Slack webhook URL, and an HTTP relay service for inbound Slack events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
