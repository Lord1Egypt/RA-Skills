## Description:

Agent-to-Agent USDC payments. Create wallets, send/receive payments, escrow between agents. Built for the USDC Hackathon on Moltbook.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[rojasjuniore](https://clawhub.ai/user/rojasjuniore)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent builders use Payclaw to configure Circle-backed testnet wallets, create payment requests, send USDC testnet payments, and coordinate local agent-to-agent escrow workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command execution and payment arguments may expose users to unintended wallet actions.

Mitigation: Use only testnet credentials, manually verify every destination and amount before sending, and harden command execution before any paid or production use.

Risk: Payment credentials are stored and passed through local CLI workflows.

Mitigation: Avoid real payment credentials until secret storage is improved; keep credentials scoped to testnet or disposable environments.

Risk: The escrow feature can be mistaken for locked or trustless escrow.

Mitigation: Treat escrow records as local bookkeeping only unless the implementation is changed to lock funds and verify releases or refunds.

## Reference(s):

- [Payclaw ClawHub Skill](https://clawhub.ai/rojasjuniore/skills/payclaw)
- [Payclaw homepage](https://github.com/rojasjuniore/payclaw)
- [Moltbook publisher page](https://moltbook.com/u/JuniorClaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output, local JSON configuration files, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local wallet configuration, transaction history, agent directory records, and escrow bookkeeping files for the Payclaw CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
