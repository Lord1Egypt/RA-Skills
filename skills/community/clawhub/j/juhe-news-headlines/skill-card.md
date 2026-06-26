## Description: <br>
查询聚合数据（juhe.cn）的最新新闻头条，支持国内、国际、体育、娱乐、科技、财经等分类列表和新闻详情。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current Chinese news headlines by category, page through results, and fetch article details by ID using a Juhe API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Juhe API key can be exposed because the skill sends requests over plain HTTP and supports command-line or local .env credential input. <br>
Mitigation: Use a low-privilege or quota-limited Juhe key, prefer the JUHE_NEWS_KEY environment variable, and use the skill only where plain-HTTP credential transport is acceptable. <br>
Risk: News categories, article IDs, and the API credential are sent to Juhe when the script queries headlines or article details. <br>
Mitigation: Use the skill only if sharing those request details with Juhe is acceptable for the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-news-headlines) <br>
- [Juhe News Headlines API](https://www.juhe.cn/docs/api/id/235) <br>
- [Juhe data platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_NEWS_KEY credential; supports category, pagination, filter, and article detail ID arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
