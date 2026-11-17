## Description:

Play a 5-letter Wordle game on the Monad blockchain using $WORDLE tokens. Start games, submit guesses, and retrieve game state via HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husseinrasti](https://clawhub.ai/user/husseinrasti)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to have an agent play a paid Wordle-style game on Monad Mainnet, including wallet setup guidance, token purchase and approval flow, game start, guesses, game state checks, and leaderboard retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through real token purchases, approvals, and game payments on Monad Mainnet.

Mitigation: Use a dedicated low-balance wallet, manually confirm each transaction, approve only the minimum WORDLE amount needed, and revoke allowances after play.

Risk: Wallet private keys may be exposed if a primary wallet or long-lived key is provided to an agent runtime.

Mitigation: Never use a primary wallet private key; use an isolated game wallet with limited funds and rotate or discard credentials after use.

Risk: Blockchain transactions are irreversible and replay protection depends on the external game service validating transaction hashes.

Mitigation: Verify transaction details before submission and rely only on the documented game API responses when starting or resuming sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/husseinrasti/skills/monad-wordle-game)
- [Publisher profile](https://clawhub.ai/user/husseinrasti)
- [Wordle game API](https://wordle.nadnation.xyz)
- [WordleGame ABI](https://github.com/husseinrasti/monad-wordle/blob/main/contract/abi.json)
- [nad.fun ABI documentation](https://nad.fun/abi.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline TypeScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for blockchain transactions, HTTP API calls, gameplay decisions, and error handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
