## Description:

Recommend an available OpenClaw model and thinking level for a task. Choose from the configured subscription models or ask for GPT only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to choose a model and thinking level for the current task from their configured subscription models. It helps them verify model and tool availability before deciding whether to switch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recommended model or thinking level may not be available through the current OpenClaw session, provider account, or adapter.

Mitigation: Check the session's model picker and available thinking levels before applying a recommendation; preserve the user's explicit model and provider choices.

## Reference(s):

- [OpenClaw subscription guide](artifact/references/openclaw-subscriptions.md)
- [GPT-only guide](artifact/references/gpt-only.md)
- [GPT-6.2 routing refresh (17 November 2026)](artifact/references/gpt62-20261117.md)
- [Model routing evidence (6 November 2026)](artifact/references/benchmarks-20261106.md)
- [ClawHub skill page](https://clawhub.ai/theangrypit/skills/model-capability-router)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Short text recommendation with a model ID, thinking level, and task-specific reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A recommendation only; the user decides whether to switch models.]

## Skill Version(s):

1.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
