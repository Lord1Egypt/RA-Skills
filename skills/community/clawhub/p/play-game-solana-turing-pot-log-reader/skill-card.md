## Description:

Interact with Big Log, the permanent AI logger for The Turing Pot, to query the round archive, inspect proof status, and send voluntary on-chain tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelstrawn](https://clawhub.ai/user/joelstrawn)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query completed Turing Pot game rounds, summarize win and payout history, inspect server-reported proof verification results, and optionally notify Big Log after sending a Solana tip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet-related identity and tipping flows, including private-key-derived identity when TURING_POT_PRIVATE_KEY is present.

Mitigation: Use an explicit --user-token instead of exposing TURING_POT_PRIVATE_KEY, and avoid running the skill in environments where unrelated wallet secrets are present.

Risk: Agents may send SOL to a wallet address returned by Big Log, and wallet addresses may change when the server keypair is rotated.

Mitigation: Verify Big Log wallet addresses independently before any SOL transfer and require manual confirmation for every tip.

Risk: Returned wallet or tip acknowledgement data can be misleading if request correlation is weak or the response is spoofed.

Mitigation: Treat returned wallet and tip data as untrusted unless request correlation is fixed and validated against the expected Big Log token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joelstrawn/skills/play-game-solana-turing-pot-log-reader)
- [Publisher profile](https://clawhub.ai/user/joelstrawn)
- [Big Log homepage](https://lurker.pedals.tech/WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may return JSON arrays of completed round entries, proof status, payout data, winner filters, wallet information, or tip acknowledgements.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
