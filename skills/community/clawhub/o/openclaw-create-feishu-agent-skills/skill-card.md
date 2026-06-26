## Description: <br>
Creates and wires a Feishu-only OpenClaw agent by guiding routing selection, updating OpenClaw bindings, restarting the gateway, and verifying the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaowen-0725](https://clawhub.ai/user/xiaowen-0725) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create a new Feishu-routed OpenClaw agent, update account or peer bindings, preserve existing routes, and verify the gateway configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app secrets can be passed through command arguments and included in command output summaries. <br>
Mitigation: Avoid sharing command output, prefer a safer secret source, and redact appSecret values from summaries before use. <br>
Risk: The skill makes persistent OpenClaw routing changes and restarts the gateway. <br>
Mitigation: Review the planned openclaw.json changes, keep the generated backup, and verify bindings after restart. <br>
Risk: Incorrect account or peer identifiers could route a Feishu group or account to the wrong agent. <br>
Mitigation: Confirm the routing mode, account ID, peer kind, and peer ID before applying changes; use the route conflict checks and binding verification output. <br>


## Reference(s): <br>
- [Routing Modes Reference](references/routing-modes.md) <br>
- [ClawHub Release Page](https://clawhub.ai/xiaowen-0725/openclaw-create-feishu-agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Feishu-only workflow; may update OpenClaw configuration and trigger gateway restart.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
