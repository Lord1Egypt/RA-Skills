## Description:

Launch a token on Flap BNB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flapguy](https://clawhub.ai/user/flapguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and token launch operators use this skill to configure, validate, and launch Flap Tax Token V3 tokens on BNB Chain. It guides quote-token selection, metadata upload, tax parameters, optional vault setup, vanity salt finding, transaction construction, and transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide irreversible BNB Chain token-launch transactions.

Mitigation: Review the final transaction before signing, especially `to`, `chainId`, `quoteToken`, `quoteAmt`, `beneficiary`, `vaultFactory`, and `vaultData`.

Risk: Custom or unverified vault factories can route revenue through contracts the user has not independently trusted.

Mitigation: Prefer official vault factories; independently verify any custom factory address and its `vaultDataSchema()` before launch.

Risk: Running a fresh unpinned npm install during a token launch can introduce dependency risk.

Mitigation: Install dependencies from a pinned, trusted environment before constructing or signing launch transactions.

## Reference(s):

- [Flap Documentation](https://docs.flap.sh)
- [Quote Token API](https://flap.sh/api/launch/quote-tokens)
- [Flap Upload API](https://funcs.flap.sh/api/upload)
- [Preflight Checks](references/preflight.md)
- [Choosing a Quote Token](references/quote-tokens.md)
- [Vault Factory Setup](references/vault-factory.md)
- [Token Metadata Upload](references/meta-upload.md)
- [Tax Token Parameters](references/tax-params.md)
- [Finding the Vanity Salt](references/salt-finding.md)
- [Construct the EVM Transaction](references/construct-tx.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code blocks, shell commands, transaction fields, and final token launch links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EVM transaction envelope fields (`to`, `value`, `data`) and may guide metadata upload or transaction broadcast when prerequisites are met.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
