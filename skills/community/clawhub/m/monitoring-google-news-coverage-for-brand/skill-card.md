## Description:

Monitors Google News coverage for a brand using apidojo's Google Search scraper on Apify and returns article titles, publications, dates, URLs, and coverage sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External PR agencies, communications teams, brand managers, and reputation monitoring services use this skill to track press mentions, compare coverage volume, classify sentiment, and identify stories that need PR attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and related result handling are sent to Apify and apidojo.

Mitigation: Avoid confidential investigation terms in queries and install only when that external processing is acceptable.

Risk: The REST fallback example can expose an Apify token in a URL query parameter.

Mitigation: Use a dedicated, least-privilege Apify token and prefer authorization-header based API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-google-news-coverage-for-brand)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, plus optional JSON or CSV files from the Apify actor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article title, publication, date, URL, type, sentiment, negative flags, and PR attention items.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
