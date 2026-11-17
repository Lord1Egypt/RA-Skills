## Description:

HiFleet supports vessel position, profile, voyage, casualty, sanction, maritime penalty, PSC, port, public tonnage, liner schedule, fleet, weather, and AIS workflows for maritime queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleiwang](https://clawhub.ai/user/charleiwang)

### License/Terms of Use:

MIT-0

## Use Case:

External maritime users and developers use this skill to query HiFleet vessel position and related maritime data through authenticated HiFleet API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles HiFleet API keys and account setup workflows.

Mitigation: Store API keys in environment variables, avoid pasting full keys into chat, and rotate any exposed key.

Risk: Payment, subscription, invoice, contact retrieval, and console SSO actions can affect accounts or expose sensitive links.

Mitigation: Require explicit user confirmation before orders, subscription changes, invoices, refunds, contact retrieval for many rows, or console SSO links.

Risk: The security evidence flags insecure endpoint and install practices, including an HTTP ZIP install path.

Mitigation: Prefer the ClawHub release or trusted source links and avoid installing from the HTTP ZIP path.

Risk: The API base can be overridden.

Mitigation: Set API base variables only to trusted HiFleet HTTPS hosts.

## Reference(s):

- [HiFleet Skills Homepage](https://skills.hifleet.com)
- [ClawHub Skill Page](https://clawhub.ai/charleiwang/skills/hifleet-skills)
- [Security](SECURITY.md)
- [First Setup](FIRST_SETUP.md)
- [Position API](references/position_api.md)
- [API Base URL](references/api_base.md)
- [Billing API](references/billing_api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HIFLEET_API_KEY for authenticated HiFleet APIs.]

## Skill Version(s):

0.3.21 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
