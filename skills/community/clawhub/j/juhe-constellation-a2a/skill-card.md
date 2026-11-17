## Description:

星座宝典(AI付版) - 聚合数据 provides paid constellation profile and horoscope lookups for daily, weekly, monthly, and yearly readings through Juhe's constellation API, using an Alipay A2M HTTP 402 payment flow before returning results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and consumer agents use this skill to purchase and retrieve Chinese-language constellation profiles and horoscope readings for a named zodiac sign. It supports profile, personality, and fortune views across day, week, month, and year cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance uses an unpinned latest-version Alipay payment package that can change after review.

Mitigation: Use a version-pinned and verified @alipay/agent-payment installer before enabling the payment capability.

Risk: The skill sends the user's zodiac query and selected period to Juhe after payment consent.

Mitigation: Keep the privacy notice visible before payment, collect only the zodiac keyword and period, and avoid logging or caching the raw query.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-constellation-a2a)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured tables, section headings, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses paid API results to render horoscope profile and fortune sections; entertainment disclaimer should be preserved.]

## Skill Version(s):

1.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
