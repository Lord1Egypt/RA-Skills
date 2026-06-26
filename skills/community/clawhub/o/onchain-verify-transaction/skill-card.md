## Description: <br>
Verify an EVM transaction's calldata via Tenderly before signing. Confirms which tokens move, in what amounts, and to which addresses. Designed to be called by other skills as a pre-execution safety gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougalcantara](https://clawhub.ai/user/dougalcantara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before sending EVM transactions to verify calldata-derived token movements, recipient addresses, amounts, drains, and unexpected approvals against the stated intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification may be unavailable when the Tenderly access key is missing, Tenderly returns an error, rate limits apply, or the chainId is unsupported. <br>
Mitigation: Warn that verification did not complete, surface the specific condition, and require explicit user confirmation before proceeding. <br>
Risk: A transaction may move tokens to an unexpected recipient, substitute output tokens, return less than expected, drain excess input, or grant unexpected approvals. <br>
Mitigation: Compare Tenderly asset and balance changes with the stated intent, halt on discrepancies, and require explicit confirmation before execution. <br>
Risk: Cross-chain swaps are verified only on the source chain where the transaction is sent. <br>
Mitigation: Treat verification as covering the outbound leg only and communicate that scope before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dougalcantara/onchain-verify-transaction) <br>
- [Tenderly](https://tenderly.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and transaction-verification narration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TENDERLY_NODE_ACCESS_KEY and a supported EVM chainId.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
