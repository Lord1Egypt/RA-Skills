## Description:

Provides offline ClickHouse SQL syntax and MRS specification checks for versions 24.8, 23.3, and 22.3, producing Markdown reports with detected issues and fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to review ClickHouse SQL before execution, checking syntax compatibility and MRS development-specification rules without connecting to a cluster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advisory SQL analysis can be incomplete or misleading because the security summary notes overstated coverage claims and cautions against relying on it as a complete ClickHouse parser.

Mitigation: Use findings as review support and verify SQL behavior against the target ClickHouse version and cluster before acting.

Risk: Reports may echo the original SQL, which could expose secrets pasted into SQL examples.

Mitigation: Do not paste credentials, tokens, or sensitive production data into SQL submitted for checking.

Risk: Guidance involving DROP, DELETE, BACKUP, or RESTORE statements could affect production data if executed without review.

Mitigation: Treat such guidance as review-only and independently verify operational SQL before execution.

## Reference(s):

- [ClickHouse SELECT Grammar Reference](references/select_grammar.md)
- [ClickHouse DDL Grammar Reference](references/ddl_grammar.md)
- [ClickHouse DML and Misc Grammar Reference](references/dml_misc_grammar.md)
- [ClickHouse Token Types Reference](references/token_types.md)
- [ClickHouse SQL Check Report Template](templates/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with violation, summary, and fix-suggestion tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static local analysis; reports may include the original SQL text supplied by the user.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
