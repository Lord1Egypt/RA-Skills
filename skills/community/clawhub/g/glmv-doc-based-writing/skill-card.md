## Description:

Writes Markdown content from user-provided documents and requirements using the ZhiPu GLM-V multimodal model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to draft articles, reports, briefs, reviews, proposals, plans, translations, and summaries after the agent reads supplied documents and writing requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents and writing requirements are sent to Zhipu's API for processing.

Mitigation: Use a dedicated API key and avoid sensitive or regulated documents unless the use has been approved.

Risk: Local PDF handling depends on PyMuPDF.

Mitigation: Install PyMuPDF in a virtual environment with a pinned version.

Risk: The --output option writes to the chosen local path and may overwrite an existing file.

Mitigation: Choose output paths deliberately and review existing files before writing results.

Risk: Generated writing may be inaccurate, incomplete, or inappropriate for the target context.

Mitigation: Review generated content against the source documents and intended audience before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/skills/glmv-doc-based-writing)
- [Project Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-doc-based-writing)
- [Zhipu Chat Completions API Documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
- [Zhipu API Key Management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text, with optional Markdown or JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; supports up to 50 remote documents or 50 local PDF pages; sends selected documents and writing requirements to Zhipu API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
