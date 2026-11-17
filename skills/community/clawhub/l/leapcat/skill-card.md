## Description:

Leapcat Skills let agents trade stocks, subscribe to IPOs, manage wallets, complete KYC, and access real-time market data on the Leapcat platform via the pinned Leapcat CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raymondxu813-finance](https://clawhub.ai/user/raymondxu813-finance)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill bundle to interact with Leapcat financial workflows, including market data, authentication, portfolio review, trading, IPO subscriptions, wallet operations, and KYC submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live financial actions such as trades, IPO subscriptions or cancellations, wallet withdrawals, KYC agreements, and KYC submissions can have irreversible account, asset, or identity-data consequences.

Mitigation: Require explicit user confirmation showing the final account, asset, quantity, price or amount, address, fees, and irreversible effects before running any sensitive command.

Risk: The workflows handle OTPs, trade passwords, local token files, and KYC documents.

Mitigation: Keep OTPs, passwords, token files, and identity documents out of logs and prompts, and only upload document paths explicitly provided by the user.

Risk: Sensitive operations depend on an npm CLI that is auto-downloaded at execution time.

Mitigation: Use the pinned leapcat@0.1.1 package, avoid elevated privileges, and prefer verified package installation or sandboxing before sensitive use.

## Reference(s):

- [Leapcat homepage](https://leapcat.ai)
- [Leapcat ClawHub skill page](https://clawhub.ai/raymondxu813-finance/skills/leapcat)
- [Leapcat npm package](https://www.npmjs.com/package/leapcat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the version-pinned npx leapcat@0.1.1 CLI and usually request JSON output for agent consumption.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
