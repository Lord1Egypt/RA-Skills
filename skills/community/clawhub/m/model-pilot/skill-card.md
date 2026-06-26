## Description: <br>
Model Pilot helps agents match task complexity to an appropriately priced model and fetch current pricing when users ask about model costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide whether a task needs a high-capability model or can be handled by a cheaper option. It supports quick model-cost checks, live pricing comparisons, and quality tradeoff guidance before expensive work begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend a cheaper model that reduces output quality for tasks where accuracy or reasoning depth matters. <br>
Mitigation: Review the stated quality tradeoff before changing models, and keep high-risk or complex tasks on the strongest available model. <br>
Risk: Model prices can change after the skill's bundled reference material was published. <br>
Mitigation: Use the skill's live pricing lookup posture and verify current prices with provider documentation before relying on cost estimates. <br>
Risk: The optional full-suite install command installs additional skills beyond Model Pilot. <br>
Mitigation: Review any multi-skill install command before execution and install only the skills needed for the current environment. <br>


## Reference(s): <br>
- [Model Pilot ClawHub Page](https://clawhub.ai/tommot2/model-pilot) <br>
- [Model Pilot Homepage](https://clawhub.ai/skills/model-pilot) <br>
- [Z.ai Pricing](https://z.ai/pricing) <br>
- [Model Database - Pricing, Benchmarks & Capability Tiers](references/model-database.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands and cost-estimation formulas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live pricing lookups when costs are requested; recommends model switches but does not perform them automatically.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
