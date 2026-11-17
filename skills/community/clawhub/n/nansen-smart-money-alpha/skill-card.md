## Description:

What tokens is smart money accumulating before they pump? Token screener with SM filter cross-referenced against netflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto market researchers use this skill to screen tokens for smart-money activity and compare screener results with net flows across a selected chain and timeframe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported paid API calls can spend funds from the configured wallet, and each call in a loop can incur a payment.

Mitigation: Review wallet authorization, payment policy, spending limits, and per-call costs before running research calls or loops.

Risk: A saved browser session or API key grants access according to its permissions, and cached authentication metadata does not establish that credentials are valid.

Mitigation: Select an explicit API key or saved session, check authentication status before research, and stop if authentication or renewal fails.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen CLI package on npm](https://www.npmjs.com/package/nansen-cli)
- [Nansen CLI project](https://github.com/nansen-ai/nansen-cli)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-smart-money-alpha)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Text summary of token screening and netflow findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include token symbols, prices, volume, market capitalization, liquidity, token age, net flows, and trader counts.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
