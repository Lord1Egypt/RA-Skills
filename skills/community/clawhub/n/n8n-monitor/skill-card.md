## Description: <br>
Monitors n8n containers through Docker commands for status, health, recent logs, and CPU and memory usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Smitti7971](https://clawhub.ai/user/Smitti7971) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect n8n Docker container status, health, recent logs, and resource use during operational monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker visibility into the n8n container can expose recent logs that contain workflow payloads, URLs, tokens, or operational details. <br>
Mitigation: Install only where the agent is intended to inspect Docker state for n8n, and review returned logs before sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with simple tables and clear status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker command output summaries for n8n container status, logs, health, and resource usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
