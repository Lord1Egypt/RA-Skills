## Description:

Production-grade data cleaning for heterogeneous CSV, Excel, JSON, Parquet, SQL dump, and log sources, with profiling, type normalization, fuzzy deduplication, schema reconciliation, PII handling, and data-quality reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to clean, merge, deduplicate, normalize, and audit one or more dirty datasets before analysis, reporting, or batch ETL workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan says the privacy and data-integrity safeguards are weaker than the documentation claims.

Mitigation: Review the privacy and deduplication limitations before installation or use, and validate outputs before relying on cleaned data.

Risk: Generated cleaned data, profiles, audit files, and reports may contain sensitive source-data values or partially masked PII.

Mitigation: Treat all generated outputs as sensitive, store them with the same controls as the source data, and do not rely on mask or drop behavior as complete PII removal.

Risk: Fuzzy deduplication can remove or merge records incorrectly.

Mitigation: Keep original data backups and review deduplication summaries before using the cleaned dataset downstream.

## Reference(s):

- [README](README.md)
- [PII Pattern Hints](knowledge/pii_patterns.md)
- [Examples](examples/README.md)
- [Project homepage from ClawHub metadata](https://github.com/openclaw-skills/multi-source-data-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown data-quality artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce cleaned dataset files, audit logs, per-source profiles, deduplication summaries, and data-quality reports in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
