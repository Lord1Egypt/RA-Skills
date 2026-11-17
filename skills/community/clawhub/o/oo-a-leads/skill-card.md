## Description:

A-Leads (a-leads.co). Use this skill for ANY A-Leads request — searching and reading data. Whenever a task involves A-Leads, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use the skill to find business or personal email addresses, find phone numbers, and check email deliverability through an A-Leads account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and add agent skills without clearly disclosing those effects.

Mitigation: Review the CLI installation separately, use a reviewed version, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Contact identifiers submitted to A-Leads may be processed, and use may incur charges.

Mitigation: Submit only contact identifiers intended for processing and check usage charges.

## Reference(s):

- [A-Leads](https://a-leads.co)
- [A-Leads API documentation](https://docs.a-leads.co/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action payloads and returned data, with Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by selected A-Leads action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
