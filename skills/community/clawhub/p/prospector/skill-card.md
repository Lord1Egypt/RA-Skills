## Description:

Prospector helps users find leads, prospects, or contacts matching an ideal customer profile by searching companies with Exa, enriching contacts with Apollo, exporting CSV results, and optionally syncing to Attio CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slempiam](https://clawhub.ai/user/slempiam)

### License/Terms of Use:

MIT

## Use Case:

Sales, growth, and developer users use Prospector to define an ICP, discover matching companies, enrich contacts, export lead lists, and optionally sync those records to Attio CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may write API keys into shell startup files or local configuration, increasing exposure and persistence risk.

Mitigation: Use environment variables or a secret manager, avoid shell-profile writes, and use API keys generated specifically for this workflow.

Risk: Lead CSV exports and optional CRM sync may contain sensitive company and contact data.

Mitigation: Treat exported CSVs as sensitive, restrict access, and confirm authorization before sending or retaining contacts in Attio.

Risk: Untrusted lead data may be opened in spreadsheets where formula-like values can execute spreadsheet functions.

Mitigation: Neutralize CSV formulas before opening, importing, or sharing exported lead files.

Risk: Dependency and shell export handling may be less reproducible or robust without pinned packages and safe quoting.

Mitigation: Pin dependencies, quote shell exports safely, and review setup changes before execution.

## Reference(s):

- [Prospector ClawHub skill page](https://clawhub.ai/slempiam/skills/prospector)
- [Exa](https://exa.ai)
- [Apollo](https://apollo.io)
- [Attio](https://attio.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, CSV files]

**Output Format:** [Markdown guidance with inline shell and Python commands, status text, and CSV lead exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV exports include company and contact fields; optional Attio sync creates or updates CRM company and people records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
