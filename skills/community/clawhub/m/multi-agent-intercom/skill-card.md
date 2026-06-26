## Description: <br>
Enables peer-to-peer cross-communication between isolated OpenClaw agents and resolves the limitation of `sessions_send` which cannot cross agent boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxue1985122219](https://clawhub.ai/user/zhangxue1985122219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running local OpenClaw multi-agent setups use this skill to generate an inter-agent communication SOP and send messages between isolated agents on the same system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inter-agent messages can persistently and automatically influence other local agents without clear sender verification or approval controls. <br>
Mitigation: Use only in trusted local multi-agent setups, limit which agents may send and receive, verify sender identity, and require human approval before high-impact actions. <br>
Risk: Messages may contain sensitive data that is propagated to other agents. <br>
Mitigation: Avoid sending secrets or sensitive data through intercom messages and review the generated SOP before adding it to AGENTS.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxue1985122219/multi-agent-intercom) <br>
- [README](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a manually pasted SOP during setup and status text when sending messages.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
