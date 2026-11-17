## Description:

Ora地图拓客专家 helps agents search for localized business leads by city and product or industry keyword, returning commercial listings with company names, addresses, websites, phone numbers, emails, and social accounts when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oraagent](https://clawhub.ai/user/oraagent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business development teams use this skill to search for local business prospects by city and keyword, then review returned contact and web presence details for outreach planning. It is intended for one city and one keyword per search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search keywords, coordinates, and any local OraAgent.key credential to a third-party API.

Mitigation: Install only after confirming the third-party API and credential handling are acceptable for the intended environment.

Risk: Returned phone numbers, emails, social accounts, and business records may be regulated or sensitive contact data.

Mitigation: Handle saved result files according to applicable privacy, retention, and outreach compliance requirements.

Risk: A quota error directs users to a payment page.

Mitigation: Verify the recharge page independently before entering payment or account information.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oraagent/skills/ora-map-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/oraagent)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown response summarizing JSON business-search results and saved raw data file details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One city and one keyword per request; results may include business names, addresses, websites, phone numbers, emails, and social accounts.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
