## Description: <br>
按关键词搜索公众号文章，返回标题、摘要、时间、账号与链接等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content researchers use this skill to search WeChat public-account articles by keyword, collect article metadata, and optionally resolve article links or fetch content when site controls allow it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and optional content fetches are sent to Sogou/WeChat. <br>
Mitigation: Run the skill only with queries that are appropriate to share with those services, and review the target sites' terms before use. <br>
Risk: High-frequency scraping can trigger blocking or violate site rules. <br>
Mitigation: Keep request volume low, use retries and delays conservatively, and stop when anti-spider or blocked statuses appear. <br>
Risk: The skill depends on third-party Python packages and makes outbound web requests. <br>
Mitigation: Install dependencies in a controlled Python environment and run with network access limited to the sites required for the search task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-wechat-article) <br>
- [Related wechat-mp skill](https://clawhub.ai/jisuapi/wechat-mp) <br>
- [JisuAPI publisher site](https://www.jisuapi.com/) <br>
- [Sogou Weixin search](https://weixin.sogou.com/weixin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text result blocks or JSON from the Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns titles, summaries, publish times, source accounts, and links; optional content fetching is capped by --content-max-chars and may be blocked by site controls.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
