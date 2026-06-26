## Description: <br>
Writes Markdown content from provided PDF or DOCX documents and user requirements using the ZhiPu GLM-V multimodal model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to draft articles, reports, briefs, proposals, reviews, and similar Markdown content from selected documents and writing requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected document URLs or local PDF page contents and writing requirements are sent to Zhipu for processing. <br>
Mitigation: Use only documents approved for that provider and avoid confidential, regulated, or customer content unless policy permits. <br>
Risk: The skill requires a Zhipu API key. <br>
Mitigation: Prefer revocable or scoped API keys where available, keep the key out of shared logs and files, and rotate it if exposed. <br>
Risk: Generated drafts may contain mistakes or misleading statements. <br>
Mitigation: Review the generated Markdown before publishing, submitting, or relying on it for decisions. <br>


## Reference(s): <br>
- [GLM-V Doc-Based-Writing homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-doc-based-writing) <br>
- [Zhipu Chat Completions API docs](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) <br>
- [Zhipu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown text by default, with optional Markdown or JSON file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; supports up to 50 remote documents or 50 local PDF pages, subject to model token limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
