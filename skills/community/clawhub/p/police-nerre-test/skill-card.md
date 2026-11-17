## Description:

公安警情文本实体关系抽取工具，从警情文本中精准抽取指定实体与关系，输出严格结构化JSON，无任何多余内容

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy020326](https://clawhub.ai/user/andy020326)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized users processing Chinese police-incident text use this skill to extract predefined entities and relationships into a fixed JSON structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface highly sensitive personal data from police-incident text in structured JSON.

Mitigation: Install and use it only in approved workflows where the user is authorized to process the provided incident text.

Risk: Structured extraction can make personal identifiers and sensitive relationships easier to retain or share.

Mitigation: Avoid pasting data that should not be processed or retained by the agent environment, and review outputs before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andy020326/skills/police-nerre-test)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Strict JSON object containing Chinese entity arrays and relationship triples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to output only JSON, with no Markdown, commentary, or extra text.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
