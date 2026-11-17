## Description:

Searches Seerfar marketplace keyword data for Ozon and available Wildberries rows, filtering by search volume, growth, product and seller counts, price, sales, conversion concentration, and related market metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace analysts, cross-border e-commerce operators, and developers use this skill to discover and rank Ozon search terms, identify low-competition or high-demand keyword opportunities, and retrieve market profile metrics for selected periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles marketplace API keys, account identifiers, and optional phone/SMS onboarding data.

Mitigation: Use only trusted LinkFox HTTPS endpoints, keep generated API keys out of transcripts and shell history, and rotate credentials if exposed.

Risk: Onboarding can create paid orders or display payment QR codes and payment URLs.

Mitigation: Run billing or order commands only after explicit user consent, and verify the plan, payment method, and amount before payment.

Risk: Marketplace queries consume LinkFox credits and may incur cost.

Mitigation: Confirm intent before repeated calls, use precise filters and sorting, and rely on the default cache to avoid duplicate paid queries.

Risk: Full API responses are saved locally and may contain commercially sensitive market research data.

Mitigation: Store outputs in an appropriate workspace, limit sharing of saved response files, and delete session data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-seerfar-ozon-market-keyword-search)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON result files plus stdout JSON or concise text summaries with onboarding commands when authentication or billing setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses under a LinkFox session data directory; responses over 8 KB are summarized unless inline output is requested; a 24-hour local cache is used by default.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
