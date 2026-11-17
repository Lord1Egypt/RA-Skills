## Description:

拼多多商家客服自动化助手，基于 CDP 连接浏览器，帮助商家登录拼多多商家后台、读取买家消息、生成客服回复并处理售后工作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and operations teams use this skill to assist with Pinduoduo customer-service workflows, including message monitoring, prepared replies, template management, and after-sales triage. Operators should review generated replies and actions before sending or applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can access active merchant sessions and customer data through the user's browser.

Mitigation: Run the skill only in a dedicated browser profile with no unrelated sessions, and review proposed browser actions before allowing them to execute.

Risk: A CDP proxy or remote debugging endpoint can expose high-impact browser control if it is reachable by untrusted clients.

Mitigation: Keep the proxy bound to localhost, protect it with authentication, and disable Chrome remote debugging when the skill is not in use.

Risk: Merchant credentials, customer conversations, exports, notifications, or CDB_URL-backed storage can transmit or retain sensitive customer data.

Mitigation: Do not store merchant passwords in config files; require explicit approval, retention limits, and access controls for exports, notifications, and database-backed storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/pinduoduo-cs-assistant-v2)
- [Pinduoduo merchant backend](https://mms.pinduoduo.com)
- [README](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing browser automation guidance and customer-service reply suggestions; generated actions should be reviewed before execution.]

## Skill Version(s):

1.1.1 (source: server release, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
