## Description:

生日花语。输入 MM-DD 生日，查询生日花、花语、诞生石及说明。适用场景：用户询问相关传统文化、生活常识或配对资料时使用。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to look up birthday flowers, flower meanings, birthstones, and related descriptions for an MM-DD birthday through Jike Data's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An influenced runtime environment can set JIKE_API_BASE_URL and redirect requests containing the configured AppKey to an arbitrary host.

Mitigation: Run the skill only in trusted environments where JIKE_API_BASE_URL is controlled, or use a version that hardcodes or allowlists https://api.jikeapi.cn.

Risk: Passing a real AppKey with the --key argument can expose the credential through shell history, process listings, or logs.

Mitigation: Prefer JIKE_BIRTHDAY_FLOWER_QUERY_KEY or JIKE_APPKEY environment variables for credentials and avoid logging command invocations that include secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-birthday-flower-query)
- [Jike Data homepage](https://www.jikeapi.cn/)
- [Birthday flower API endpoint](https://api.jikeapi.cn/v1/birthday/flower)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese text by default, or formatted JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey in JIKE_BIRTHDAY_FLOWER_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
