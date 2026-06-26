## Description: <br>
将中文自然语言查询转换为符合 templates/default.json 结构的 JSON 参数，并支持在连续请求中继承和更新上下文。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingjiusheng](https://clawhub.ai/user/yingjiusheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to convert Chinese natural-language data, news, and public-opinion queries into structured JSON parameters for downstream tools or workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Context reuse can carry prior query parameters into a short follow-up that belongs to a different task. <br>
Mitigation: Review generated JSON before downstream use and start a fresh request when changing topics. <br>
Risk: Generated JSON may contain incorrect extracted fields or dates from ambiguous natural-language input. <br>
Mitigation: Validate parsed fields, especially dates, sources, quantities, and sensitive-topic parameters, before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yingjiusheng/nl2json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration] <br>
**Output Format:** [JSON matching the configured template fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes input, question_name, and an other object; missing template fields are filled with default empty values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
