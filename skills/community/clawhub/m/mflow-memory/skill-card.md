## Description:

Long-term memory engine for OpenClaw agents using M-flow knowledge graphs that stores conversations as structured episodic memories and retrieves them via graph-routed search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowelement-alexunbridled](https://clawhub.ai/user/flowelement-alexunbridled)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to give agents persistent memory for past conversations, preferences, facts, and decisions. It is intended for agents that need memory search, storage, deletion, and graph-based recall across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversation-derived memories across sessions.

Mitigation: Use it only where long-term retention is expected, review stored memories regularly, and avoid storing secrets, regulated data, or confidential work without consent and retention controls.

Risk: The setup starts a Docker MCP service and exposes a local port.

Mitigation: Run it on a trusted local machine, keep the service bound to localhost, and review the generated OpenClaw MCP registration before use.

Risk: The skill requires an LLM API key for knowledge extraction.

Mitigation: Use a limited API key with budget controls and avoid entering credentials into shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowelement-alexunbridled/skills/mflow-memory)
- [M-flow GitHub](https://github.com/FlowElement-ai/m_flow)
- [M-flow documentation](https://docs.m-flow.ai)
- [M-flow skill repository path](https://github.com/FlowElement-ai/m_flow/tree/main/openclaw-skill/mflow-memory)
- [M-flow benchmarks](https://github.com/FlowElement-ai/mflow-benchmarks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and an LLM_API_KEY; stores memory data in a Docker volume and registers an MCP server with OpenClaw.]

## Skill Version(s):

0.3.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
