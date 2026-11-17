## Description:

基于 IT桔子 MCP 数据生成赛道融资动态简报、投资人项目观察、活跃机构分析。连接线上 MCP 端点查询真实融资事件和投资机构数据，输出面向投资人的结构化简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyentq-alt](https://clawhub.ai/user/skyentq-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and investment researchers use this skill to query IT桔子 MCP data for sector funding events, notable projects, and active investors over a requested time range. It is intended to produce investor-facing market briefings grounded in returned MCP results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an IT桔子 MCP API key during use.

Mitigation: Provide the key only through the MCP client or tool parameters, and avoid storing real API keys in skill files or shared prompts.

Risk: Funding data may include undisclosed, incomplete, or small-sample results.

Mitigation: Base conclusions only on MCP query results, explicitly note missing amounts and limited samples, and avoid unsupported predictions or investment scoring.

Risk: Briefings are expected to be Chinese-language by default.

Mitigation: Ask the agent to adapt the output language when an English or bilingual briefing is required.

## Reference(s):

- [IT桔子 MCP endpoint](https://mcp.itjuzi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/skyentq-alt/skills/itjuzi)
- [ClawHub publisher profile](https://clawhub.ai/user/skyentq-alt)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, API Calls, Guidance]

**Output Format:** [Markdown briefing with tables and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided IT桔子 MCP API key; conclusions should remain tied to returned MCP data and note incomplete funding amounts or small samples.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
