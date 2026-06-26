## Description: <br>
Switches the active OpenClaw LLM model through the Huddle01 GRU gateway and reports the current model when asked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OmGuptaIND](https://clawhub.ai/user/OmGuptaIND) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to switch or inspect the active model for a hudl provider backed by gru.huddle01.io while keeping active and default model settings aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw model settings and restarts OpenClaw. <br>
Mitigation: Run validation first, review the resolved model and before/after active/default values, and keep a config backup when rollback matters. <br>
Risk: Broad model aliases may select a model the user did not intend. <br>
Mitigation: State the resolved hudl model ID before switching and ask for clarification when the requested model is unclear or high impact. <br>
Risk: A fallback install source is not established by server-resolved provenance. <br>
Mitigation: Prefer the ClawHub install path unless the fallback source is independently trusted. <br>


## Reference(s): <br>
- [GRU Gateway Model Catalog](references/models.md) <br>
- [Huddle01 GRU Gateway](https://gru.huddle01.io) <br>
- [GRU Gateway Models API](https://gru.huddle01.io/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and configuration status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports before and after active/default model values and may restart OpenClaw after successful validation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
