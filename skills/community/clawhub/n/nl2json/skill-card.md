## Description:

将中文自然语言请求转换为符合模板字段的结构化 JSON 参数，并支持时间格式归一化和短后续请求的上下文继承。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingjiusheng](https://clawhub.ai/user/yingjiusheng)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to turn Chinese data, news, public-opinion, or search requests into a consistent JSON object based on templates/default.json. It is intended for structured parameter extraction where missing template fields should still be represented with defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may route general JSON-conversion requests through this skill.

Mitigation: Use it when a fixed JSON parameter object is desired, and verify that the selected template matches the user's task.

Risk: Short follow-up requests may inherit fields from a previous conversion.

Mitigation: Ask for a fresh conversion or provide all relevant fields when prior context should not be reused.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs preserve the template fields input, question_name, and other; time values are normalized to YYYY-mm-dd H:i:s when present.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
