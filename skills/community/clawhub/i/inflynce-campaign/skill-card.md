## Description: <br>
Create and launch Inflynce Boost campaigns to promote HTTPS links by paying USDC rewards to users on Base based on social influence scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inflynceprotocol](https://clawhub.ai/user/inflynceprotocol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to create paid Inflynce Boost campaigns for tweets, websites, Farcaster casts, and other HTTPS links. It can also guide setup for campaign fees, USDC budget approvals, and Base transaction prerequisites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create paid public marketing campaigns and broadcast Base transactions. <br>
Mitigation: Install only if this behavior is intended, review campaign details before execution, and prefer the web wallet flow when possible. <br>
Risk: Programmatic fee payment and top-up flows require a wallet private key and can move or approve real USDC. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing private keys on the command line, keep USDC approvals small, and revoke unused allowances after use. <br>
Risk: Incorrect recipient, token, or spender addresses could cause loss of funds or unintended approvals. <br>
Mitigation: Verify the Inflynce fee recipient, USDC contract, and boosts contract addresses against the Inflynce site or documentation before signing transactions. <br>


## Reference(s): <br>
- [Inflynce Campaign on ClawHub](https://clawhub.ai/inflynceprotocol/inflynce-campaign) <br>
- [Inflynce Boost](https://boost.inflynce.com) <br>
- [Inflynce GraphQL API endpoint](https://boost.inflynce.com/api/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference transaction hashes, campaign IDs, wallet addresses, Base network settings, and USDC amounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
