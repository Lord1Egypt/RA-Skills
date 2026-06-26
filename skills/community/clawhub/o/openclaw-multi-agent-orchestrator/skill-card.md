## Description: <br>
OpenClaw Multi Agent Orchestrator manages local AI agent registration, task dispatch, load balancing, performance monitoring, and inter-agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple local agents, route tasks to suitable agents, inspect agent status, and exchange inter-agent messages through local CLI scripts and JSON configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dispatched tasks and inter-agent messages may remain in local JSON state files. <br>
Mitigation: Avoid entering secrets, credentials, passwords, or sensitive business data into tasks or messages unless local retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwg2025/openclaw-multi-agent-orchestrator) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and local JSON configuration/state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent, task, message, and collaboration state is stored in local JSON files under the skill config directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
