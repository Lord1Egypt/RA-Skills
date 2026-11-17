## Description:

moneydevkit helps agents add Bitcoin Lightning payment flows to Next.js or Replit web apps, including fixed-price, pay-what-you-want, product, customer, and order workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satbot-mdk](https://clawhub.ai/user/satbot-mdk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add checkout, product, customer, and order payment flows to Next.js or Replit applications using MoneyDevKit credentials and MCP, CLI, or dashboard setup paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MDK_MNEMONIC is a wallet seed phrase; exposure can compromise payment funds.

Mitigation: Store MDK_MNEMONIC only in a secrets manager or environment variable, never commit or log it, and use testnet or signet credentials before mainnet.

Risk: The skill can guide agents to run npx setup and configure payment-account tooling.

Mitigation: Install only from trusted MoneyDevKit sources, review generated project changes, and pin or verify npm package versions before production use.

## Reference(s):

- [Next.js Integration](references/nextjs.md)
- [Replit Integration](references/replit.md)
- [MoneyDevKit Documentation](https://docs.moneydevkit.com)
- [MoneyDevKit MCP Server](https://mcp.moneydevkit.com)
- [MoneyDevKit npm Organization](https://www.npmjs.com/org/moneydevkit)
- [ClawHub Skill Page](https://clawhub.ai/satbot-mdk/skills/moneydevkit)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, bash, and environment-variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MDK_ACCESS_TOKEN and MDK_MNEMONIC; optional account-management steps can use mcporter.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
