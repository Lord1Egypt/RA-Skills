## Description:

Multi-model consensus for AI agents that combines predictions from multiple LLMs, models, or sources into a mathematically optimal consensus weighted by historical accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to combine predictions from multiple models, agents, or human sources, weight contributors by historical accuracy, and surface disagreement before acting on a consensus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prediction inputs, model identifiers, confidences, and historical accuracy values to the OraClaw service.

Mitigation: Use it only when that data sharing is acceptable, and avoid confidential forecasts unless approved for the service.

Risk: The skill requires an ORACLAW_API_KEY and paid usage after any available free tier.

Mitigation: Confirm API key handling, pricing, and billing expectations before installation or automated use.

Risk: High model disagreement can make the consensus less reliable.

Mitigation: Flag high entropy results to the user and require review before acting on the consensus.

## Reference(s):

- [Oraclaw Ensemble ClawHub listing](https://clawhub.ai/whatsonyourmind/skills/oraclaw-ensemble)
- [OraClaw Ensemble homepage](https://oraclaw.dev/ensemble)
- [Publisher profile](https://clawhub.ai/user/whatsonyourmind)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown guidance with JSON-shaped prediction inputs and structured consensus results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces consensus prediction guidance, per-model weights, entropy-based disagreement notes, and individual contribution summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
