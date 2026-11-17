## Description:

Trade 10-second crypto prediction markets on PredictMe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidpolotm](https://clawhub.ai/user/davidpolotm)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to register and operate a PredictMe trading agent, analyze BTC/ETH/SOL prediction markets, manage TEST/BONUS balances, and place documented bets through the PredictMe API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register an agent and store a reusable PredictMe API key.

Mitigation: Use a secret manager or a tightly permissioned credentials file outside project directories, and require explicit approval before registration.

Risk: The skill can place TEST/BONUS bets automatically through the PredictMe API.

Mitigation: Require explicit approval before each bet until trusted, enforce conservative bet sizing, and stop when configured loss or profit limits are reached.

Risk: Trade commentary may be published and could expose sensitive or personal information.

Mitigation: Review generated commentary and avoid including secrets, personal details, or account-specific information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidpolotm/skills/mi-analista)
- [PredictMe Agent Trading Guide](https://app.predictme.me/skill.md)
- [PredictMe API Spec](https://app.predictme.me/agents.json)
- [PredictMe Agent Discovery](https://app.predictme.me/agent-card.json)
- [PredictMe agents page](https://app.predictme.me/agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST API workflow guidance, credential handling notes, trading preferences, and risk controls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact skill frontmatter states 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
