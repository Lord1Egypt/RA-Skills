## Description:

Looks up Amazon keywords for up to 10 ASINs using Jungle Scout data, returning search volume, ranking, competition, PPC bid, trend, and relevance metrics across 10 marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers and ecommerce analysts use this skill to reverse lookup search terms and paid or organic keyword metrics associated with competitor or target Amazon ASINs. It supports keyword expansion, competitor keyword analysis, PPC bid research, and marketplace-specific keyword filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox handles ASIN queries, API keys, session metadata, and optional phone/SMS onboarding data.

Mitigation: Install only if this data handling is acceptable; prefer a secret store for API keys and avoid storing long-lived keys in shell startup files.

Risk: Endpoint override environment variables can redirect API traffic away from the default LinkFox services.

Mitigation: Avoid endpoint override environment variables unless the destination is explicitly reviewed and trusted.

Risk: The onboarding flow can access account, billing, and payment actions.

Mitigation: Review plan, order, and payment details with the user before any billing action, and do not poll or continue payment flows without explicit need.

Risk: Automatic feedback submission may send task context or user sentiment to LinkFox.

Mitigation: Allow feedback submission only after reviewing exactly what will be sent.

Risk: Keyword queries consume LinkFox compute credits and repeated retries can increase cost.

Mitigation: Warn the user before calls that may consume credits and avoid automatic retries, pagination, or parameter changes after failures or empty results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-keyword-by-asin)
- [Jungle Scout 根据 ASIN 反查关键词 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables with saved JSON response files; may include shell commands for API calls or onboarding.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are written to local JSON files, responses over 8 KB are summarized by default, and repeat calls may use a 24-hour local cache.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
