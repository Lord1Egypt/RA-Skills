## Description: <br>
M-flow Memory gives OpenClaw agents persistent long-term memory by storing conversations as structured knowledge graphs and retrieving relevant context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowelement-alexunbridled](https://clawhub.ai/user/flowelement-alexunbridled) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when an agent needs to remember prior conversations, user preferences, decisions, facts, or plans across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores conversations automatically as long-term memory, which can capture sensitive, regulated, or unwanted information. <br>
Mitigation: Use it only when cross-session memory is intended, avoid storing secrets or regulated data, and use the provided deletion or pruning tools when memory should be removed. <br>
Risk: Setup requires an LLM API key and runs a persistent Docker service exposed on a local port. <br>
Mitigation: Use a dedicated limited-scope API key, restrict access to the Docker-exposed port, and review the OpenClaw MCP configuration change before relying on the service. <br>
Risk: Memory data persists in a Docker volume after restarts and may remain after teardown unless removal is explicitly requested. <br>
Mitigation: Review retention expectations before use and remove the Docker volume when stored memories should be deleted. <br>


## Reference(s): <br>
- [M-flow homepage](https://github.com/FlowElement-ai/m_flow) <br>
- [M-flow documentation](https://docs.m-flow.ai) <br>
- [M-flow LoCoMo benchmark](https://github.com/FlowElement-ai/mflow-benchmarks) <br>
- [ClawHub skill page](https://clawhub.ai/flowelement-alexunbridled/mflow-memory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker, an LLM API key, a persistent Docker volume, and OpenClaw MCP registration.] <br>

## Skill Version(s): <br>
0.3.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
