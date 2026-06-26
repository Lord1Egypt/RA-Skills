## Description: <br>
西瓜视频（Xigua）公开视频数据查询与内容分析 skill，通过 MaxHub API 查询视频详情、作者、评论、搜索、推荐和相关视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content analysts, researchers, and agent developers use this skill to query public Xigua video, author, comment, search, recommendation, and related-video data through MaxHub for content research and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the MaxHub API key plus user-provided IDs, keywords, URLs, and optional cookies or tokens to a third-party API service. <br>
Mitigation: Use only authorized data, avoid production session cookies, rotate the API key, and keep credentials out of logs and prompts. <br>
Risk: Returned comments, user data, and video playback links may contain personal data or content subject to platform terms. <br>
Mitigation: Minimize retained data, avoid public redistribution without authorization, and use playback links only for permitted analysis or archival workflows. <br>


## Reference(s): <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-xigua) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Recipe index](references/recipes/_index.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>
- [Video endpoint reference](references/post.md) <br>
- [User endpoint reference](references/user.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API calls require MAXHUB_API_KEY and send requests to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
