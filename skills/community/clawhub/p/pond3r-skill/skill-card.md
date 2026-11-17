## Description:

Query crypto intelligence via Pond3r MCP: curated datasets, SQL queries, protocol metrics, yields, and market analysis for DeFi data, stablecoin yields, token opportunities, Polymarket trades, cross-protocol comparisons, and blockchain analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to query Pond3r crypto and DeFi datasets, inspect schemas, execute read-only SQL, and summarize market, protocol, yield, and opportunity data. It also provides configuration guidance for MCP-enabled runtimes and CLI-based access when native MCP tools are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text and report descriptions are sent to Pond3r services.

Mitigation: Install only when the user trusts Pond3r with those prompts and descriptions; avoid sending sensitive data unless approved.

Risk: The CLI query path can read SQL from a file path provided at runtime.

Mitigation: Do not let untrusted instructions choose --sql-file paths; review the file path and SQL before execution.

Risk: Report creation is a persistent external action.

Mitigation: Require explicit user approval before creating or scheduling reports through the Pond3r Report API.

Risk: API keys may be exposed through logs, chat, shell history, or shared files.

Mitigation: Keep POND3R_API_KEY in environment configuration, never print secret values, and rotate any exposed key immediately.

## Reference(s):

- [Pond3r Reference](artifact/reference.md)
- [Pond3r MCP Endpoint](https://mcp.pond3r.xyz/mcp)
- [Pond3r API Keys](https://makeit.pond3r.xyz/api-keys)
- [Pond3r Report API](https://api.pond3r.xyz/v1/api/reports)
- [Pond3r Web Interface](https://makeit.pond3r.xyz)
- [ClawHub Skill Page](https://clawhub.ai/fabriziogianni7/skills/pond3r-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact commands run, query outputs or summaries, dataset/schema details, failure messages, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
