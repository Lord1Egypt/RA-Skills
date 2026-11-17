## Description:

Personal knowledge graph. Record notes, track moods, manage tasks, spot patterns in someone's life.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladikasik](https://clawhub.ai/user/vladikasik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Neron to connect to a personal knowledge graph, search notes and entities, track tasks and mood patterns, and record new notes or insights through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected agent can access sensitive journal-like data, including mood, body, substance, relationship, task, and inferred pattern records.

Mitigation: Use the skill only with trusted agents, protect the token or password, and rotate credentials if they may have been exposed.

Risk: The skill exposes write and delete operations that can alter or remove personal graph records.

Mitigation: Require explicit confirmation before writes, ai_note auto-logging, raw Cypher queries, or delete operations.

Risk: Pattern summaries or analytics may be sensitive or misleading when based on incomplete personal data.

Mitigation: Present insights as tentative, user-reviewable summaries and avoid exposing raw mood or body fields unless the user specifically asks.

## Reference(s):

- [Neron ClawHub skill page](https://clawhub.ai/vladikasik/skills/neron)
- [Neron MCP endpoint](https://mcp.neron.guru/mcp)
- [README](README.md)
- [Connect Agent](docs/CONNECT-AGENT.md)
- [Connect Neron to Claude](docs/CONNECT-CLAUDE.md)
- [Neron MCP Tool Reference](docs/mcp-tools.md)
- [Neron Quick Start](docs/USER-GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Natural language responses with JSON MCP tool arguments and Markdown setup examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and mutate a user's personal graph through MCP tools, including raw Cypher analytics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
