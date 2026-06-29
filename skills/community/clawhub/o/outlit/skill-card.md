## Description: <br>
Use when accessing Outlit customer intelligence through the `outlit` CLI, Outlit MCP tools, Pi tools, or @outlit/tools, including customer lookups, users, workspace users, timelines, facts, source evidence, semantic search, revenue, churn, SQL analytics, setup, notifications, integrations, or troubleshooting agent access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-paz](https://clawhub.ai/user/leo-paz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and customer-facing teams use this skill to query Outlit customer intelligence, inspect customer timelines and facts, run read-only analytics, configure agent access, and troubleshoot integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to access customer intelligence data that may include sensitive customer, billing, support, CRM, and communication context. <br>
Mitigation: Install and use it only in trusted Outlit workspaces, request only needed fields, and handle returned customer data according to the user's data governance requirements. <br>
Risk: Credential handling is required for CLI or tool access. <br>
Mitigation: Prefer OAuth or environment-based credentials such as OUTLIT_API_KEY, avoid hardcoding shared endpoints or bearer tokens, and verify authentication state before use. <br>
Risk: The fast installer uses a curl-to-bash pattern. <br>
Mitigation: Prefer the documented npm or Homebrew install paths when possible, and review installer behavior before running direct shell installation. <br>
Risk: Notification and integration setup commands can perform account-level actions. <br>
Mitigation: Run notification, integration setup, or provider credential commands only after the user explicitly asks for those actions. <br>


## Reference(s): <br>
- [Outlit homepage](https://outlit.ai) <br>
- [Outlit documentation](https://docs.outlit.ai/) <br>
- [CLI overview](https://docs.outlit.ai/cli/overview) <br>
- [CLI commands](https://docs.outlit.ai/cli/commands) <br>
- [CLI integrations](https://docs.outlit.ai/cli/integrations) <br>
- [AI agent setup](https://docs.outlit.ai/cli/ai-agents) <br>
- [Agent skills](https://docs.outlit.ai/ai-integrations/skills) <br>
- [MCP integration](https://docs.outlit.ai/ai-integrations/mcp) <br>
- [Pi agents](https://docs.outlit.ai/ai-integrations/pi) <br>
- [Public tools API](https://docs.outlit.ai/api-reference/tools) <br>
- [Customer context graph](https://docs.outlit.ai/concepts/customer-context-graph) <br>
- [SQL Reference](references/sql-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, SQL, Markdown] <br>
**Output Format:** [Markdown with inline shell commands, SQL snippets, and references to CLI, MCP, and Pi tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI usage and evidence citations from customer records, timelines, facts, search results, sources, or SQL results.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
