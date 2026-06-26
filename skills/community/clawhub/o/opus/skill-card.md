## Description: <br>
Routes agent tasks across Claude Haiku, Sonnet, and Opus tiers so simple requests use cheaper models and complex work escalates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VictorKing2005](https://clawhub.ai/user/VictorKing2005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to set model-routing guidance for Claude-only agent setups, starting with Haiku for simple work and escalating to Sonnet or Opus for higher-complexity tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad escalation rules can increase use of higher-cost Claude tiers and send more task context to those models. <br>
Mitigation: Review the routing thresholds before installation and tune or disable escalation for cost-sensitive or sensitive-context workflows. <br>
Risk: The package name "opus" can be confused with a model-specific skill even though the artifact provides general model-routing guidance. <br>
Mitigation: Confirm the publisher and skill page match the intended smart-model-switching package before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/VictorKing2005/opus) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; does not execute tools or require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
