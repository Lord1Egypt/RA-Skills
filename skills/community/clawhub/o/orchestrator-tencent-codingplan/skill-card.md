## Description: <br>
Task orchestration framework for Tencent Coding Plan that routes parallel or decomposed work to Tencent-hosted models and can spawn sub-agents with selected workspace context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drifting-snow](https://clawhub.ai/user/drifting-snow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when to delegate work to Tencent Coding Plan sub-agents, route tasks to suitable models, and aggregate results for coding, writing, search, reasoning, or large-file analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace file contents, user messages, and task prompts may be sent to the listed Tencent endpoint when included in delegated task context. <br>
Mitigation: Use explicit invocation and per-task confirmation, and avoid repositories containing secrets, credentials, customer data, or private business material unless file inclusion is tightly controlled. <br>
Risk: Broad orchestration triggers can spawn sub-agents and increase external data exposure or token cost. <br>
Mitigation: Confirm before spawning multiple sub-agents, sending files, or handling tasks that can be completed directly in the main session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drifting-snow/orchestrator-tencent-codingplan) <br>
- [Publisher profile](https://clawhub.ai/user/drifting-snow) <br>
- [Tencent Coding Plan API endpoint](https://api.lkeap.cloud.tencent.com/coding/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with task plans, model-routing guidance, and generated implementation content when delegated agents are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aggregated sub-agent results and recommendations for limiting file transfer and token use.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
