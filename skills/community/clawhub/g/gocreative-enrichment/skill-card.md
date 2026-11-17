## Description:

Lead enrichment, company enrichment, work-email finder, and email validation for AI agents, including company firmographics, domain/DNS/WHOIS intelligence, and LinkedIn/GitHub profile data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, and agent developers use this skill to enrich leads and companies, find or validate work emails, and research domains before outreach or qualification. It is suited for workflows that can send target prospect or company data to GoCreative and approve pay-per-call x402 payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send personal contact, prospect, employee, or customer data to a third-party API.

Mitigation: Use it only for an approved business purpose and confirm that the workflow is allowed to send the target data to GoCreative.

Risk: The skill can auto-pay per request through x402 using USDC.

Mitigation: Place wallet spend limits or require manual approval around x402 payments before using it in live workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/gocreative-enrichment)
- [GoCreative API provider endpoint](https://api.gocreativeai.com)
- [Company enrichment endpoint](https://api.gocreativeai.com/v1/enrich/company/{domain})
- [Email finder endpoint](https://api.gocreativeai.com/v1/enrich/email/{name-and-domain})
- [Email 360 endpoint](https://api.gocreativeai.com/v1/bundle/email-360/{email})
- [Domain enrichment endpoint](https://api.gocreativeai.com/v1/enrich/domain/{domain})
- [LinkedIn enrichment endpoint](https://api.gocreativeai.com/v1/enrich/linkedin/{profile})
- [Company 360 endpoint](https://api.gocreativeai.com/v1/bundle/company-360/{domain})

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTPS GET examples and JSON API responses from GoCreative endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires URL-encoded endpoint arguments and x402 USDC payment handling for paid requests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
