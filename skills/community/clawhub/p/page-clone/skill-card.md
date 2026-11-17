## Description:

从用户提供的页面截图和描述中精准识别页面结构、布局尺寸、全量数据内容，输出结构化的页面复刻规格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[15926863020](https://clawhub.ai/user/15926863020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to analyze screenshots and user descriptions before recreating a page. It produces a structured replication specification covering layout, controls, buttons, field definitions, and visible text for user review before code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots may contain credentials, private customer or employee data, financial or account records, internal URLs, or confidential case details that the skill is designed to copy verbatim into its output.

Mitigation: Use only screenshots whose visible values are intentionally meant to be reproduced, or redact sensitive values before invoking the skill.

Risk: The generated page specification may preserve private visible text exactly as shown.

Mitigation: Review the specification before using it for implementation, sharing, or storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15926863020/skills/page-clone)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown specification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output is intended for user confirmation before any coding phase.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
