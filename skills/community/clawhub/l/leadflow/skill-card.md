## Description:

Turn any city into a lead list in 60 seconds by scraping Google Maps and Yelp, enriching and verifying contacts, scoring lead quality, and exporting CRM-ready results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkocaj](https://clawhub.ai/user/lkocaj)

### License/Terms of Use:

MIT

## Use Case:

Sales teams, marketing agencies, service businesses, freelancers, and consultants use LeadFlow to collect local business leads, enrich contact details, verify reachable contacts, score lead quality, and export lists for CRM or outreach workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI fetches websites discovered from business listings, which can expose the user's network to untrusted sites.

Mitigation: Run the workflow in a network-restricted environment when possible and limit scraping to trusted use cases and expected geographies.

Risk: Lead data and API-provider responses are stored locally and may contain personal or business contact information.

Mitigation: Store output in controlled locations, protect local databases and exports, and delete data that is no longer needed.

Risk: Generated spreadsheet files may contain untrusted fields from external sources.

Mitigation: Treat generated CSV and XLSX files as untrusted and review them before opening in spreadsheet software or importing into business systems.

Risk: Webhook delivery can send selected lead data to a user-provided URL.

Mitigation: Use only approved webhook endpoints and verify filters, batch size, and destination ownership before sending data.

Risk: The workflow uses several external data providers with user-supplied API keys.

Mitigation: Use limited-scope API keys, monitor provider usage, and avoid debug logging that could expose proxy credentials or sensitive configuration.

## Reference(s):

- [LeadFlow ClawHub page](https://clawhub.ai/lkocaj/skills/leadflow)
- [LeadFlow npm package](https://www.npmjs.com/package/leadflow)
- [OnCall Automation](https://oncallautomation.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown instructions with bash command examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can create local SQLite data and CSV, XLSX, CRM import, or webhook outputs depending on user-selected workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
