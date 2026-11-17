## Description:

GL importer helps agents import CSV/XLSX accounting data into QuickBooks Online or Xero through the Synder Importer REST API, including field mapping, file upload, import execution, status polling, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelastreikosynder](https://clawhub.ai/user/michaelastreikosynder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and accounting operators use this skill to prepare, validate, and run spreadsheet-based imports into connected QuickBooks Online or Xero companies through Synder. It is intended for import workflows, not reading or exporting accounting data from those systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live imports can create or modify records in connected QuickBooks Online or Xero companies.

Mitigation: Start with dryRun=true, review proposed mappings and results, and require explicit approval before any dryRun=false import.

Risk: The API token allows an agent to operate against accounting data for connected companies.

Mitigation: Use a limited, revocable token, store it only in the environment, and revoke it when the workflow is complete or no longer trusted.

Risk: Settings changes, mapping deletion, cancellation, and reversion can disrupt accounting workflows or remove imported entities.

Mitigation: Require explicit approval for these operations and verify the target company, mapping, and import identifiers before execution.

## Reference(s):

- [Synder Importer API Full Reference](references/api.md)
- [Synder Importer API Docs](https://importer.synder.com/apidocs)
- [Synder Importer](https://importer.synder.com)
- [Synder](https://synder.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash/curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMPORTER_API_TOKEN; live imports should be preceded by dryRun=true and human review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
