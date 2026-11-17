## Description:

小红书热点追踪 × 爆文生成 × 知识卡片 × 公众号发布全链路自动化

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, social media operators, and publication editors use this skill to collect trending topics, analyze topic potential, generate long-form WeChat-style articles and knowledge cards, and archive outputs to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create and share Feishu documents from AI-generated public-trend content without a clear approval gate.

Mitigation: Run in draft mode first, review generated articles, cards, and links before sharing, and restrict the Feishu bot to a dedicated folder.

Risk: Scheduled runs may repeatedly collect public trends and publish generated content before human validation.

Mitigation: Avoid scheduled execution until approval and validation steps are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/skills/neirong-liebian-gongchang)
- [README](artifact/README.md)
- [Workflow Configuration](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown article content, structured JSON analysis, knowledge-card file references, and Feishu document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Feishu documents by default unless draft mode is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
