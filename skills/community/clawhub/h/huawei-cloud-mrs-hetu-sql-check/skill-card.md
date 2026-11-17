## Description:

Checks HetuEngine SQL for syntax compatibility, statement structure, clause completeness, and specification issues using a local tokenizer, parser, and rule engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to review HetuEngine SQL before execution, validate syntax, and identify specification or performance-related rule violations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL or file inputs may contain sensitive information even though the skill runs local static analysis.

Mitigation: Review SQL and file inputs before running the checker, and avoid passing sensitive non-SQL files.

Risk: Security evidence notes that some documented checks are partial and results should be treated as advisory.

Mitigation: Use the report as review guidance and confirm important findings against HetuEngine behavior before deployment or execution.

Risk: Reports and rule text are largely Chinese, which may affect reviewers who do not read Chinese.

Mitigation: Have bilingual reviewers inspect high-impact findings or translate reports before making production decisions.

## Reference(s):

- [AST Schema](references/ast_schema.md)
- [Syntax Rules](rules/syntax_rules.yaml)
- [Specification Rules](rules/spec_rules.yaml)
- [Keywords](rules/keywords.py)
- [Grammar Rules](rules/grammar_rules.py)
- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-hetu-sql-check)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports or JSON-style CLI output with rule violations, severity, location, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes inline SQL text or local SQL files; check mode can be syntax, spec, or all.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
