## Description: <br>
HubSpot Suite helps agents manage HubSpot CRM, marketing, sales, service, CMS, automation, data quality, import/export, reporting, and administration through HubSpot API guidance and shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Luigi08001](https://clawhub.ai/user/Luigi08001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
HubSpot administrators, RevOps teams, CRM operators, and developers use this skill to generate HubSpot API requests, shell commands, and workflow guidance for CRM records, associations, imports/exports, reporting, automation, and data quality tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or run broad HubSpot CRM and automation actions, including imports, exports, merges, deletes, workflow changes, schema changes, and bulk updates. <br>
Mitigation: Use a dedicated least-privilege HubSpot token, prefer read-only scopes for reporting, test in a sandbox first, and require manual approval before any bulk or destructive operation. <br>
Risk: HubSpot customer data and credentials can be exposed through exports, local files, CLI-authenticated sessions, .env files, or verbose debugging. <br>
Mitigation: Protect tokens and generated files, avoid DEBUG=1 with real customer data, and restrict access to any environment or CLI credential stores used by the scripts. <br>
Risk: Bulk imports, merges, and data-cleanup workflows can change customer records at scale if inputs or match criteria are wrong. <br>
Mitigation: Validate CSV inputs and filters, use dry-run or read-only checks where available, keep backups or exports before changes, and review merge and update targets manually. <br>


## Reference(s): <br>
- [HubSpot Authentication Setup](references/auth-setup.md) <br>
- [HubSpot Contacts API](references/crm-contacts.md) <br>
- [HubSpot Companies API](references/crm-companies.md) <br>
- [HubSpot Deals API](references/crm-deals.md) <br>
- [HubSpot Tickets API](references/crm-tickets.md) <br>
- [HubSpot Associations API](references/associations.md) <br>
- [HubSpot Properties API](references/properties.md) <br>
- [HubSpot Engagements API](references/engagements.md) <br>
- [HubSpot Workflows & Automation](references/workflows.md) <br>
- [HubSpot Import & Export Operations](references/import-export.md) <br>
- [HubSpot Data Quality & Deduplication](references/data-quality.md) <br>
- [HubSpot Search Operators & Filter Syntax](references/search-filters.md) <br>
- [HubSpot Rate Limits & Best Practices](references/rate-limits.md) <br>
- [HubSpot Knowledge Base Tips](references/knowledge-base-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline bash, curl, JSON, and shell script examples; helper scripts may produce CSV, JSON, or text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HubSpot access token for live API operations.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
