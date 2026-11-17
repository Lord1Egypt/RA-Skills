## Description:

Generate B2B leads from Google Maps using a self-hosted MCP server (`google-maps`) and export to CSV or XLSX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realowg](https://clawhub.ai/user/realowg)

### License/Terms of Use:


## Use Case:

External users, developers, and sales operations teams use this skill to run repeatable Google Maps lead-generation batches by geography and industry, enrich results with contact fields, deduplicate listings, and export lead files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV or XLSX exports may contain formula-like values from untrusted Google Maps listings.

Mitigation: Sanitize spreadsheet cells before opening exports, and use spreadsheet clients with external-content and legacy macro features disabled.

Risk: Lead files may contain sensitive business contact data and may be sent through chat delivery channels.

Mitigation: Review generated files before sharing them and ask for confirmation before sending lead exports through chat.

Risk: The workflow requires a Google Maps API key and may generate paid API usage.

Mitigation: Keep API keys out of commits and report an estimated run cost before batch execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Concise Markdown guidance plus CSV or XLSX lead exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports include name, address, phone, website, email, rating, place_id, and Google Maps URL; summaries include count and contact coverage.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
