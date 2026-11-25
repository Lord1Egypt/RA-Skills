## Description:

Screens a wallet, token, or counterparty for risk signals to support decisions before funds are sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assessing a payment or counterparty use this skill to obtain sanctions, token safety, wallet portfolio, or merchant trust signals before deciding whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes the mutable agentcash@latest package, whose contents may change between uses.

Mitigation: Pin the package version and review that exact release before running it.

Risk: Wallet addresses and request or payment metadata are sent to a third-party service without a stated privacy notice.

Mitigation: Verify that you trust the receiving service and are comfortable sharing the addresses and associated metadata before making a call.

## Reference(s):

- [Wallet Risk Triage on ClawHub](https://clawhub.ai/nutshell2000/skills/glyphcall-wallet-risk)
- [Glyphcall sanctions screening](https://api.glyphcall.com/sanctions/check?address=<addr>)
- [Glyphcall token verdict](https://api.glyphcall.com/token/verdict?token=<addr>)
- [Glyphcall wallet portfolio](https://api.glyphcall.com/wallet/portfolio?address=<addr>)
- [Glyphcall merchant trust](https://api.glyphcall.com/merchant/trust?name=<domain>)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain-language risk summary with returned screening signals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cover sanctions, token verdicts, wallet portfolios, or merchant trust. Report failed or unverifiable checks as unavailable rather than clean.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
