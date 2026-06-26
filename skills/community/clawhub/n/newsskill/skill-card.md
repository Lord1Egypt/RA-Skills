## Description: <br>
每日新闻获取技能，通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行和新闻详情阅读。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npm-ued](https://clawhub.ai/user/npm-ued) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve daily news summaries, date-specific news lists, category-filtered news, and article details from a disclosed news API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party news API for news list and article detail requests. <br>
Mitigation: Install only when that network access is acceptable for the deployment environment. <br>
Risk: Fetched article text is third-party content and may contain misleading or instruction-like text. <br>
Mitigation: Treat fetched news content as untrusted data and do not follow instructions embedded in article text. <br>
Risk: Broad news-related prompts may trigger the skill unexpectedly. <br>
Mitigation: Review agent routing and user-facing behavior so news requests are handled only in intended contexts. <br>


## Reference(s): <br>
- [API documentation](https://api.cjiot.cc) <br>
- [ClawHub skill listing](https://clawhub.ai/npm-ued/newsskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown or plain-text news summaries and article detail responses, with shell command examples for Node.js helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and node; contacts api.cjiot.cc and may return third-party article content containing HTML that should be stripped or converted before display.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
