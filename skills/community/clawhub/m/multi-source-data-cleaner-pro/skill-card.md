## Description: <br>
Production-grade data cleaning across heterogeneous sources such as CSV, Excel, JSON, Parquet, SQL dumps, and log files, with profiling, type normalization, missing-value handling, fuzzy deduplication, schema reconciliation, PII handling, and data-quality reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and analysts use this skill to clean, merge, deduplicate, and profile messy tabular datasets from multiple local sources while preserving audit outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local datasets selected by the user and writes cleaned files, profiles, and audit reports that may contain sensitive customer, employee, medical, financial, or regulated data. <br>
Mitigation: Use a protected output directory, restrict access to audit/profile files, and handle generated reports as sensitive artifacts. <br>
Risk: The security summary notes that unmasked sensitive sample data may be saved in audit or profile outputs despite advertised PII masking. <br>
Mitigation: Avoid the pii-policy keep setting unless explicitly authorized, review audit/profile outputs before sharing, and prefer mask or drop for sensitive columns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/boboy-j/multi-source-data-cleaner-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/boboy-j) <br>
- [Project Homepage](https://github.com/openclaw-skills/multi-source-data-cleaner) <br>
- [PII Pattern Hints](knowledge/pii_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON, CSV, Markdown, or cleaned dataset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cleaned datasets, data-quality reports, deduplication groups, schema mappings, audit logs, and row-level provenance files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
