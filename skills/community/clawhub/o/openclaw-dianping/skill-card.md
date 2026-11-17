## Description:

查询大众点评餐厅信息，包括评分、人均消费、地址、菜系或区域推荐，并提示使用城市 URL/ID 处理定位问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[newaiguy](https://clawhub.ai/user/newaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to guide an agent through Dianping restaurant searches by name, cuisine, area, or nearby recommendations, then summarize restaurant cards with ratings, average spend, addresses, highlights, and review snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the user is logged in, restaurant searches and page views may use the user's Dianping session.

Mitigation: Install only when browser-based Dianping searches are intended, and have the user enter any phone or SMS verification themselves.

Risk: Restaurant details depend on live Dianping pages and may vary by city URL, city ID, account location, or page loading state.

Mitigation: Confirm the target city in the URL or query, review extracted restaurant details before relying on them, and scroll when needed to load complete results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newaiguy/skills/openclaw-dianping)
- [Dianping Hangzhou](https://www.dianping.com/hangzhou)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summaries with restaurant details and browser navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on live Dianping page content, login state, city URL or city ID, and user-entered SMS verification when required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
