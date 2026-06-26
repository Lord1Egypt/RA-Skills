## Description: <br>
Play chess on lawb.xyz/chess with on-chain wagers. Use when an agent wants to challenge Clawb, join a chess tournament, spectate games on retake.tv/clawb, or participate in lawb chess bounties. Covers wallet setup, game creation/joining, move protocol, wager escrow, and spectator integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wables411](https://clawhub.ai/user/wables411) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to connect an EVM wallet, create or join wagered chess games, validate and submit moves, interact with wager escrow contracts, and spectate or participate in Lawb Chess events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through wagered on-chain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, verify chain and contract details independently, approve only the exact wager amount, and manually confirm each wallet transaction. <br>
Risk: The skill can guide an agent to update live public game, chat, profile, and leaderboard state. <br>
Mitigation: Require explicit user approval for the chain, token, wager amount, opponent, move, and any public message or profile content before the agent writes state. <br>


## Reference(s): <br>
- [Lawb Chess](https://lawb.xyz/chess) <br>
- [Clawb Stream](https://retake.tv/clawb) <br>
- [Lawb Bounties](https://lawb.xyz) <br>
- [chess.js](https://github.com/jhlywa/chess.js) <br>
- [ClawHub Skill Page](https://clawhub.ai/wables411/lawbchess) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with JSON, JavaScript, Solidity, and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet, chain, token, Firebase, contract, move validation, chat, leaderboard, and spectator workflow guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
