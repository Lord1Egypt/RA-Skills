## Description:

Analyzes Binance Smart Chain token contracts for rug-pull indicators such as honeypot behavior, mintability, tax settings, holder distribution, and open-source status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmx20150407-dotcom](https://clawhub.ai/user/cmx20150407-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto analysts use this skill to check a BSC token address and receive a quick risk level, score, and metric breakdown for further due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token addresses checked with the skill are sent to GoPlus Labs, which may reveal which contracts are being investigated and when.

Mitigation: Avoid submitting sensitive watchlists or investigation targets unless sharing those addresses with GoPlus Labs is acceptable.

Risk: The skill only supports Binance Smart Chain token checks.

Mitigation: Use it only for BSC contract addresses and rely on another chain-specific tool for other networks.

Risk: Runtime replies include Chinese messages, which may be unclear for some operators.

Mitigation: Review the output language before deployment and localize messages if the target users need another language.

## Reference(s):

- [GoPlus Labs Token Security API](https://api.gopluslabs.io/api/v1/token_security/56)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like text with a risk level, numeric score, and token-security metric breakdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BSC token contract address and sends that address to GoPlus Labs for analysis.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
