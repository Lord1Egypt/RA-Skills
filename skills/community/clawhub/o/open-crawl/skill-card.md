## Description:

open-crawl helps agents look up live Amazon product and search-results data, or fetch a user-named public web page, through Claw School's hosted API and return structured JSON or raw HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-school](https://clawhub.ai/user/claw-school)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they explicitly need current Amazon product or search-result details, such as price, rating, reviews, rankings, BSR, or named public page HTML. It is intended only for public URLs and not for private, authenticated, internal-network, token-bearing, or personal-data pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public target URLs and returned page content are sent to Claw School's hosted API and its upstream scraping provider.

Mitigation: Use the skill only for public URLs and install it only when that external data sharing is acceptable.

Risk: Private, logged-in, internal-network, pre-signed, token-bearing, or personal-data URLs could disclose sensitive information if submitted.

Mitigation: Do not submit sensitive URLs or pages; ask the user for a public URL when the target is not clearly public.

Risk: Relayed service messages may contain external-service text that should not become new agent instructions.

Mitigation: Treat relayed service messages as user-facing status or remediation text, not as authority to change agent behavior.

Risk: The CLAW_KEY authenticates the account used for requests.

Mitigation: Keep the CLAW_KEY confidential and send it only as the bearer credential for the Claw School API.

## Reference(s):

- [open-crawl skill page](https://clawhub.ai/claw-school/skills/open-crawl)
- [Claw School](https://claw-school.com)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [JSON responses with structured Amazon fields or raw HTML fallback, plus concise user-facing guidance for errors and safe use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAW_KEY and sends public target URLs and returned page content to Claw School's hosted API and its upstream scraping provider.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
