## Description:

Guides agents through reading the Kolect Sentiment Feed on Base, checking freshness and pending state, and preparing on-chain sentiment update requests.

This skill is for research and development only.

## Publisher:

[kolect-info](https://clawhub.ai/user/kolect-info)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to integrate Kolect's on-chain sentiment feed into analysis, dashboards, trading workflows, or DeFi logic while checking freshness before requesting updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update examples involve live wallet signing and can expose a private key if copied directly.

Mitigation: Use a wallet, hardware signer, external signer, or minimally funded test wallet, and never paste or hardcode a real private key.

Risk: requestUpdate is a state-changing transaction that can spend gas and may require a request fee.

Mitigation: Require explicit user confirmation and verify chain, contract address, symbol, time window, gas, fee, freshness, and pending state before sending a transaction.

Risk: Sentiment freshness, pending requests, supported symbols, time windows, fees, and update intervals are dynamic on-chain state.

Mitigation: Query the contract immediately before acting and present timestamps, freshness, pending state, and BPS validation results to the user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kolect-info/skills/kolect-sentiment)
- [Kolect Website](https://kolect.info)
- [Kolect Sentiment Feed Contract on Base](https://base.blockscout.com/address/0x6783ab3c181976e8c960c43d711aaf4da79a4e4b)
- [Kolect X Profile](https://x.com/kolect_info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JavaScript examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Base contract details, ABI snippets, BPS validation rules, freshness checks, pending-state checks, and transaction-safety guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact contract section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
