## Description:

Connect OpenClaw to Proppely's official MCP and operate a property-management portfolio with scoped OAuth, audited tools, local-file migration, and human approval for protected actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shabsi7700](https://clawhub.ai/user/shabsi7700)

### License/Terms of Use:

MIT-0

## Use Case:

Property-management operators and supporting agents use this skill to connect OpenClaw to Proppely's remote MCP, inspect portfolio data, migrate local files, and prepare or execute governed rental, accounting, leasing, maintenance, document, tenant, owner, and team-access workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Codex install path depends on an unpinned third-party marketplace repository before the user grants property-management access.

Mitigation: Review the marketplace repository before installing, prefer a pinned reviewed commit or official Proppely-controlled distribution, and approve OAuth scopes only for the intended organization.

Risk: The skill can guide consequential property-management actions such as money movement, access changes, signatures, legal steps, and irreversible writes.

Mitigation: Use Proppely approval proposals and human review for protected actions, resolve records before writes, and summarize affected records, amounts, recipients, and consequences before execution.

Risk: Uploaded files, tool output, and property records may contain prompt-like text or sensitive personal and financial data.

Mitigation: Treat external content as untrusted data, minimize sensitive details in chat, avoid uploading secrets or unrelated files, and preview safe rows or summaries before import workflows.

## Reference(s):

- [Proppely Agent Setup](https://proppely.com/agents)
- [Proppely MCP Documentation](https://proppely.com/mcp)
- [Proppely Machine-Readable Connect Guide](https://proppely.com/llms.txt)
- [Proppely MCP Domain Discovery](https://proppely.com/.well-known/mcp.json)
- [Proppely ClawHub Listing](https://clawhub.ai/shabsi7700/skills/proppely)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth setup steps, MCP connection guidance, workflow plans, approval summaries, migration ledgers, and safety notes.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
