## Description:

Assess whether to escalate models

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent orchestrators use this skill to decide whether a task's complexity, uncertainty, novelty, or stakes justify a higher-capability model. It guides them to investigate first and document the reason, scope, and success criteria for any escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to run in situations where escalation governance is not relevant.

Mitigation: Review trigger matches and invoke the skill only when model-selection or escalation decisions are in scope.

Risk: Security analysis coverage is partial because two local references could not be resolved.

Mitigation: Review the skill and confirm its referenced materials before relying on its guidance.

## Reference(s):

- [Skill project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-abstract-escalation-governance)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown guidance with checklists, tables, and escalation rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides decision guidance; no specific file output is defined.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
