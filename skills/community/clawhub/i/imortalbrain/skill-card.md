## Description: <br>
Immortal Brain is an autonomous OpenClaw agent for task workflow management, local memory organization, heartbeat monitoring, and continuous learning through task connections and user profiling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovidiuproca](https://clawhub.ai/user/ovidiuproca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run an autonomous local task-management loop that ingests tasks, researches and plans work, reports progress, and maintains memory, identity, and user-profile files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can continue after user silence through a documented auto-approval timeout. <br>
Mitigation: Review and edit HEARTBEAT.md before enabling the skill, and disable silence-based auto-approval when explicit consent is required. <br>
Risk: The agent maintains broad local memory, profile, identity, and tool-context files that may contain sensitive information. <br>
Mitigation: Avoid storing secrets in TOOLS.md or memory files the skill scans, and review local files before enabling recurring heartbeat processing. <br>
Risk: Core memory optimization and identity update commands can modify persistent local memory and identity files. <br>
Mitigation: Back up MEMORY.md and IDENTITY.md before using optimization or identity update commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ovidiuproca/imortalbrain) <br>
- [README](artifact/README.md) <br>
- [Conceptual guide](artifact/references/conceptual_guide.md) <br>
- [Heartbeat information](artifact/references/heartbeat_info.md) <br>
- [Setup guide](artifact/references/setup_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command responses, Markdown reports, shell commands, and local Markdown/JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local OpenClaw workspace files such as memory, Creier, identity, and core memory documents.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
