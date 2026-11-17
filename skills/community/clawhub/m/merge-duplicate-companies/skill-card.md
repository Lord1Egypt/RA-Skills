## Description:

Identify duplicate company records by domain and name, export audit CSVs for review, and guide merging; API access is used for discovery, while HubSpot company merges are handled through third-party tools or manual UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to audit duplicate HubSpot company records, produce CSV review files, and plan safe manual or tool-assisted merges. It is intended for CRM data hygiene workflows where merges must be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HubSpot company merges are irreversible and may discard conflicting property values from the non-primary record.

Mitigation: Review generated audit CSVs and choose the primary record manually before each merge.

Risk: Generated CSVs can contain CRM company identifiers and business relationship metadata.

Mitigation: Store CSV exports in a trusted workspace and keep them out of shared folders and repositories.

Risk: An over-scoped HubSpot token increases blast radius if the local environment is compromised.

Mitigation: Use a private app token limited to the crm.objects.companies.read scope for discovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/merge-duplicate-companies)
- [HubSpot CRM API endpoint](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks plus CSV audit file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local duplicate-company audit CSVs and human-facing merge guidance; it does not perform automatic HubSpot merges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
