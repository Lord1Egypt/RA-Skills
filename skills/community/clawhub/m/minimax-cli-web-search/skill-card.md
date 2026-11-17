## Description:

Web search via MiniMax MCP using a local CLI wrapper (mcporter), with environment preflight, API-key/config checks, and normalized result formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biggersun](https://clawhub.ai/user/biggersun)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run real-time web searches through a configured MiniMax MCP server, returning concise findings with source links for research and time-sensitive fact checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured MiniMax/MCP service and may expose sensitive text if users include secrets or private information.

Mitigation: Avoid secrets, private documents, and sensitive personal information in queries.

Risk: Local mcporter or MiniMax MCP configuration may be missing, unhealthy, or using invalid authentication.

Mitigation: Run the preflight check before first use in a new environment and verify the MCP server and API key setup locally.

Risk: Network, timeout, or upstream response variance can reduce search quality or reliability.

Mitigation: Use normalized JSON output for automation, adjust timeout when needed, and retry with narrower queries.

## Reference(s):

- [Environment Checklist](references/environment-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/biggersun/skills/minimax-cli-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional normalized JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes ordered results with title, URL, snippet, and date when available.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
