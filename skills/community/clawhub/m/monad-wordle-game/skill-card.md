## Description: <br>
Play a 5-letter Wordle game on the Monad blockchain using $WORDLE tokens. Start games, submit guesses, and retrieve game state via HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husseinrasti](https://clawhub.ai/user/husseinrasti) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent play an on-chain Wordle game on Monad Mainnet, including wallet setup, token purchase guidance, game payment, guess submission, and game-state retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Monad Mainnet token purchases, token approvals, and paid game transactions. <br>
Mitigation: Use a dedicated wallet with limited MON and WORDLE, require manual approval for every buy, approval, and play transaction, and revoke or limit allowances after playing. <br>
Risk: The security review flags insufficient built-in safeguards around wallet authority and token spending. <br>
Mitigation: Verify the token address, game contract, ABI, nad.fun flow, and API endpoint before use, and install only when intentional mainnet transaction signing is acceptable. <br>


## Reference(s): <br>
- [Monad Wordle ClawHub listing](https://clawhub.ai/husseinrasti/monad-wordle-game) <br>
- [WordleGame contract ABI](https://github.com/husseinrasti/monad-wordle/blob/main/contract/abi.json) <br>
- [nad.fun ABI documentation](https://nad.fun/abi.md) <br>
- [Monad Wordle API](https://wordle.nadnation.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Monad Mainnet contract addresses, wallet setup guidance, payment flow, API endpoints, and gameplay strategy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
