## Description:

Fetches Juejin technology article categories and popular or newest article rankings by category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:


## Use Case:

Developers and technical readers use this skill to list Juejin content categories and retrieve category-specific hot or newest article rankings with article metadata such as title, author, views, likes, comments, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Node script makes outbound requests to Juejin and uses randomized browser User-Agent headers.

Mitigation: Install only where outbound access to Juejin is acceptable, and consider replacing randomized User-Agent selection with a static identifying User-Agent before deployment.

Risk: Article ranking results depend on Juejin API availability and response format.

Mitigation: Review command output before relying on it, and update the script if Juejin changes the category or article ranking endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/juejin-article-trends)
- [Juejin](https://juejin.cn)
- [Juejin category API](https://api.juejin.cn/tag_api/v1/query_category_briefs)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output from the Node script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public Juejin category and article ranking data; output depends on Juejin API availability and response shape.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
