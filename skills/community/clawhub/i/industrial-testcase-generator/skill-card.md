## Description:

Generates standardized, traceable Excel test cases for industrial automation monitoring systems such as PLC, SCADA, and HMI from requirements documents or descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and industrial automation teams use this skill to turn PLC, SCADA, HMI, communications, alarm, safety, reliability, and compliance requirements into structured test cases and coverage evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Industrial requirement documents may contain sensitive operational, safety, or network details.

Mitigation: Handle input documents and generated workbooks under the organization's data-handling rules, and redact unnecessary sensitive details before use in shared agent environments.

Risk: Generated test cases may include inferred implicit requirements or default standards when source requirements are incomplete.

Mitigation: Have qualified industrial QA, safety, or compliance reviewers verify assumptions, standards mappings, and acceptance criteria before using outputs for certification, commissioning, or safety decisions.

Risk: Excel workbooks may look complete even when upstream requirements are ambiguous or underspecified.

Mitigation: Treat generated coverage statistics as review aids and reconcile them against the authoritative requirement set before importing test cases into a management platform.

## Reference(s):

- [Skill README](artifact/README.md)
- [Industrial Domain Knowledge](artifact/references/domain-knowledge.md)
- [Industrial Test Case Format Specification](artifact/references/format-spec.md)
- [Example Requirements](artifact/examples/requirements.md)
- [ClawHub Skill Page](https://clawhub.ai/kokxi/skills/industrial-testcase-generator)
- [Agent Skills](https://agentskills.io)
- [Agent Skills Reference Validator](https://github.com/agentskills/agentskills/tree/main/skills-ref)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [Excel workbook (.xlsx) with a 15-column test-case sheet and coverage statistics sheet; intermediate outputs may be structured JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and openpyxl to generate the workbook.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
