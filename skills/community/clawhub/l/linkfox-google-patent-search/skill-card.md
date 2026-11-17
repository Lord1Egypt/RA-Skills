## Description:

Searches Google Patents for public patent records by keyword, inventor, assignee, country, date, and status, returning bibliographic fields, patent links, and PDF links for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, cross-border sellers, and developers use this skill to discover patent records for prior-art research, freedom-to-operate checks, and patent-infringement risk screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries, account details, phone-based login flow, payment operations, and feedback data are handled through LinkFox services.

Mitigation: Install only if LinkFox is trusted for those data categories, avoid confidential patent strategy unless endpoint variables are controlled, and store API keys in a proper secret manager.

Risk: The skill writes complete search responses and cache data to local files.

Mitigation: Run it from an intended writable workspace, review output and cache paths before use, and remove sensitive saved results when they are no longer needed.

Risk: Search calls consume credits and auth or billing recovery can involve package selection and payment operations.

Mitigation: Confirm expected cost before repeat searches, avoid automatic retries or query expansion, and validate plan and payment choices with the user.

## Reference(s):

- [谷歌专利检索 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-google-patent-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, and saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses may be summarized in stdout while the full response is saved locally; repeated queries may be cached for 24 hours.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
