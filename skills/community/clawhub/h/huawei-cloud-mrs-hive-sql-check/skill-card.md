## Description:

Checks Huawei Cloud MRS Hive SQL statements against defined syntax, specification, and large-SQL interception rules using a bundled automated checker engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to run local static checks on Huawei Cloud MRS Hive SQL before execution or review. It reports only checker-detected syntax, specification, and large-SQL interception findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include original SQL text or SQL snippets.

Mitigation: Run the checker only on SQL that may be shared with the agent and review generated reports before redistribution.

Risk: Rule names, report labels, and remediation text may appear in Chinese.

Mitigation: Have reviewers confirm localized findings and remediation wording before acting on the report.

Risk: Documentation may contain minor mismatches in listed defaults or rule counts.

Mitigation: Use the bundled checker output as the source of truth for actual findings and selected mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-hive-sql-check)
- [AST Schema](references/ast-schema.md)
- [Syntax Rules](rules/syntax_rules.yaml)
- [Specification Rules](rules/spec_rules.yaml)
- [Performance Rules](rules/perf_rules.yaml)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report or JSON checker output with rule identifiers, levels, positions, snippets, and fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes SQL text locally; reports may include the original SQL and snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
