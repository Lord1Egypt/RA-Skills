## Description: <br>
Accept payments on websites with moneydevkit by adding checkout, paywall, product, customer, and order flows to Next.js or Replit apps over Bitcoin Lightning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satbot-mdk](https://clawhub.ai/user/satbot-mdk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add payment collection to web apps, including fixed-price checkouts, pay-what-you-want flows, products, customer capture, and order tracking for Next.js or Replit deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet seed phrase or API token exposure can compromise payment funds or account access. <br>
Mitigation: Store MDK_MNEMONIC and MDK_ACCESS_TOKEN in environment variables or a secrets manager, never paste them into chat, logs, or git, test with non-production credentials first, and rotate compromised tokens. <br>
Risk: Authenticated moneydevkit MCP tools can manage apps, products, customers, orders, and API keys. <br>
Mitigation: Require explicit confirmation before changes, deletions, payment-account updates, or key rotation, and prefer separate limited-scope production apps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satbot-mdk/moneydevkit) <br>
- [Moneydevkit documentation](https://docs.moneydevkit.com) <br>
- [Moneydevkit MCP server](https://mcp.moneydevkit.com) <br>
- [moneydevkit on npm](https://www.npmjs.com/org/moneydevkit) <br>
- [Next.js Integration](references/nextjs.md) <br>
- [Replit Integration (Express + Vite)](references/replit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, shell command, and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MDK_ACCESS_TOKEN, MDK_MNEMONIC, and npx; mcporter is optional. Guidance may involve the moneydevkit MCP server and documentation endpoints.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
