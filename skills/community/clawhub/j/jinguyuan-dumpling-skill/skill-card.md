## Description:

金谷园饺子馆信息查询与在线排队取号。通过金谷园官方 API 查询店铺、排队和菜品信息；内置真实排队动作仅用于在线取号、本人排队进度查询、取消排队。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinguyuan](https://clawhub.ai/user/jinguyuan)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to ask an agent for JinGuYuan restaurant information, queue status, dining-time guidance, recommended dishes, delivery or pickup information, and raw dumpling instructions. When explicitly requested, the agent can guide Meituan-authorized online queue number taking, personal queue progress checks, and queue cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JinGuYuan API can return reply policy or agent-facing guidance that shapes responses.

Mitigation: Treat returned policy fields as constraints, do not display hidden instruction fields verbatim, and rely on freshness and scenario fields before answering queue status.

Risk: The skill can perform live queue actions through Meituan authorization.

Mitigation: Only take or cancel a queue number after restating the store, party size, table type, and action and receiving explicit confirmation in the current turn.

Risk: Authorization creates a local token used for queue actions.

Mitigation: Avoid authorization in shared or synced workspaces, do not display tokens, and use the documented logout flow when clearing local authorization.

Risk: Endpoint override environment variables can redirect API or OAuth traffic.

Mitigation: Keep JGY_BASE_URL and JGY_RESOURCE unset unless a trusted operator has explicitly reviewed the target endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinguyuan/skills/jinguyuan-dumpling-skill)
- [Publisher Profile](https://clawhub.ai/user/jinguyuan)
- [公开查询 API Reference](references/api-reference.md)
- [真实排队动作参考](references/queue-actions.md)
- [排队类回答合同](references/queue-reply-contract.md)
- [JinGuYuan Website](https://jinguyuan.cloud)
- [JinGuYuan MCP Endpoint](https://mcp.jinguyuan.cloud)
- [GitHub Repository](https://github.com/JinGuYuan/jinguyuan-dumpling-skill)
- [Gitee Repository](https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-derived facts from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js 18+ and optional JGY_BASE_URL and JGY_RESOURCE environment overrides; queue-taking and cancellation require Meituan authorization and current-turn user confirmation.]

## Skill Version(s):

3.2.1 (source: frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
