## Description:

解析医疗险条款文档并提取32个结构化字段，含14个核心字段和18个增强字段，支持PDF/DOCX/TXT格式，输出标准JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[long1973m](https://clawhub.ai/user/long1973m)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to parse Chinese medical insurance policy text or uploaded PDF, DOCX, and TXT files into a standardized JSON structure for comparison and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extracted insurance fields may be incomplete or incorrect for complex policy language.

Mitigation: Review the generated JSON against the original policy text before using it for decisions.

Risk: The skill processes user-provided insurance documents that may contain sensitive personal or policy information.

Mitigation: Use only documents you intentionally provide and avoid sharing generated outputs beyond the intended review workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/long1973m/skills/insurance-policy-parser)
- [保险条款结构化输出格式规范](references/output-format.md)

## Skill Output:

**Output Type(s):** [analysis, json, shell commands, guidance]

**Output Format:** [JSON with optional Markdown guidance and shell commands for document parsing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON contains level1_core_fields and level2_enhancement_fields; Level 2 values may be null when the source policy is unclear.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
