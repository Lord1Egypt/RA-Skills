## Description: <br>
帮助代理查询卖家之家跨境电商服务商分类，并按分类、关键词和分页游标搜索服务商。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up MJZJ service-provider categories and search cross-border e-commerce service providers by category, keyword, and cursor. It supports public search workflows and references an authenticated follow-on messaging workflow when a user chooses to contact a provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks for MJZJ_API_KEY even though the documented search endpoints are public. <br>
Mitigation: Configure MJZJ_API_KEY only when needed for authenticated follow-on actions, and avoid exposing the credential in prompts, logs, or shell history. <br>
Risk: Provider private messaging is outside the declared public search scope and can contact third parties. <br>
Mitigation: Require explicit user approval of the recipient userSlug and exact message text before any private message is sent. <br>
Risk: Snowflake and other id-like fields can exceed safe integer precision on some platforms. <br>
Mitigation: Handle id, cid, labelIds elements, and nextPosition as strings for input, output, and parameter passing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-sp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mjzj-tec) <br>
- [MJZJ service-provider homepage](https://sp.mjzj.com) <br>
- [MJZJ service classifications endpoint](https://data.mjzj.com/api/spQuery/getClassifies) <br>
- [MJZJ provider search endpoint](https://data.mjzj.com/api/spQuery/queryProviders) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, API calls] <br>
**Output Format:** [Markdown with inline curl examples and API parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [ID-like fields, including Snowflake IDs, must be treated as strings end to end.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
