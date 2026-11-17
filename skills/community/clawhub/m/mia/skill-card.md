## Description:

MIA (Memory-Intelligent Assistant) helps OpenClaw reuse prior task experience through memory retrieval, plan generation, and feedback collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingyangqiao](https://clawhub.ai/user/jingyangqiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use MIA to retrieve similar prior task trajectories, generate execution plans with optional historical context, and collect answer feedback for new problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task history and feedback may be persisted locally in JSONL files.

Mitigation: Set MIA_MEMORY_FILE and MIA_FEEDBACK_FILE to protected paths, limit file permissions, and review or delete stored records regularly.

Risk: Planner API mode can send prompts, historical plans, and bearer credentials to a configured external endpoint.

Mitigation: Prefer local mode for sensitive work; use API mode only with trusted HTTPS endpoints and narrowly scoped API keys.

Risk: Planner output may reflect incorrect or unsuitable guidance from the configured model or historical reference plan.

Mitigation: Treat generated plans as proposals and review them before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingyangqiao/skills/mia)
- [Publisher profile](https://clawhub.ai/user/jingyangqiao)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands, configuration]

**Output Format:** [JSON command-line output with generated plan text, memory records, and feedback records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planner output is capped by the configured model request; memory and feedback modules persist JSONL records to configurable local files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
