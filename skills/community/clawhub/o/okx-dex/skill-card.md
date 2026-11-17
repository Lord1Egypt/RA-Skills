## Description:

OKX DEX aggregator (v6). Get swap quotes, swap/approve tx data, tokens, and chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricky321u](https://clawhub.ai/user/ricky321u)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading automation agents use this skill to query OKX DEX aggregator v6 for supported chains, token lists, swap quotes, and approval or swap transaction payloads. Users should independently review transaction details before signing or broadcasting anything.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate financial transaction data and includes a script with a hardcoded wallet address.

Mitigation: Review or edit scripts/test_okx.sh before use, verify wallet address, token, amount, slippage, approval target, and decoded calldata, and require independent wallet confirmation before signing.

Risk: The skill requires OKX API credentials.

Mitigation: Use only OKX API credentials intended for this skill and avoid exposing broader account permissions than needed.

## Reference(s):

- [OKX DEX API Reference (v6)](https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference)
- [ClawHub Skill Page](https://clawhub.ai/ricky321u/skills/okx-dex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, curl, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OKX API credentials and local curl, jq, and python3 binaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
