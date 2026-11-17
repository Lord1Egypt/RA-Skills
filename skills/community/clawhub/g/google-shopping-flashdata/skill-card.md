## Description:

Search Google Shopping with FlashData for products, merchant names, prices and product links. Use for product discovery, comparing listed offers and collecting product-price data by market. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping researchers can search Google Shopping by product, category, and market to collect listed products, merchant names, prices, and links for offer comparisons or further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted FlashData service receives the API key and submitted query arguments, and queries spend paid FlashData Credits.

Mitigation: Keep the API key in protected secret configuration and review submitted query content and the expected credit use before making requests.

Risk: The security analysis was partial, so its benign verdict does not establish that all risks were assessed.

Mitigation: Review the skill and its dependencies before deployment, and reassess if the source or execution behavior changes.

## Reference(s):

- [FlashData Google Shopping documentation](https://flashdata.dev/docs/sources/google_shopping?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_shopping-task)
- [FlashData API key signup](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_shopping-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_shopping-task)
- [FlashData hosted MCP endpoint](https://flashdata.dev/mcp?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_shopping-task)
- [ClawHub release page](https://clawhub.ai/flashdatadev/skills/google-shopping-flashdata)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON product listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned listings and result counts vary by query and market; listed prices may not include shipping, availability, or checkout price.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
