## Description:

Export Google Maps business data to CSV, JSON, or CRM format (HubSpot, Pipedrive, Salesforce). Bulk export with custom field mapping and filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmapsscraper](https://clawhub.ai/user/gmapsscraper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to define, confirm, export, filter, and transform Google Maps business listings for spreadsheets, JSON workflows, or CRM imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied category or location text can make copied shell snippets unsafe if it is inserted without sanitization.

Mitigation: Validate inputs and safely quote or encode search text before constructing requests; review generated commands before execution.

Risk: Business contact data and search terms are sent to and downloaded from gmapsscraper.io.

Mitigation: Use only data you are allowed to export and process, protect and rotate the API key if exposed, and delete downloaded exports when no longer needed.

## Reference(s):

- [gmapsscraper.io](https://gmapsscraper.io)
- [Google Maps Export on ClawHub](https://clawhub.ai/gmapsscraper/skills/google-maps-export)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash, Python, and CRM field-mapping examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV or JSON export files after the user runs the guided API workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
