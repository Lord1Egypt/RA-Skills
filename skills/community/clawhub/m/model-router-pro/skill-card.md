## Description: <br>
Routes substantive user requests to a model selected by a 12-dimension task scorer, then guides the agent to switch models before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route substantive OpenClaw requests to an available model based on task complexity, model capability scores, and relative cost. It is intended for workflows where automatic model selection and session-level model switching are desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic routing can switch models on most substantive requests and the optional AGENTS.md reinforcement can make that behavior persistent across future agent sessions. <br>
Mitigation: Install only when automatic routing is desired, keep higher-priority instructions in control, and avoid adding the broad AGENTS.md reinforcement unless persistent routing is acceptable. <br>
Risk: Generated or default model scores may not match a user's actual model availability, capability, or pricing. <br>
Mitigation: Run --setup knowingly, review the generated models.json, and adjust capability and cost scores before relying on routing decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bevanding/model-router-pro) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with CLI commands and JSON routing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Router results include a recommended model id, tier, and confidence; setup can generate a models.json configuration from available OpenClaw models.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
