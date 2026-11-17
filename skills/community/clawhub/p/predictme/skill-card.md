## Description:

Trade 10-second BTC, ETH, and SOL crypto prediction markets on PredictMe using TEST or BONUS balances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howardpen9](https://clawhub.ai/user/howardpen9)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to register with PredictMe, retrieve market odds, place TEST or BONUS balance bets, manage credentials and nonces, and review bet history for trading performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to register with PredictMe and store a bearer API key.

Mitigation: Store credentials in a keychain or a locked-down local file, exclude credential files from version control, and rotate or revoke the key if it is exposed.

Risk: The skill can guide repeated TEST or BONUS balance bets without a consistently enforced approval gate.

Mitigation: Require explicit human approval before each bet until intentionally disabled, set conservative max-bet percentages, and enforce stop-loss and profit-target limits.

Risk: PredictMe agent profile, leaderboard, and trade commentary activity may be public.

Mitigation: Avoid sensitive personal or proprietary information in agent names, profile descriptions, and generated trade commentary.

## Reference(s):

- [PredictMe ClawHub Skill Page](https://clawhub.ai/howardpen9/skills/predictme)
- [PredictMe Agent Trading Guide](https://app.predictme.me/skill.md)
- [PredictMe Agent API Spec](https://app.predictme.me/agents.json)
- [PredictMe Agent Discovery Card](https://app.predictme.me/agent-card.json)
- [PredictMe Agents Page](https://app.predictme.me/agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, JSON configuration snippets, and shell or code-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to call external PredictMe API endpoints, store bearer credentials, maintain monotonically increasing bet nonces, and generate public trade commentary.]

## Skill Version(s):

1.2.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
