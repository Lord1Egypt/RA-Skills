## Description:

PayRam MCP Integration helps agents connect to PayRam's MCP server to accept cryptocurrency payments, create payment links, generate payment, payout, and webhook code, and scaffold payment-enabled applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to connect to PayRam's MCP server, generate crypto payment and payout integrations, prepare webhooks, and scaffold payment-enabled applications for PayRam workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run external PayRam scripts and self-host setup commands without server-resolved provenance for this release.

Mitigation: Review the external PayRam scripts at a pinned version before execution and avoid production or wallet-bearing environments until that review is complete.

Risk: Headless setup can involve PayRam passwords, wallet mnemonics, destination addresses, chain selection, wallet creation, and contract deployment.

Mitigation: Use testnet funds first, keep passwords and mnemonics out of shell history and project files where possible, manually confirm destination addresses and chain choices, and treat any exposed mnemonic as compromised.

## Reference(s):

- [PayRam Architecture & Security Model](references/architecture.md)
- [PayRam Headless Agent Skill](references/headless-setup.md)
- [PayRam Website](https://payram.com)
- [PayRam MCP Integration Documentation](https://docs.payram.com/mcp-integration)
- [PayRam MCP Server GitHub Repository](https://github.com/PayRam/payram-helper-mcp-server)
- [PayRam Headless Agent Guide](https://github.com/PayRam/payram-scripts/blob/main/docs/PAYRAM_HEADLESS_AGENT.md)
- [PayRam MCP Server](https://mcp.payram.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment integration snippets, app scaffolding instructions, setup checklists, and operational guidance for PayRam MCP workflows.]

## Skill Version(s):

1.4.2 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
