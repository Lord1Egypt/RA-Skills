## Description:

查品牌、车系、车型详情、搜索与热门/销量榜等。当用户说：比亚迪汉有什么配置？十万左右 SUV 推荐车型数据，或类似车型库问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up Chinese vehicle brands, series, model details, search results, popular models, and sales rankings through JisuAPI-backed car catalog data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's JisuAPI AppKey and car lookup parameters to JisuAPI.

Mitigation: Use a dedicated, limited-quota API key where possible and rotate it if it may have been logged or exposed.

Risk: Returned vehicle data may depend on JisuAPI availability, permissions, quotas, and current catalog coverage.

Mitigation: Check returned error JSON and API status before relying on results in downstream recommendations or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-car)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Car API documentation](https://www.jisuapi.com/api/car)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; API calls return JisuAPI car data or structured error JSON.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
