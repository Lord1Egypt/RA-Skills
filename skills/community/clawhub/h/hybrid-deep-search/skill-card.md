## Description:

Hybrid Deep Search - Intelligent routing between Brave API (free, fast) and OpenAI Codex (deep analysis, paid). Auto-selects optimal search strategy based on query complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scsun1978](https://clawhub.ai/user/scsun1978)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to route search queries between fast web lookup and deeper Codex-assisted analysis based on query complexity. It supports quick fact finding, comparison research, news-oriented lookup, academic-oriented lookup, and structured search output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says auto mode may route sensitive queries to external providers and may trigger paid OpenAI usage.

Mitigation: Review queries before using auto or codex mode, configure OPENAI_API_KEY deliberately, and use quick mode when external paid routing is not acceptable.

Risk: The security review says the skill may be a prototype and may not perform real search yet.

Mitigation: Validate behavior in a controlled workspace, check returned source quality, and treat results as unverified until the search path is confirmed.

Risk: The security review says declared shell and network permissions are broad for sensitive workspaces.

Mitigation: Narrow allowed commands and network access before deployment, and review the skill before installation.

## Reference(s):

- [Brave Search API](https://brave.com/search/api/)
- [OpenAI GPT-5-Codex](https://platform.openai.com/docs/models/gpt-5-codex)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or plain text search results with optional command-line usage and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes queries in quick, codex, or auto mode; codex mode requires OPENAI_API_KEY and may use paid external API access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
