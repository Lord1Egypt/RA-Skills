## Description: <br>
全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, WeChat Official Account operators, editors, and content strategists use this skill to retrieve ranked original WeChat article recommendations by category and date, generate a shareable HTML report, and request daily subscription-style updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a REDFOX_API_KEY and sends it to the RedFox service. <br>
Mitigation: Install only if the user trusts RedFox, store the key in an environment variable, and avoid exposing it in prompts, logs, or generated files. <br>
Risk: Security review marked this version suspicious because HTTPS certificate checks are disabled while sending the required API key. <br>
Mitigation: Restore TLS certificate verification before production use or defer deployment until the publisher remediates this behavior. <br>
Risk: Generated HTML may include remote article data. <br>
Mitigation: Escape remote article fields before rendering HTML and review generated files before sharing or opening them in sensitive environments. <br>
Risk: Subscription behavior can create recurring pushes. <br>
Mitigation: Require clear opt-in before enabling subscriptions and provide a clear unsubscribe path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/gzh-original-article-king) <br>
- [Category mapping reference](references/category_mapping.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox article data API endpoint](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown article ranking tables, generated HTML reports, and setup or execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may generate a local HTML ranking file for PDF export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
