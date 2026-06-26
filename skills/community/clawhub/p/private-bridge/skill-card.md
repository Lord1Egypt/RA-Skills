## Description: <br>
Private Bridge connects an OpenClaw instance to a trusted relay over an outbound WebSocket so remote operators can send prompts, check status, trigger workflows, and restart the node without exposing inbound ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-czar](https://clawhub.ai/user/jason-czar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to control headless or server-deployed OpenClaw nodes through a relay connection when direct SSH, inbound ports, or messaging integrations are not appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay messages can cause the node to run prompts, trigger workflows, and restart the OpenClaw process. <br>
Mitigation: Install only on nodes intended for relay control, restrict callable workflows in the runtime, and disable the skill when remote control is not needed. <br>
Risk: Compromise or misuse of AUTH_TOKEN can allow unauthorized relay access. <br>
Mitigation: Protect AUTH_TOKEN as a secret, rotate it regularly, and use only trusted relay operators. <br>
Risk: Prompt content, response tokens, node_id, heartbeat details, and workflow completion status pass through the configured relay. <br>
Mitigation: Use wss:// relay URLs and avoid routing sensitive work through a relay unless its operator and data handling are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-czar/private-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/jason-czar) <br>
- [README](artifact/README.md) <br>
- [Skill security and privacy disclosure](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration examples, shell commands, and relay protocol details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RELAY_URL, NODE_ID, and AUTH_TOKEN configuration before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
