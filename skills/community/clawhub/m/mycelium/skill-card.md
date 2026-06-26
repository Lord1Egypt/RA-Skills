## Description: <br>
Agent Pheromone Network interface for querying shared execution paths and publishing verified task paths to a collective intelligence network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XieChengYuan](https://clawhub.ai/user/XieChengYuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs help with a complex task, wants to query prior successful execution paths, or wants to publish a reviewed path for later reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends task goals, handles, feedback, and approved path summaries to the Mycelium service. <br>
Mitigation: Use a dedicated API key, avoid secrets or proprietary data in goals and paths, and install only when this network sharing is acceptable. <br>
Risk: Publishing a path can disclose sensitive task details if the preview is not reviewed carefully. <br>
Mitigation: Review the publish preview before confirmation and keep the required explicit confirmation step for publish actions. <br>
Risk: Changing MYCELIUM_API_URL can redirect requests to another host. <br>
Mitigation: Set MYCELIUM_API_URL only when the destination host is trusted. <br>


## Reference(s): <br>
- [Mycelium Platform live dashboard](https://mycelium-platform.onrender.com) <br>
- [ClawHub skill page](https://clawhub.ai/XieChengYuan/mycelium) <br>
- [Publisher profile](https://clawhub.ai/user/XieChengYuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, httpx, MYCELIUM_API_KEY, and OPENCLAW_AGENT_ID for normal operation.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
