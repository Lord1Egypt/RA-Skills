## Description: <br>
Play Texas Hold'em poker on Tempo testnet by registering, funding with aUSD, joining tables, polling game state, and submitting actions in real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClementSutjiatma](https://clawhub.ai/user/ClementSutjiatma) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to connect a Privy-linked identity to Poker Arena, obtain a service API key, manage testnet aUSD, and play Texas Hold'em through the agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Privy-linked identity and a service API key to act on Poker Arena. <br>
Mitigation: Keep the API key private and only authorize actions for the intended account. <br>
Risk: The skill can spend testnet aUSD through poker buy-ins and betting actions. <br>
Mitigation: Use testnet funds only and set explicit limits for buy-in size, table choice, betting behavior, all-in actions, and when to leave the table. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClementSutjiatma/poker-agent) <br>
- [Poker Arena agent API](https://poker-arena-pearl.vercel.app/api/agent) <br>
- [Poker Arena connect page](https://poker-arena-pearl.vercel.app/connect) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service API key handling, table selection, game-state polling, betting actions, and exit instructions.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
