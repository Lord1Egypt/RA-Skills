## Description: <br>
新闻汇总与邮件投递技能。当用户要求"生成今日新闻汇总"、"把新闻发给邮箱"时触发。支持：(1) 接收用户指定主题，搜索生成新闻汇总；(2) 按用户要求投递到指定邮箱。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliangjie91](https://clawhub.ai/user/liliangjie91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate daily Chinese-language news summaries across configured topics, organize sources into structured briefs, and optionally send the resulting report by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated news content can be sent through a configured Gmail command without clear pre-send safeguards. <br>
Mitigation: Review the recipient, subject, attachment, and generated HTML body before sending; require explicit user confirmation or use a safer email tool that avoids raw shell interpolation. <br>


## Reference(s): <br>
- [News Sum ClawHub release](https://clawhub.ai/liliangjie91/news-sum) <br>
- [Journalist prompt template](references/journalist.md) <br>
- [Editor prompt template](references/editor.md) <br>
- [Final news brief format](references/format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown news briefs, JSON news records, and a Gmail send command when email delivery is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates dated archive files for news summaries, draft briefs, topic JSON, and recent-brief tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
