## Description:

Hubspot Suite helps agents manage HubSpot CRM, marketing, sales, service, CMS, automation, reporting, data quality, and import/export tasks through HubSpot API guidance and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luigi08001](https://clawhub.ai/user/luigi08001)

### License/Terms of Use:


## Use Case:

Developers, operators, and HubSpot administrators use this skill to generate HubSpot API calls, shell commands, configuration guidance, and workflow steps for CRM management, data migration, reporting, deduplication, automation, and account administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful HubSpot CRM access that can read or modify business data.

Mitigation: Use a minimally scoped HubSpot private-app token and review requested operations before running generated commands or scripts.

Risk: Unsafe script patterns could expose tokens or change HubSpot data unexpectedly.

Mitigation: Avoid overriding HUBSPOT_BASE_URL except to the official HubSpot API, do not pass untrusted object or property names to scripts, and run mutating actions only after a backup or dry run.

## Reference(s):

- [HubSpot Authentication Setup](references/auth-setup.md)
- [HubSpot Contacts API](references/crm-contacts.md)
- [HubSpot Companies API](references/crm-companies.md)
- [HubSpot Deals API](references/crm-deals.md)
- [HubSpot Tickets API](references/crm-tickets.md)
- [HubSpot Associations API](references/associations.md)
- [HubSpot Properties API](references/properties.md)
- [HubSpot Engagements API](references/engagements.md)
- [HubSpot Workflows & Automation](references/workflows.md)
- [HubSpot Import & Export Operations](references/import-export.md)
- [HubSpot Data Quality & Deduplication](references/data-quality.md)
- [HubSpot Rate Limits & Best Practices](references/rate-limits.md)
- [HubSpot Search Operators & Filter Syntax](references/search-filters.md)
- [HubSpot Knowledge Base Tips](references/knowledge-base-tips.md)
- [Hubspot Suite ClawHub listing](https://clawhub.ai/luigi08001/skills/hubspot-suite)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HubSpot access token for live API operations; generated commands should be reviewed before execution.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
