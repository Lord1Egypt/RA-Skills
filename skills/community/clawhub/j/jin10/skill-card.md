## Description:

金十数据 enables an agent to query Jin10 financial market quotes, K-line data, flash headlines, news details, and economic calendar events through the bundled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinspt](https://clawhub.ai/user/robinspt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to retrieve Jin10 market quotes, K-line/candlestick data, financial news, flash updates, and economic calendar information for finance-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Jin10 API token and sends financial-data queries to the Jin10 MCP endpoint.

Mitigation: Store JIN10_API_TOKEN as a scoped environment variable or managed OpenClaw configuration value, and install only when sharing queries with Jin10 is acceptable.

Risk: CLI output and documentation are mostly Chinese, which may lead to misunderstanding of returned financial data.

Mitigation: Review returned fields and translate or summarize results before using them in user-facing decisions.

## Reference(s):

- [Jin10 API Contract](references/api-contract.md)
- [Jin10 MCP endpoint](https://mcp.jin10.com/mcp)
- [Jin10 API token setup](https://mcp.jin10.com/app)
- [ClawHub skill page](https://clawhub.ai/robinspt/skills/jin10)
- [ClawHub publisher profile](https://clawhub.ai/user/robinspt)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, plus JSON or text results from the bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JIN10_API_TOKEN; default command output is JSON, with text output available for user-facing summaries.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
