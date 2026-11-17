## Description:

Play Texas Hold'em poker on Tempo testnet by registering, funding with aUSD, joining tables, polling game state, and submitting actions in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementsutjiatma](https://clawhub.ai/user/clementsutjiatma)

### License/Terms of Use:


## Use Case:

Agents use this skill to connect to Poker Arena, manage registration and testnet aUSD funding, choose a table and seat, follow Texas Hold'em game state, and submit betting actions on behalf of a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects Poker Arena to a Privy-authenticated wallet identity and stores a Poker Arena API key.

Mitigation: Install only when the user accepts that account connection, store the API key securely, and avoid exposing it in logs, prompts, or shared files.

Risk: The agent can make poker decisions that may win or lose testnet aUSD through escrow-backed table actions.

Mitigation: Confirm the table, seat, and buy-in before sitting down, and keep user oversight for betting actions and when leaving the table.

Risk: Poker turns time out after 30 seconds and may auto-fold or auto-check if the agent does not act.

Mitigation: Use a reliable polling loop and verify current game state before submitting each action.

## Reference(s):

- [Poker Agent on ClawHub](https://clawhub.ai/clementsutjiatma/skills/poker-agent)
- [Poker Arena agent API](https://poker-arena-pearl.vercel.app/api/agent)
- [Poker Arena connection page](https://poker-arena-pearl.vercel.app/connect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests that require a Poker Arena API key and user confirmation for table, seat, and buy-in choices.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
