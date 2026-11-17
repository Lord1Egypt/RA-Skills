## Description:

每天早晨 9 点推送适合孩子阅读的 KidsNews 精选新闻摘要，并附思考问题、辩论话题和详情链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shujip](https://clawhub.ai/user/shujip)

### License/Terms of Use:

MIT-0

## Use Case:

Families and caregivers use this skill to receive a concise Simplified Chinese daily news brief for children, with prompts that support discussion, reflection, and debate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring news brief delivery may surprise users if scheduling is enabled without clear consent.

Mitigation: Enable scheduled delivery only after the user agrees to receive the daily KidsNews brief.

Risk: News links could direct users outside the expected KidsNews destination if API responses are not checked.

Mitigation: Validate that returned links use HTTPS and stay on the KidsNews domain before including them in the brief.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shujip/skills/kidsnews)
- [KidsNews daily report API](https://www.kidsnews.app/api/kidsnews/daily-report)
- [KidsNews website](https://www.kidsnews.app)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Simplified Chinese Markdown daily brief with linked news summaries, questions, and debate topics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled delivery is suggested for 09:00 local server time; returned links should remain on the expected HTTPS KidsNews domain.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
