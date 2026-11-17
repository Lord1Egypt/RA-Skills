## Description:

Fetches daily news recommendations from a fixed API, lets an agent sort items by user interests or query terms, and generates a responsive H5 daily report page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxcoder1997](https://clawhub.ai/user/yxcoder1997)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chinese-language daily news recommendations, personalize their order from explicit preferences or consented context, and generate a local H5 report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use profile or memory data for news personalization.

Mitigation: Use profile or long-term memory data only with explicit user consent, and avoid storing inferred traits unless they are needed for the requested report.

Risk: The generated HTML uses untrusted news titles, summaries, images, and URLs.

Mitigation: Escape news fields and validate links before opening or sharing the generated H5 report.

Risk: The skill depends on a fixed external news API and local report files.

Mitigation: Review the API endpoint and generated local files before installation or deployment in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxcoder1997/skills/jt-daily-report)
- [Daily news recommendation API](https://jiutian.10086.cn/jiujiuassist/proactive/get_user_news_recommend)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON sorted ID data, and a generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report data under data/ and output/daily_report.html.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
