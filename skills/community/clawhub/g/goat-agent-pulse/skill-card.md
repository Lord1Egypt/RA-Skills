## Description:

Agent Pulse provides a standardized interruptibility and load-status check with fixed trigger words and fixed output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevengaojn2010](https://clawhub.ai/user/stevengaojn2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and orchestration systems use Agent Pulse to expose an agent's availability, interruptibility, and new-task acceptance state from visible low-cost runtime signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Natural-language questions about whether the agent is busy or available may trigger the fixed pulse card unexpectedly.

Mitigation: Use explicit `/pulse` or `Agent Pulse` triggers when predictable behavior is required, and document accepted trigger phrases for users.

Risk: Availability status can be uncertain when visible runtime signals are weak or conflicting.

Mitigation: Return `unknown` with cautious task acceptance, rely on low-cost visible signals, and avoid claiming hidden internal certainty.

## Reference(s):

- [Agent Pulse README](README.md)
- [Agent Pulse Rules](references/rules.md)
- [OpenClaw Signal Mapping](references/openclaw-signals.md)
- [Deployment Defaults](references/deployment-defaults.md)
- [ClawHub Skill Page](https://clawhub.ai/stevengaojn2010/skills/goat-agent-pulse)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Fixed plain-text pulse card, with optional JSON from the bundled evaluator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default pulse card contains status, interruptibility, acceptNewTask, and reason fields.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
