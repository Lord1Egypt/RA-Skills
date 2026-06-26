## Description: <br>
Assesses whether an agent should escalate to a higher-capability model after investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent orchestrators use this skill to decide when model escalation is justified, document the reason and scope, and return to a lower-cost model after the deeper reasoning task is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence model-escalation decisions in agent and orchestration workflows. <br>
Mitigation: Keep activation focused on escalation governance use cases and require documented justification before changing model capability. <br>
Risk: Version-specific model and effort-control guidance can become stale as provider behavior changes. <br>
Mitigation: Verify current model availability and effort-control behavior before relying on those operational notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-escalation-governance) <br>
- [Homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with tables and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory decision framework; no executable code or hidden access behavior was reported in the security evidence.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
