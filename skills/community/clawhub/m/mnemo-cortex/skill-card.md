## Description: <br>
Installs and wires Mnemo Cortex, a local-first persistent memory system, into OpenClaw and other MCP-capable agents for cross-session recall, decision history, or multi-agent shared memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guymanndude](https://clawhub.ai/user/guymanndude) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install or connect a local Mnemo Cortex memory server so supported MCP-capable hosts can save, recall, search, and share memories across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain secrets, regulated data, or sensitive project details beyond a single session. <br>
Mitigation: Avoid saving secrets or regulated data, and learn how to inspect or delete stored memories before using the skill on sensitive projects. <br>
Risk: Shared or mismatched agent IDs can expose or hide memories across agents. <br>
Mitigation: Confirm which agent IDs can share memory and enable cross-agent sharing only when intended. <br>
Risk: The setup flow asks users to install and run software from the referenced repository. <br>
Mitigation: Review the referenced repository before running install commands and verify the local Mnemo Cortex server health after setup. <br>


## Reference(s): <br>
- [Mnemo Cortex project](https://github.com/GuyMannDude/mnemo-cortex) <br>
- [Brain repo template](https://github.com/GuyMannDude/mnemo-plan) <br>
- [THE-LANE-PROTOCOL.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/THE-LANE-PROTOCOL.md) <br>
- [SESSION-GUIDE.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/SESSION-GUIDE.md) <br>
- [MONITORING.md](https://github.com/GuyMannDude/mnemo-cortex/blob/master/MONITORING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and host-specific configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides install verification and MCP host integration; does not directly execute commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
