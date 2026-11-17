## Description:

HeartFlow is a local rule-engine cognitive preprocessor for text classification, PAD emotion detection, decision routing, and structured cognition signals for downstream agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run deterministic pre-processing and MCP tools that analyze input text, route decisions, check cognitive or module status, and produce structured signals for downstream AI responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary classifies the package as suspicious because it is a broad local MCP service with memory and self-modifying behavior, and its documentation understates several high-impact runtime behaviors.

Mitigation: Review carefully before installation, run as an unprivileged user in an isolated directory, and only enable MCP server, persistence, daemon mode, benchmark imports, or self-modifying behavior when needed.

Risk: The MCP server can expose local agent functionality over HTTP/SSE if run.

Mitigation: Set HEARTFLOW_MCP_TOKEN explicitly, avoid shared parent .env files, bind and expose the server only in trusted environments, and stop the service when it is not in active use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-cognitive-engine)
- [Publisher profile](https://clawhub.ai/user/yun520-1)
- [npm package](https://www.npmjs.com/package/@yun520-1/heartflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-like structured text with optional shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool responses, classification labels, emotion scores, routing decisions, status checks, and operational guidance.]

## Skill Version(s):

6.3.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
