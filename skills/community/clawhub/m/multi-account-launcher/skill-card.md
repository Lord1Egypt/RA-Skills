## Description:

通过 HTTP API 控制多账号矩阵管理工具，实现浏览器账号的启动、关闭和信息查询，支持按名称和索引操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control a local multi-account browser matrix tool by listing accounts, starting accounts, stopping accounts, and matching accounts by name or index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Start and stop commands may open or close active browser account sessions.

Mitigation: Verify account names or indexes before issuing start or stop commands.

Risk: The skill sends HTTP control requests to the configured API endpoint.

Mitigation: Keep the API URL bound to localhost and avoid changing config.yaml to an external address.

Risk: Runtime dependencies may vary if installed without version control.

Mitigation: Use a virtual environment and prefer pinned dependencies when installing requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wociaozhongyunonghaole/skills/multi-account-launcher)
- [Multi-account matrix tool website](https://zmt.scys6688.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and plain-text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes UTF-8 command results to last_result.txt for reliable Chinese text handling.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
