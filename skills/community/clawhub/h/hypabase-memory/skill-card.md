## Description:

Persistent memory for agents that stores preferences, decisions, facts, and events as a connected knowledge graph recalled by who, what, when, or why.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshidwasekar](https://clawhub.ai/user/harshidwasekar)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill to add persistent MCP-backed memory for preferences, project facts, decisions, events, and procedures. It helps agents remember structured facts in PENMAN form and later recall, consolidate, or forget those memories through the exposed memory tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores broad user, project, preference, decision, fact, and event memories in a persistent local database.

Mitigation: Use it only with an explicit retention policy and avoid storing secrets, credentials, health, financial, legal, or confidential work data.

Risk: The MCP server is launched through an unpinned external `hypabase` package.

Mitigation: Pin and review the package version before deployment where possible.

Risk: Using the OpenAI embedder can send memory contents to an external provider for processing.

Mitigation: Keep the default local embedder or choose another non-external option unless external processing is approved.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/harshidwasekar/skills/hypabase-memory)
- [Publisher profile](https://clawhub.ai/user/harshidwasekar)
- [Hypabase homepage](https://hypabase.app)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell command examples, and PENMAN memory examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool usage examples for remember, recall, consolidate, and forget.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
