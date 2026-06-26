## Description: <br>
Provides OpenClaw agents with local, scene-aware, persistent structured memory for task deduplication and long-term workflow recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openmemoai](https://clawhub.ai/user/openmemoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let OpenClaw agents recall completed tasks, decisions, and successful workflows across sessions while reducing repeated work. It is best suited for coding, DevOps automation, research, and other multi-step agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent task memories may persist across sessions and influence future work. <br>
Mitigation: Review stored memories through the adapter inspector or storage controls, delete stale or incorrect memories, and treat recalled memories as context to verify before acting. <br>
Risk: Stored memories could include secrets, credentials, personal data, regulated data, or confidential customer details if users save them. <br>
Mitigation: Avoid writing sensitive data to memory and keep the default local adapter unless a remote endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openmemoai/openmemo-clawhub-skill) <br>
- [OpenMemo project](https://github.com/openmemoai/openmemo) <br>
- [OpenMemo OpenClaw adapter](https://github.com/openmemoai/openmemo-openclaw-adapter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text setup guidance and JSON tool responses from local memory recall, write, and task-check operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local OpenMemo adapter by default; remote endpoints require explicit trust and configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
