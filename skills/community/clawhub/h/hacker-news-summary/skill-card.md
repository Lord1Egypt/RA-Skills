## Description:

Fetches the top 10 Hacker News stories, translates titles to Chinese with Baidu Translate, generates a bilingual Markdown report, and can optionally send it to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joewangup](https://clawhub.ai/user/joewangup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate a daily bilingual Hacker News digest and optionally deliver it to a Feishu group. It is suited for teams that want a lightweight automated technology-news briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hacker News titles are sent to Baidu Translate for processing.

Mitigation: Use only when this third-party translation service is acceptable for the content being translated.

Risk: The generated report can be posted to a configured Feishu webhook.

Mitigation: Set FEISHU_WEBHOOK only for approved destinations and protect the webhook as a secret.

Risk: Baidu API credentials and the Feishu webhook may be stored in shell environment files.

Mitigation: Use local secret-management practices and restrict file access to shell startup files containing credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joewangup/skills/hacker-news-summary)
- [Baidu Translate Open Platform](https://fanyi-api.baidu.com/)
- [Hacker News Firebase Top Stories API](https://hacker-news.firebaseio.com/v0/topstories.json)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown report and optional Feishu text message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_APPID and BAIDU_SECRET; FEISHU_WEBHOOK enables optional delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
