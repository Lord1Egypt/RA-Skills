## Description:

Query verified phone numbers and email addresses from LinkedIn profile URLs using the LeadContact API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhyswan](https://clawhub.ai/user/zhyswan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to enrich sales, recruiting, or CRM workflows by requesting phone numbers or email addresses for LinkedIn profile URLs through LeadContact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkedIn profile URLs and returned phone or email data are privacy-sensitive.

Mitigation: Use the skill only with authorization and a lawful basis, and protect returned contact data.

Risk: The LeadContact API token could be exposed if embedded in client-side code or logs.

Mitigation: Store LEADCONTACT_API_TOKEN securely and avoid printing or committing it.

Risk: Automated lookup workflows can exceed expected service use or policy limits.

Mitigation: Validate LinkedIn profile URLs before requests and respect the documented rate limit.

## Reference(s):

- [LeadContact homepage](https://leadcontact.ai)
- [LeadContact privacy policy](https://leadcontact.ai/zh-CN/privacy)
- [ClawHub skill page](https://clawhub.ai/zhyswan/skills/leadcontact)
- [Publisher profile](https://clawhub.ai/user/zhyswan)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LEADCONTACT_API_TOKEN; API responses may include personal phone numbers or email addresses.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
