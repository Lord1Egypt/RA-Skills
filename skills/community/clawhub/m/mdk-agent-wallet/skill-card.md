## Description:

Self-custodial Bitcoin Lightning wallet for AI agents that lets an agent send and receive payments, check balances, generate invoices, and manage a wallet with BOLT11, BOLT12, LNURL, and lightning address support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satbot-mdk](https://clawhub.ai/user/satbot-mdk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate a self-custodial Bitcoin Lightning wallet for agent payments, invoice generation, balance checks, and payment history review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run mutable npm code for a mainnet wallet that can send real funds.

Mitigation: Use a pinned, reviewed package version and require explicit limits or human approval before agents send payments.

Risk: The wallet stores a BIP39 mnemonic on disk, and that mnemonic controls the wallet funds.

Mitigation: Start with an unfunded wallet, back up the mnemonic offline, and restrict permissions on ~/.mdk-wallet/.

Risk: The wallet runs a local daemon and connects outbound to MDK Lightning infrastructure.

Mitigation: Review the daemon and network behavior before deployment and monitor use in environments that handle funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satbot-mdk/skills/mdk-agent-wallet)
- [MoneyDevKit agent-wallet documentation](https://docs.moneydevkit.com/agent-wallet)
- [@moneydevkit/agent-wallet npm package](https://www.npmjs.com/package/@moneydevkit/agent-wallet)
- [MoneyDevKit](https://moneydevkit.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npx; wallet command outputs are JSON.]

## Skill Version(s):

0.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
