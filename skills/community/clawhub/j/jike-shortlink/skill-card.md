## Description:

短链接。支持生成短链接、短链接还原和短链接访问统计，可设置最大访问次数和到期时间。适用场景：用户说“帮我生成一个短链接”“还原这个短链跳到哪里”“查一下这个短链访问次数”等。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to create short links, restore short links to their target URLs, and check short-link access statistics through the Jike API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Jike API key and can expose it if passed on the command line or included in shared request examples.

Mitigation: Prefer environment variables for the API key, avoid command-line key arguments, and redact keys from logs, prompts, and copied output.

Risk: The API base URL is configurable through JIKE_API_BASE_URL, which can redirect requests and API keys to an unintended endpoint.

Mitigation: Leave JIKE_API_BASE_URL unset or lock it to the legitimate HTTPS Jike API host in managed environments.

Risk: Creating a short link is a write operation that publishes a reachable redirect for the target URL.

Mitigation: Confirm the target URL and access or expiration limits before creation, and avoid shortening sensitive or internal URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-shortlink)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike shortlink create endpoint](https://api.jikeapi.cn/v1/shortlink/create)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned from command-line short-link operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an API key provided through JIKE_SHORTLINK_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
