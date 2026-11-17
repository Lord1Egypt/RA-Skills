## Description:

Classifies OpenClaw tasks by complexity and routes them to cost-aware model tiers with progressive escalation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsgoecke](https://clawhub.ai/user/jsgoecke)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to classify user requests and choose model tiers that balance cost, quality, and task complexity before delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages delegating user tasks to external model providers, which can expose private documents, code, calendar data, logs, secrets, or regulated data.

Mitigation: Use explicit provider allowlists, require user confirmation before external delegation, and redact secrets or sensitive content before routing.

Risk: Model prices and availability can change, making routing recommendations stale.

Mitigation: Review current provider pricing and availability before relying on cost-sensitive routing decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jsgoecke/skills/openclaw-model-router)
- [OpenRouter Free Models](https://openrouter.ai/collections/free-models)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with routing tables and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model tier recommendations, optimization modes, progressive escalation steps, and provider pricing notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
