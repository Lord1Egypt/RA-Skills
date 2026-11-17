## Description:

OpenClaw Regex Engine gives agents MCP tools to test regex patterns, explain them in plain English, build patterns from natural-language descriptions, browse curated examples, and perform regex find-and-replace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they need to test, explain, generate, browse, or apply JavaScript-compatible regular expressions through a remote MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User regex patterns and sample text can be sent to an external MCP service.

Mitigation: Use the skill only with content suitable for external processing, and avoid secrets, credentials, regulated personal data, proprietary code, and confidential documents.

Risk: The skill privacy wording may understate external disclosure because processing happens through a remote service.

Mitigation: Prefer explicit confirmation before invoking regex tools on pasted or sensitive-looking content.

Risk: Regexes generated or selected by the skill may be incomplete for security validation or complex parsing.

Mitigation: Treat generated patterns as implementation aids, test them against positive and negative examples, and combine format checks with application-side validation.

## Reference(s):

- [OpenClaw Regex Engine on ClawHub](https://clawhub.ai/yedanyagamiai-cmd/skills/openclaw-regex-engine)
- [Publisher profile](https://clawhub.ai/user/yedanyagamiai-cmd)
- [OpenClaw homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers)
- [Regex Engine MCP endpoint](https://regex-engine-mcp.yagami8095.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool results and regex code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls may send pattern and input text to a remote MCP service; avoid secrets and regulated or confidential data.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
