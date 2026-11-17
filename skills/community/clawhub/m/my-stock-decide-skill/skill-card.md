## Description:

Provides stock trading decision support when a user supplies portfolio holdings and explicitly asks for trade decisions, combining live macroeconomic checks with per-ticker analysis and position-sizing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for decision-support analysis of U.S. stock portfolios when they provide holdings and request trade decisions. The skill produces macro scoring, ticker-level buy/sell/hold recommendations, order type and target price guidance, and final portfolio allocation targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive portfolio screenshots or holdings data.

Mitigation: Only provide portfolio screenshots or holdings data that are acceptable to share with the agent, and remove account numbers, names, and other identifiers where possible.

Risk: The output may be mistaken for automatic trade execution or regulated personalized financial advice.

Mitigation: Treat the output as decision support that requires user review before any trading action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-decide-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macro score summaries, per-ticker trade actions, sentiment, order type, target price, rationale, and projected T1/T2/T3 allocation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
