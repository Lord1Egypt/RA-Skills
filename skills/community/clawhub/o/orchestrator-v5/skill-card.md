## Description: <br>
AI Orchestrator V5 routes user requests to specialist agents and coordinates multi-agent workflows using confidence scoring, fallback chains, checkpoints, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify broad work requests, select suitable specialist agents, and coordinate direct, sequential, parallel, review, or hybrid workflows. It is intended for multi-agent planning, routing, checkpointing, and validation rather than executing hidden code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad delegation can route sensitive, regulated, payment, crypto, legal, healthcare, or security work to specialist agents without enough user review. <br>
Mitigation: Require explicit user approval before delegating sensitive tasks or work in regulated domains. <br>
Risk: Generated routing plans or specialist recommendations may be incorrect or misleading. <br>
Mitigation: Review proposed agent selections, fallback chains, and execution plans before acting on them. <br>
Risk: Checkpointing can preserve private context if sensitive information is included in the session. <br>
Mitigation: Avoid saving sensitive context in checkpoints and review checkpoint contents before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/orchestrator-v5) <br>
- [Full Agent Catalog](artifact/references/catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured routing tables, plans, checkpoints, and validation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose specialist-agent delegation, fallback chains, human approval checkpoints, and recovery checkpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
