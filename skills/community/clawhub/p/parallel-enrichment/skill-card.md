## Description:

Bulk data enrichment via Parallel API. Adds web-sourced fields (CEO names, funding, contact info) to lists of companies, people, or products. Use for enriching CSV files or inline data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to enrich CSV files or inline records with web-sourced fields for company research, lead enrichment, contact lookup, funding research, and product comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private CSV data or sensitive records may be sent to an external enrichment service.

Mitigation: Submit only data that policy allows Parallel to process; avoid secrets, credentials, regulated personal data, and confidential datasets unless approved.

Risk: Enriched output files may retain sensitive or commercially useful data locally.

Mitigation: Choose output paths deliberately and manage retention, access, and cleanup according to the dataset sensitivity.

## Reference(s):

- [Parallel](https://parallel.ai)
- [Parallel API Docs](https://docs.parallel.ai)
- [Parallel Enrichment API Reference](https://docs.parallel.ai/api-reference/enrichment)
- [Parallel CLI Integration Docs](https://docs.parallel.ai/integrations/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and YAML examples for running enrichment jobs that write CSV output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The enriched CSV output retains original columns, adds requested enrichment columns, and includes a _parallel_status column for each row.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
