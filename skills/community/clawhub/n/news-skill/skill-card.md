## Description:

Provides brief latest-news summaries for a user-specified topic, including item titles, sources where available, and short overviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request concise current-news summaries for a topic, such as AI, Bitcoin, or technology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed payment API key.

Mitigation: Remove the key from the artifact, rotate the exposed credential, and require secure runtime configuration before release.

Risk: The release evidence reports automatic per-call billing and broken billing or loading behavior.

Mitigation: Fail closed on billing errors, repair load-time issues, and clearly disclose billing and consent behavior before the skill is used.

Risk: The release evidence reports that user and query data are sent to external services.

Mitigation: Disclose the external news and billing service paths and obtain appropriate user consent before sending requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loverun321/skills/news-skill)
- [Publisher profile](https://clawhub.ai/user/loverun321)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing the requested topic, news item titles and summaries, item count, payment status, or error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five news items and may include payment-required or fetch-error responses.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
