## Description:

Connects OpenClaw agents to WeCom through Bot WebSocket, self-built Agent API, and WeCom customer-service channels, with media handling and document, calendar, and MCP tool access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

ISC

## Use Case:

Developers and teams use this skill to connect OpenClaw agents to enterprise WeCom conversations, route replies across Bot WebSocket, Agent API, and customer-service channels, and expose WeCom document, calendar, media, and collaboration capabilities to agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin can read and send local files through media handling.

Mitigation: Limit media localRoots to dedicated staging directories and require human confirmation before file uploads.

Risk: The plugin can mutate WeCom business documents and calendars.

Mitigation: Use scoped WeCom credentials, restrict tool access to trusted agents, and review destructive document or calendar actions before execution.

Risk: Dynamic agent configuration can persist new routing and workspace state.

Mitigation: Disable dynamicAgents until intentionally configured, set account and agent limits, and review generated workspace paths.

Risk: The security evidence recommends upgrading vulnerable dependencies before production use.

Mitigation: Run dependency review and update vulnerable packages before deploying in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-wecom-plugin)
- [Project homepage listed in artifact](https://cnb.cool/huo15/ai/huo15-wecom-plugin)
- [WeCom calendar API documentation](https://developer.work.weixin.qq.com/document/path/93329)
- [WeCom upstream configuration documentation](https://developer.work.weixin.qq.com/document/path/95813)
- [WeCom document tool guide](SKILLS_DOC.md)
- [WeCom calendar tool guide](SKILLS_CAL.md)
- [Release changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/YAML configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose WeCom messages, media uploads, document/calendar operations, and plugin configuration changes.]

## Skill Version(s):

2.9.5 (source: server release, package.json, and changelog; SKILL.md frontmatter lists 2.9.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
