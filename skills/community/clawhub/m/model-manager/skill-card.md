## Description: <br>
Fetches and displays OpenRouter AI models with pricing and context limits, and helps configure OpenClaw model routing for selected models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Notestone](https://clawhub.ai/user/Notestone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compare model pricing, plan cost-aware routing, and prepare configuration changes for selected models. It can also launch optional multi-agent execution workflows for task planning, coding, and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execution mode can spawn kept agent sessions that write workspace files and retain task data. <br>
Mitigation: Use list and plan for low-risk review; run --execute only in a dedicated workspace, avoid sensitive task text, and inspect generated files and kept sessions afterward. <br>
Risk: Routing and configuration changes can affect OpenClaw model defaults and fallback behavior. <br>
Mitigation: Review any generated routing or configuration changes before relying on them. <br>
Risk: The skill was flagged as suspicious because execution mode lacks tight cleanup controls. <br>
Mitigation: Treat execution mode as higher risk than read-only model listing and clean up retained sessions or local memory files after use. <br>


## Reference(s): <br>
- [OpenClaw Model Manager on ClawHub](https://clawhub.ai/Notestone/model-manager) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [Model Benchmarks Skill](https://clawhub.ai/skills/model-benchmarks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown tables, JSON configuration patches, shell command output, and generated workspace files when execution mode is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retain spawned agent sessions and local swarm memory when execution mode is used.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
