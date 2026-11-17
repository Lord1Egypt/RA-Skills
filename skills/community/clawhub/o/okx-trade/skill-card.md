## Description:

Setup, install, and use OKX Agent Trade Kit for AI-assisted OKX market data, portfolio, trading, and bot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chingchiu169](https://clawhub.ai/user/chingchiu169)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, and operate OKX Agent Trade Kit through OpenClaw or MCP-compatible clients. It supports market data lookup, account review, demo trading, live trading setup, and grid or DCA bot guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install mutable npm packages with npx or npm.

Mitigation: Verify the package source and version before installation, avoid global installation where possible, and review the package before use.

Risk: The skill supports live trading with exchange API credentials.

Mitigation: Start in demo or read-only mode, use a dedicated OKX subaccount, grant only required permissions, and keep withdrawals disabled.

Risk: The skill stores OKX credentials in ~/.okx/config.toml.

Mitigation: Protect the configuration file with restrictive permissions, such as a private directory and 0600 file mode.

## Reference(s):

- [OKX Agent Trade Kit documentation](https://www.okx.com/docs-v5/agent_en/)
- [OKX Agent Trade Kit GitHub repository](https://github.com/okx/agent-trade-kit)
- [MCP Client Setup](references/mcp-setup.md)
- [OKX Agent Trade Kit Tools Reference](references/tools-reference.md)
- [ClawHub skill page](https://clawhub.ai/chingchiu169/skills/okx-trade)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, TOML configuration snippets, tables, and natural-language examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading setup guidance and safety reminders before money-moving actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
