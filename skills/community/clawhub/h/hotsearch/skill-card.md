## Description: <br>
Fetches Weibo, Baidu, and Douyin hot-search rankings, links, scores, and update times through the JisuAPI hotsearch service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current hot-search lists from Weibo, Baidu, or Douyin and summarize the ranked topics with links and popularity signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JisuAPI AppKey and sends it to JisuAPI when retrieving hot-search rankings. <br>
Mitigation: Use only an intended JisuAPI key, scope and rotate it according to the provider account controls, and do not expose the key in prompts or logs. <br>
Risk: The skill contacts JisuAPI for live Weibo, Baidu, or Douyin hot-search data whenever a platform command is run. <br>
Mitigation: Run it only when current hot-search results are needed, and ask for a specific platform name to avoid unnecessary external API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/hotsearch) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>
- [JisuAPI hotsearch API documentation](https://www.jisuapi.com/api/hotsearch/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON arrays or JSON error objects from the Python script, with agent-authored text or Markdown summaries for users.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a JISU_API_KEY environment variable, and one platform argument: weibo, baidu, or douyin.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
