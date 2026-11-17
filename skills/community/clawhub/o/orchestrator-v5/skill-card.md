## Description:

AI Orchestrator V5 routes user requests to specialist agents, scores selection confidence, and coordinates direct, sequential, parallel, review, or hybrid workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select appropriate specialist agents, plan multi-agent workflows, and introduce checkpoints for complex software, product, research, and operations tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route a sensitive or high-impact request to an unsuitable specialist.

Mitigation: Review selected agents, confidence scores, and fallback choices before acting on recommendations.

Risk: Checkpoint or session-memory workflows may retain private task context.

Mitigation: Avoid or clear checkpoints for confidential work unless the surrounding agent environment has approved retention controls.

## Reference(s):

- [Full Agent Catalog](references/catalog.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/orchestrator-v5)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with routing tables, execution plans, checkpoints, and phase summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; recommendations should be reviewed before sensitive or high-impact work.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
