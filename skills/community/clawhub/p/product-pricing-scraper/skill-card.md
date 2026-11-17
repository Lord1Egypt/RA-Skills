## Description:

Helps agents collect, normalize, and compare product pricing observations across e-commerce pages, with an included helper script for structuring already-scraped results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and e-commerce operators use this skill to guide product price extraction, normalize scraped pricing data, and compare retailers for monitoring or market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation advertises scraping, CSV, tracking, and currency-conversion capabilities that are incomplete in the included script.

Mitigation: Use it as a lightweight helper for organizing already-scraped price data and guiding manual extraction; implement and review missing capabilities before relying on them.

Risk: Price scraping can violate site terms, robots.txt, rate limits, or permission boundaries when used at scale or against restricted pages.

Mitigation: Check site terms and robots.txt before scraping, avoid login-protected or personal data sources without explicit permission, and keep request rates conservative.

## Reference(s):

- [Site-Specific Selectors](references/selectors.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/product-pricing-scraper)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance with JSON data outputs and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script structures JSON input from stdin; CSV output, price tracking, live scraping, and currency conversion require additional implementation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
