## Description:

Monitors tech acquisition news and M&A activity using apidojo's Google Search scraper, returning acquisition announcements, acquirer and target companies, deal size signals, and strategic rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, founders, investors, and competitive intelligence teams use this skill to monitor recent technology acquisition and M&A activity, classify search results, and summarize the strongest deal signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback places the Apify token in URL query strings, which can expose credentials in logs, process listings, shell history, or copied diagnostics.

Mitigation: Prefer Apify MCP or helper tooling that keeps secrets out of URLs; use authorization headers for REST calls, least-privilege Apify tokens, and token rotation if exposure is possible.

Risk: Breaking M&A search results may include rumors or early reports before official confirmation.

Mitigation: Label result status clearly, keep unconfirmed items separate from confirmed announcements, and verify important findings against official company releases before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-tech-acquisition-news-google)
- [Apify actor: apidojo/google-search-scraper](https://apify.com/apidojo/google-search-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables and inline shell commands; optional CSV or JSON result files when using the helper runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classifies results as confirmed, reported, rumored, or denied and includes a relevance score and summary.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
