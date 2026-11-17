## Description:

Scan and redact email addresses, Chinese mobile numbers, IP addresses, and secret fields in text, CSV, and JSON while preserving originals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and operations teams use this skill to scan files or create local redacted copies before sharing. Review every output, especially CSV files with credential columns, before external sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV copies can retain passwords and API keys even when scan reports show no matches.

Mitigation: Do not rely on CSV exports being safe to share until secret-column masking is fixed. Inspect credential columns manually and review every output; a report with no matches does not prove sensitive information was removed.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab](https://mochilab.bz)
- [Privacy Redaction Desk on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-privacy-redactor)

## Skill Output:

**Output Type(s):** [Text files, JSON files, CSV files, Scan reports]

**Output Format:** [Redacted text, JSON, or CSV files with JSON and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local copies and preserves originals; reports provide match counts and hashes, not matched values.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
