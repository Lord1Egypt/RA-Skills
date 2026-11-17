## Description:

Enrich LinkedIn profile URLs with mobile phone numbers and work or personal emails using Apify actors, then merge results into unified output records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, sales operations teams, and agencies use this skill to enrich LinkedIn profile URL lists with email and mobile phone data for prospecting, CRM preparation, spreadsheets, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends LinkedIn profile lists to Apify actors and enriches people with email and mobile phone data.

Mitigation: Use it only with a lawful basis for contact enrichment, review applicable privacy obligations, and start with small URL batches.

Risk: The Apify credential can be exposed if passed directly in shell commands.

Mitigation: Prefer APIFY_TOKEN from a protected environment or secret manager, avoid --apify-token in shell history, and use a least-privilege Apify token when available.

Risk: Inputs may require additional validation before enrichment.

Mitigation: Validate that all submitted URLs are intended LinkedIn profile URLs before running the skill.

## Reference(s):

- [Input contract](artifact/references/input-contract.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Sample input](artifact/references/sample_input.json)
- [Apify phone actor X95BXRaFOqZ7rzjxM](https://console.apify.com/actors/X95BXRaFOqZ7rzjxM)
- [Apify email actor q3wko0Sbx6ZAAB2xf](https://console.apify.com/actors/q3wko0Sbx6ZAAB2xf)
- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/linkedin-email-phone-apify)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON records with concise Markdown command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Merged rows include LinkedIn URL, identity fields, company or title fields, work email, personal emails, mobile phone, and email or phone presence flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
