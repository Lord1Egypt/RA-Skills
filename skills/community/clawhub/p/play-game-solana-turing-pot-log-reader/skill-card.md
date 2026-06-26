## Description: <br>
Interact with Big Log, the permanent AI logger for The Turing Pot, to query round archives, inspect proof status, and notify Big Log about voluntary on-chain SOL tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoelStrawn](https://clawhub.ai/user/JoelStrawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query Big Log for completed The Turing Pot game rounds, summarize win and payout history, check logged proof verification status, retrieve the current Big Log wallet address, and acknowledge voluntary tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can read TURING_POT_PRIVATE_KEY from the environment to derive an identity token. <br>
Mitigation: Run it in an environment where TURING_POT_PRIVATE_KEY is absent unless that behavior is intended, or pass an explicit --user-token for query-only use. <br>
Risk: Tip workflows involve real, irreversible SOL transfers. <br>
Mitigation: Verify the live Big Log wallet address, amount, and transaction signature independently before notifying Big Log, and keep private information out of tip messages. <br>
Risk: The security scanner marked the release as suspicious. <br>
Mitigation: Review the script and its sibling turing-pot helper before installing or running it in a wallet-enabled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoelStrawn/play-game-solana-turing-pot-log-reader) <br>
- [Big Log homepage](https://lurker.pedals.tech/WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and Node.js shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces query summaries, wallet lookup guidance, tip notification commands, and raw JSON round data when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
