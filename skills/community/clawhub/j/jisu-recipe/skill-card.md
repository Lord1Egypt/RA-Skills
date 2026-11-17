## Description:

按关键词或分类检索菜谱，可查分类与菜谱详情。当用户说：糖醋排骨怎么做？来个家常豆腐菜谱，或类似做菜问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search JisuAPI recipe data by keyword or category, inspect recipe classes, and retrieve full recipe details for cooking questions. It supports agents that answer recipe requests with ingredients, steps, tags, and related dish recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured JisuAPI AppKey and recipe lookup inputs to JisuAPI.

Mitigation: Install only when comfortable sharing those values with JisuAPI, and provide the key through the JISU_API_KEY environment variable.

Risk: Recipe results may include remote image URLs, including plain HTTP URLs.

Mitigation: Treat returned media URLs as untrusted and avoid automatically rendering them in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-recipe)
- [JisuAPI recipe API documentation](https://www.jisuapi.com/api/recipe/)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON returned from command-line API calls, usually summarized by the agent as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
