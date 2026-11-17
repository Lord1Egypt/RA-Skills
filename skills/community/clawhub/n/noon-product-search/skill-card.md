## Description:

Noon 商品搜索工具用于输入阿拉伯语关键词，使用 Chrome 浏览器在 noon.com/saudi-ar 搜索并返回商品标题、评分、评价数和价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Noon Saudi Arabia search result data for Arabic product keywords, including product titles, ratings, review counts, and prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation and may require Chrome remote debugging or broad browser control.

Mitigation: Run it only in a disposable browser profile or isolated environment, and do not use a normal Chrome profile with remote debugging enabled.

Risk: The scraping behavior may collect more results than the documentation's first-page wording suggests.

Mitigation: Review the skill before installation and limit the browser session, query scope, and run environment to the intended collection task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/skills/noon-product-search)
- [Publisher profile](https://clawhub.ai/user/freemanwangfuhan-coder)
- [Noon Saudi Arabia](https://www.noon.com/saudi-ar/)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Console text listing product records with title, rating, review count, and price.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return up to 60 de-duplicated product records.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
