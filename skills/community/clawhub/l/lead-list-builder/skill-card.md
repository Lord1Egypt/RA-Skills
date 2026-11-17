## Description:

Operate as a Lead List Building Agent - an autonomous agent that discovers businesses with outdated or broken websites, audits each site, enriches contact information, scores every lead, and writes results to a Google Sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

External sales, marketing, and agency operators use this skill to find local businesses with outdated or broken websites, enrich contact details, score sales opportunities, and deliver a prioritized Google Sheet for outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and Google service account credentials are required for the workflow.

Mitigation: Store credentials outside source control, use a dedicated environment, and restrict the Google service account to the intended sheet.

Risk: The workflow collects and uses business contact data for lead generation.

Mitigation: Confirm that collection, storage, and outreach practices comply with applicable privacy and anti-spam requirements before use.

Risk: The skill depends on third-party Python packages and external data services.

Mitigation: Review and pin dependencies before installation and monitor API service terms, quotas, and access permissions.

## Reference(s):

- [Lead List Builder Agent on ClawHub](https://clawhub.ai/maverick-software/skills/lead-list-builder)
- [maverick-software Publisher Profile](https://clawhub.ai/user/maverick-software)
- [Lead List Builder Setup Guide](references/setup-guide.md)
- [Search Query Library](references/query-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, Google Sheets lead records, setup commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires search, PageSpeed, optional contact-enrichment API credentials, and Google Sheets service account configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
