## Description:

Scrape webpages through Claw School's proxy and return structured JSON for Amazon product and search pages or raw HTML for other URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbeihanda](https://clawhub.ai/user/linbeihanda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch webpages, collect Amazon product or search result data as structured JSON, and inspect raw HTML when structured parsing is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, request parameters, and returned page data are sent to the Claw School scraping service.

Mitigation: Use only URLs and data that are appropriate to share with that service, and verify the endpoint and data-handling terms before using sensitive business data.

Risk: The skill uses a non-expiring CLAW_KEY and an externally configured API base.

Mitigation: Set CLAW_API_BASE only to the intended trusted HTTPS service, avoid exposing the key, and rotate CLAW_KEY if exposure is suspected.

Risk: Scraping localhost, private network resources, authenticated pages, or URLs containing tokens could expose sensitive data.

Mitigation: Do not use the skill for private network targets, authenticated pages, token-bearing URLs, or sensitive internal resources.

## Reference(s):

- [Claw School](https://claw-school.com)
- [ClawHub skill page](https://clawhub.ai/linbeihanda/skills/omni-scraper)
- [Publisher profile](https://clawhub.ai/user/linbeihanda)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for API calls that can return structured JSON or raw HTML from the external scraping service.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
