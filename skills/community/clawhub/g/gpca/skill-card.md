## Description:

Manage GPCA bank cards, USDT wallet, KYC verification, and automate shopping on Amazon/Taobao with browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lobclaw](https://clawhub.ai/user/lobclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage GPCA card, wallet, KYC, and shopping workflows. It can check balances, guide funding and card operations, and assist checkout flows with explicit confirmation gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can install and run unpinned remote MCP server code and npm dependencies.

Mitigation: Review the referenced MCP server and dependency tree before setup; use a pinned, reviewed revision before enabling automatic installation.

Risk: Email verification automation can expose inbox contents and one-time authentication codes.

Mitigation: Prefer manual code entry, limit browser access to GPCA verification messages only, and require first-use disclosure before opening an inbox.

Risk: Payment automation can expose card details or submit transactions on untrusted merchant domains.

Mitigation: Retrieve card details only at the payment step, mask card data in conversation, verify the domain immediately before filling payment fields, and require explicit confirmation before purchase submission.

Risk: Financial transfers and checkout submissions can cause irreversible or duplicate charges if retried automatically.

Mitigation: Require explicit user confirmation for transfers and purchases, and do not auto-retry ambiguous transfer or payment submissions.

## Reference(s):

- [GPCA Skill Homepage](https://github.com/gpcaclaw/gpca-skill)
- [GPCA MCP Server](https://github.com/gpcaclaw/gpca-mcp-server.git)
- [Card Manager - Detailed Workflows](references/card-manager.md)
- [Shopping Assistant - Detailed Workflows](references/shopping-assistant.md)
- [Shopping Flows & Site-Specific Tips](references/shopping-flows.md)
- [GPCA MCP Tools Reference](references/api-reference.md)
- [Security & Privacy Guidelines](references/security-notes.md)
- [Common User Flows](references/user-flows.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown guidance with inline shell commands and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle sensitive financial, identity, payment, and email verification workflows; user confirmations are part of the expected output flow.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
