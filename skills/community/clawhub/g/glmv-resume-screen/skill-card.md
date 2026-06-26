## Description: <br>
Screen and evaluate resumes against criteria using the ZhiPu GLM-V multimodal model, reading resume files and returning pass/fail analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and agents assisting them use this skill to batch-screen candidate resumes against role-specific criteria and compare pass/fail reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume contents, screening criteria, and local PDF page images are sent to Zhipu's external GLM-V API. <br>
Mitigation: Use the skill only when policy permits sending candidate data to Zhipu, minimize unnecessary personal data in inputs, and review provider data-handling terms for the use case. <br>
Risk: The skill requires a ZHIPU_API_KEY credential. <br>
Mitigation: Use a dedicated API key where possible, store it in approved environment or OpenClaw configuration, and rotate or revoke it if exposed. <br>
Risk: Saved Markdown or JSON outputs can contain candidate evaluation details. <br>
Mitigation: Save outputs only to locations approved for candidate data and apply normal access controls and retention rules. <br>


## Reference(s): <br>
- [GLM-V Resume Screen skill homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-resume-screen) <br>
- [Zhipu chat completions API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) <br>
- [Zhipu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, guidance] <br>
**Output Format:** [Markdown table by default; optional Markdown or JSON file when an output path is provided.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes success status, model result, usage metadata, screening criteria, and file count.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
