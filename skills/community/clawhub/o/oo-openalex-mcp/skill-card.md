## Description:

Use the OpenAlex MCP connector through OOMOL to search and analyze scholarly works, explore researchers and institutions, and manage author profiles and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, librarians, and research-office staff can search OpenAlex works and entities, analyze research portfolios, explore citations, and manage connected author profiles or alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installers and the hosted connector implementation has not been verified.

Mitigation: Review the CLI installation, prevent automatic execution of downloaded installers, and prefer a separately verified installation. Review the CLI's agent-skill synchronization settings.

Risk: Connected-account actions can change author profiles or delete alerts.

Mitigation: Keep user confirmation for profile changes and alert deletion.

## Reference(s):

- [OpenAlex](https://openalex.org)
- [OpenAlex connector documentation](https://help.openalex.org/access/connector/)
- [OpenAlex Query Language documentation](https://help.openalex.org/access/oql/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Research summaries and analysis, with structured JSON data where provided by OpenAlex actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected query, filters, and action.]

## Skill Version(s):

1.0.0 (source: evidence.json release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
