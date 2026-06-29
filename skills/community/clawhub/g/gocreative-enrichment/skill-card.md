## Description: <br>
Provides company and lead enrichment, work-email discovery and validation, firmographics, domain/DNS/WHOIS intelligence, and LinkedIn/GitHub profile data through GoCreative pay-per-call API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to enrich companies and leads, find or validate work email addresses, and research domains before sales, prospecting, or compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may send domains, names, email addresses, and profile identifiers to GoCreative for enrichment. <br>
Mitigation: Use the skill only for leads or companies you are authorized to process, and avoid sensitive customer or employee data unless privacy and compliance requirements allow it. <br>
Risk: API calls may trigger small USDC pay-per-call charges through x402. <br>
Mitigation: Confirm wallet policy, expected prices, and payment approval behavior before enabling the skill in automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/colinhughes2121/gocreative-enrichment) <br>
- [GoCreative API](https://api.gocreativeai.com) <br>
- [Company enrichment endpoint](https://api.gocreativeai.com/v1/enrich/company/{domain}) <br>
- [Email validation endpoint](https://api.gocreativeai.com/v1/bundle/email-360/{email}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTPS GET endpoint examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires URL-encoded inputs and may trigger x402 USDC pay-per-call charges.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
