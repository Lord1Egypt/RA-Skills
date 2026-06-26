## Description: <br>
自媒体文章生成技能 - 根据关键词自动搜索、汇总数据、生成抖音/小红书/微博文章，特别擅长美食（面食）主题 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyi0329-pixel](https://clawhub.ai/user/fyi0329-pixel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External content creators and marketing teams use this skill to research noodle and food topics, extract useful facts, and generate platform-specific drafts for Douyin, Xiaohongshu, and Weibo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided topics and keywords can be passed into a shell command during search. <br>
Mitigation: Run only with trusted inputs until search execution is rewritten to use safe argument passing or direct API calls. <br>
Risk: Generated posts may contain inaccurate, misleading, or outdated food and venue claims from search results. <br>
Mitigation: Review generated articles and cited source data before publishing. <br>
Risk: Raw output data may retain prompts, search results, and generated content in the workspace. <br>
Mitigation: Use a constrained workspace and delete raw output data that should not be retained. <br>
Risk: The skill requires a Tavily API key for search. <br>
Mitigation: Set the API key intentionally and avoid including confidential information in topics or keywords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fyi0329-pixel/noodle-create-writing) <br>
- [Tavily API documentation](https://tavily.com) <br>
- [OpenClaw skill development guide](https://docs.openclaw.ai) <br>
- [Weibo](https://weibo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown article drafts, plain text copies, and JSON source data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate platform-specific drafts for Douyin, Xiaohongshu, Weibo, or all supported platforms.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
