## Description:

Finds a LinkedIn profile URL for an Odoo contact using their name and company, then saves it to the x_linkedin_url field in Odoo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernhmueller](https://clawhub.ai/user/bernhmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to look up a LinkedIn profile for a selected Odoo contact and update that contact's custom LinkedIn URL field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact names and company names are sent to DuckDuckGo during profile lookup.

Mitigation: Use only where third-party search processing is acceptable for CRM contact data.

Risk: An unverified search result can be written to the Odoo x_linkedin_url field.

Mitigation: Review the found LinkedIn URL before relying on the updated CRM record.

Risk: The script uses Odoo credentials and can update contact records.

Mitigation: Run with least-privilege Odoo credentials and avoid unchanged use in environments with strict CRM data integrity requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and execution status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Odoo credential environment variables, queries DuckDuckGo, and writes the selected result to Odoo.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
