## Description: <br>
Intelligent cost-aware model routing that classifies task complexity and selects the optimal AI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsgoecke](https://clawhub.ai/user/jsgoecke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to classify tasks by complexity and choose cost-aware model tiers, routing simple work to cheaper models and complex or reasoning-heavy work to stronger models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing may send private prompts through a provider or model gateway the user does not trust. <br>
Mitigation: Define trusted providers in advance and require approval before routing sensitive work through premium or gateway models. <br>
Risk: Cost-aware routing can still escalate to premium models and increase spend. <br>
Mitigation: Set a maximum spend or preferred model tier and require approval before premium escalation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jsgoecke/openclaw-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only routing guidance; model pricing and availability should be checked before relying on a recommendation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
