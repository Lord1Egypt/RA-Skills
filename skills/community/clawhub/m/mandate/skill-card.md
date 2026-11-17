## Description:

Mandate guides agents to validate wallet transactions against spending policies, allowlists, approval workflows, prompt-injection checks, and audit trails before signing or broadcasting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Mandate to add pre-transaction policy validation, approval handling, and audit visibility to AI agents that can spend from wallets. It is especially relevant for wallet-enabled agents using OpenClaw, Claude Code, GOAT, AgentKit, ElizaOS, MCP, or direct CLI, REST, and SDK integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to consume mutable remote SKILL.md updates.

Mitigation: Disable or ignore the remote heartbeat unless updates are reviewed and approved through the normal release process.

Risk: Plugin and CLI installation examples do not pin exact package versions.

Mitigation: Review the plugin and CLI packages before installation and pin exact versions where possible.

Risk: The Mandate runtime key functions like a financial-policy credential.

Mitigation: Keep MANDATE_RUNTIME_KEY out of logs, screenshots, broad shell environments, and committed .env files.

Risk: Direct SDK or REST integrations without hooks depend on the agent to call validation before spending.

Mitigation: Prefer hook-based plugins when available and fail closed when validation is blocked or unreachable.

## Reference(s):

- [Mandate homepage](https://app.mandate.md)
- [Mandate API](https://app.mandate.md/api)
- [Mandate MCP server](https://mcp.mandate.md/mcp)
- [Claude Mandate plugin](https://github.com/SwiftAdviser/claude-mandate-plugin)
- [ClawHub skill page](https://clawhub.ai/swiftadviser/skills/mandate)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls]

**Output Format:** [Markdown with bash, JavaScript, JSON, REST examples, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI, REST, SDK, MCP, plugin, and fail-closed policy-check flows.]

## Skill Version(s):

1.3.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
