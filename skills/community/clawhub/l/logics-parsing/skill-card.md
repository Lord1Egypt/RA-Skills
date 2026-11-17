## Description:

阿里文档智能解析工具 - 将PDF/图片转结构化HTML。支持复杂布局、公式识别、化学结构、代码块、流程图、乐谱等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to guide setup and use of Alibaba Logics-Parsing for converting PDFs and document images into structured HTML or JSON. It is suited to academic, scientific, and business document extraction workflows that involve formulas, tables, chemical structures, code blocks, flowcharts, sheet music, or complex layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can run mutable third-party code and dependencies.

Mitigation: Use a pinned, reviewed Logics-Parsing commit with locked dependency versions, and avoid elevated privileges during setup.

Risk: The skill may be used on confidential contracts, invoices, financial reports, or regulated documents.

Mitigation: Process sensitive documents only in an approved isolated environment with clear output-retention rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smseow001/skills/logics-parsing)
- [Logics-Parsing repository referenced in install commands](https://github.com/alibaba/Logics-Parsing)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, HTML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup commands and document parsing output examples; review execution and data-handling context before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
