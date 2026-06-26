## Description: <br>
短链接。支持生成短链接、短链接还原和短链接访问统计，可设置最大访问次数和到期时间。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create short links, restore a short link to its target URL, and retrieve short-link access statistics through the JikeAPI short-link service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL data and the JikeAPI key are sent to the JikeAPI service. <br>
Mitigation: Avoid using the skill with private internal URLs, secrets, or sensitive identifiers. <br>
Risk: The API base URL can be overridden through JIKE_API_BASE_URL. <br>
Mitigation: Verify JIKE_API_BASE_URL is unset or points to the expected JikeAPI host before use. <br>
Risk: Creating a short link is a write operation that creates a real link through the external service. <br>
Mitigation: Confirm the target URL and any expiration or access-count limits before running the create command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-shortlink) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI short-link create endpoint](https://api.jikeapi.cn/v1/shortlink/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON command output, with Markdown guidance and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_SHORTLINK_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
