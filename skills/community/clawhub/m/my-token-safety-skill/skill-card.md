## Description: <br>
Analyzes Binance Smart Chain token contracts for risks such as honeypots, mintable supply, high taxes, ownership concentration, holder count, and open-source status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmx20150407-dotcom](https://clawhub.ai/user/cmx20150407-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to quickly screen BSC token contract addresses for common token-risk signals. It supports triage and due diligence workflows but should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried BSC contract addresses are sent to GoPlus Labs. <br>
Mitigation: Only submit token contract addresses that are acceptable to disclose to the external API provider. <br>
Risk: The generated score may be incomplete or unsuitable as investment advice. <br>
Mitigation: Use the result as one due-diligence signal and verify token risk independently before making financial decisions. <br>
Risk: The skill supports only Binance Smart Chain tokens. <br>
Mitigation: Use it only with BSC contract addresses and route other chains to chain-specific tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cmx20150407-dotcom/my-token-safety-skill) <br>
- [GoPlus Labs token security API endpoint](https://api.gopluslabs.io/api/v1/token_security/56) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style text response with a risk level, numeric score, and token-risk metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a BSC token contract address and only supports Binance Smart Chain chainId 56.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
