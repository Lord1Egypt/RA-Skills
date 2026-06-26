## Description: <br>
健康管理基于用户提交的体检、化验和检查报告等个人医疗数据，通过外部医疗模型评估常见疾病风险并生成个性化健康干预报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lantian888](https://clawhub.ai/user/lantian888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to collect structured health history, medication, and lab-report information, send it for risk assessment, and receive the returned health report without summarization. It can also generate an optional HTML health risk report from assessment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects sensitive medical details and may send broad conversation history to external services. <br>
Mitigation: Obtain explicit user consent, disclose external processing, and transmit only the minimum health data needed for the assessment. <br>
Risk: Credentials or token-fetching behavior may expose access to external services. <br>
Mitigation: Remove exposed credentials from artifacts and use a managed secret store with rotation and least-privilege access. <br>
Risk: Generated health reports may contain sensitive personal information in local files. <br>
Mitigation: Avoid patient names in filenames, store reports securely, and sanitize report content before rendering. <br>


## Reference(s): <br>
- [API documentation](artifact/references/api_docs.md) <br>
- [ClawHub skill page](https://clawhub.ai/lantian888/jiankangguanli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown responses with optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams model output, preserves returned formatting, and may write sensitive local report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
