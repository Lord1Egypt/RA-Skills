## Description:

Korean search-keyword and shopping-trend analytics via the official NAVER DataLab API, with shell subcommands for search trends and shopping insight breakdowns by category, keyword, device, gender, and age.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing teams use this skill to collect Korean NAVER DataLab trend signals for SEO planning, commerce demand sensing, campaign timing, brand monitoring, and trend dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NAVER credentials and query data could be redirected away from the official API if NAVER_DATALAB_BASE is overridden.

Mitigation: Run only with NAVER_DATALAB_BASE unset or locked to https://openapi.naver.com/v1/datalab before providing NAVER_CLIENT_ID and NAVER_CLIENT_SECRET.

Risk: Submitted keywords, dates, categories, and demographic filters are sent to NAVER DataLab.

Mitigation: Avoid submitting confidential campaign terms or sensitive data as query inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/naver-datalab-cli)
- [NAVER Developers Application Registration](https://developers.naver.com/apps/#/register)
- [NAVER Shopping Insight Category Reference](https://datalab.naver.com/shoppingInsight/sCategory.naver)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSONL records and Markdown usage guidance with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs relative trend ratios rather than absolute search or shopping volumes.]

## Skill Version(s):

0.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
