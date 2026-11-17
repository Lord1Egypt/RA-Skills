## Description:

Provides onboarding guidance for PREF's quantitative research MCP server, including agent API key registration, authenticated client configuration, quota awareness, and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morluto](https://clawhub.ai/user/morluto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to connect Claude Code, Codex, or another MCP client to PREF quantitative research tools with a pref_agent key and verify authenticated quota instead of anonymous access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live PREF API key could be exposed through shell history, logs, prompts, transcripts, or shared terminal output.

Mitigation: Use a secure prompt, OS keychain, or protected editor flow for secrets, and rotate the PREF key if it has already been exposed.

Risk: Connecting a broad remote MCP server can expose more tool capability than an agent needs for a task.

Mitigation: Inspect the available PREF MCP tools before use and restrict the enabled remote tools to the task-relevant set.

## Reference(s):

- [PREF homepage](https://pref.trade)
- [PREF MCP endpoint](https://pref.trade/mcp)
- [PREF agent registration endpoint](https://pref.trade/v1/agents/register)
- [ClawHub skill page](https://clawhub.ai/morluto/skills/pref)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash, YAML, JSON, and text code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes remote MCP endpoint setup, bearer-token authentication, quota tiers, and verification guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
