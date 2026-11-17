## Description:

Smart Scheduler classifies user requests by complexity and routes simple tasks directly while decomposing complex tasks for resource selection, execution, aggregation, and debate-style verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route user work between fast handling and deeper multi-step processing. It is intended for task triage, resource selection, result aggregation, and verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local service calls may send task content to localhost APIs during routing or verification.

Mitigation: Review and explicitly approve configured local endpoints before installation, and run the skill in an isolated environment where unexpected local services are not reachable.

Risk: The skill may persist truncated user prompt text and run statistics to a local stats file.

Mitigation: Avoid secrets and sensitive business data, disable or redirect stats collection, and purge local logs according to retention policy.

Risk: Dynamic routing and execution-related code can depend on unverified local skills, services, or generated code paths.

Mitigation: Require human approval before installing or executing routed dependencies, scan generated code and referenced skills, and keep sandboxing controls enabled.

## Reference(s):

- [Smart Scheduler on ClawHub](https://clawhub.ai/timo2026/skills/openclaw-smart-scheduler)
- [Publisher profile](https://clawhub.ai/user/timo2026)

## Skill Output:

**Output Type(s):** [Text, Guidance, Code]

**Output Format:** [TaskResult-style text response with routing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include complexity, selected skill, latency, subtasks, verification confidence, and status details.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; SKILL.md frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
