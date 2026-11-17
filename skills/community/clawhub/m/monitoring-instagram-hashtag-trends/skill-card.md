## Description:

Monitors Instagram hashtag performance and trends using apidojo's Instagram scraper on Apify, returning hashtag volume, average engagement, growth trends, top posts, and strategy recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External Instagram content creators, social media managers, and brand content teams use this skill to evaluate hashtag reach and engagement, identify trending or restricted tags, and build a balanced hashtag set for posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback demonstrates passing an Apify token in a URL query string, which can expose credentials through logs, browser history, or monitoring systems.

Mitigation: Use an Authorization header or the recommended helper script where possible, avoid copying the URL-token example as written, and use a narrowly scoped Apify token.

Risk: Requested Instagram hashtags or URLs are sent to Apify for scraping and analysis.

Mitigation: Only submit hashtags and URLs that are appropriate to share with Apify, and avoid sensitive campaign or account information unless approved for that workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-instagram-hashtag-trends)
- [ClawHub publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV or JSON scrape-result files when the user requests saved outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
